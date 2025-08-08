
# app.py
import os, json, re
import pandas as pd
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

# --- OpenAI client ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
client = OpenAI(api_key=OPENAI_API_KEY)
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4-turbo")

# --- Data ---
CSV_PATH = os.environ.get("TRIALS_CSV", "processed_clinical_trials.csv")
df_trials = pd.read_csv(CSV_PATH, low_memory=False)

_df = df_trials.copy()
_df["conditions_lc"] = _df["Conditions"].astype(str).str.lower()
_df["locations_lc"]  = _df["Locations"].astype(str).str.lower()
_df["status_str"]    = _df["OverallStatus"].astype(str)
_df["phase_str"]     = _df["Phase"].astype(str).str.upper()

def _norm_phase_token(user_phase: str | None) -> str | None:
    if not user_phase:
        return None
    p = str(user_phase).upper().replace(" ", "")
    p = p.replace("PHASEI", "PHASE1").replace("PHASEII", "PHASE2").replace("PHASEIII", "PHASE3")
    p = p.replace("EARLYPHASE1", "PHASE1")
    if "PHASE1" in p or re.search(r"\b1\b", p): return "PHASE1"
    if "PHASE2" in p or re.search(r"\b2\b", p): return "PHASE2"
    if "PHASE3" in p or re.search(r"\b3\b", p): return "PHASE3"
    return None

def _status_pattern(user_status: str | None) -> str | None:
    if not user_status:
        return None
    s = str(user_status).strip().lower()
    if s in ("recruiting", "recruit", "open", "active"):
        return r"(Recruiting|Not yet recruiting|Enrolling by invitation|Active, not recruiting)"
    return re.escape(user_status)

def search_clinical_trials(condition=None, location=None, status="Recruiting", phase=None, expand_status=True):
    df = _df
    if condition:
        df = df[df["conditions_lc"].str.contains(str(condition).lower(), na=False)]
    if location:
        df = df[df["locations_lc"].str.contains(str(location).lower(), na=False)]
    if status:
        pat = _status_pattern(status)
        if pat:
            df = df[df["status_str"].str.contains(pat, case=False, na=False, regex=True)]
    if phase:
        tok = _norm_phase_token(phase)
        if tok:
            df = df[df["phase_str"].str.contains(tok, na=False)]

    if df.empty and expand_status and status:
        df = _df
        if condition:
            df = df[df["conditions_lc"].str.contains(str(condition).lower(), na=False)]
        if location:
            df = df[df["locations_lc"].str.contains(str(location).lower(), na=False)]
        if phase:
            tok = _norm_phase_token(phase)
            if tok:
                df = df[df["phase_str"].str.contains(tok, na=False)]
    return df

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/healthz")
def healthz():
    return jsonify({"ok": True})

@app.route("/chat", methods=["POST"])
def chatbot_query():
    payload = request.get_json(silent=True) or {}
    user_input = (payload.get("user_input") or "").strip()
    if not user_input:
        return jsonify({"message": "Please enter a query."}), 400

    classify_prompt = f"""
    Return only valid JSON with keys:
    "type": "search_trials" | "general_info",
    "condition": string or null,
    "location": string or null,
    "status": string or null (default to "Recruiting" if not provided),
    "phase": string or null (e.g., "Phase 1"/"Phase 2"/"Phase 3").
    User query: "{user_input}"
    """.strip()

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Return only valid JSON, no commentary."},
                {"role": "user", "content": classify_prompt},
            ],
            temperature=0.0,
        )
        details = json.loads(resp.choices[0].message.content)
    except Exception as e:
        return jsonify({"error": f"AI parsing error: {e}"}), 500

    if (details.get("type") or "").lower() == "search_trials":
        condition = details.get("condition")
        location  = details.get("location")
        status    = details.get("status") or "Recruiting"
        phase     = details.get("phase")

        results = search_clinical_trials(condition, location, status, phase)
        if results.empty:
            return jsonify({"message": f"No trials found for {condition or 'any condition'} in {location or 'any location'} with status {status}."})

        out = []
        for _, row in results.head(5).iterrows():
            out.append({
                "title":       row.get("BriefTitle", ""),
                "nct_id":      row.get("NCTId", ""),
                "status":      row.get("OverallStatus", ""),
                "phase":       row.get("Phase", ""),
                "eligibility": (row.get("EligibilityCriteria", "") or "")[:1000],
            })

        follow_prompt = f"""
        Suggest three brief follow-up questions a user might ask next about:
        "{user_input}"
        Return only JSON: {{"questions": ["...","...","..."]}}
        """.strip()

        try:
            fu = client.chat.completions.create(
                model=MODEL,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "Return only valid JSON."},
                    {"role": "user", "content": follow_prompt},
                ],
                temperature=0.2,
            )
            follow_up = json.loads(fu.choices[0].message.content).get("questions", [])
        except Exception:
            follow_up = []

        return jsonify({"results": out, "follow_up_questions": follow_up})

    # general info path
    info_prompt = f'Answer in <=100 words, friendly and clear:\n"{user_input}"'
    try:
        g = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": info_prompt}],
            temperature=0.3,
        )
        answer = g.choices[0].message.content.strip()
    except Exception as e:
        return jsonify({"error": f"LLM error: {e}"}), 500

    return jsonify({"message": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
