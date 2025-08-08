
# ClinicalTrialMD Chat

Simple Flask app that searches a clinical-trials CSV and uses an LLM to interpret questions.

## Repo Structure
- `app.py` — Flask API + query logic (uses env: `OPENAI_API_KEY`, `OPENAI_MODEL`, `TRIALS_CSV`)
- `templates/index.html` — Minimal UI
- `requirements.txt`
- `service/ctchat.service` — systemd unit (binds to 127.0.0.1:8000)
- `caddy/Caddyfile` — optional HTTPS reverse proxy config
- `.gitignore` — prevents large CSV / secrets from being committed

## Local Run
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...          # set your key
export OPENAI_MODEL=gpt-4-turbo       # or gpt-4o, etc.
export TRIALS_CSV=processed_clinical_trials.csv
python app.py
# open http://127.0.0.1:5001
```

## Deploy on EC2 (summary)
1) Copy repo to `/home/ubuntu/chatbot/app` and your CSV to the same folder.
2) Create env file `/etc/ctchat.env`:
```
OPENAI_API_KEY=sk-...                   
TRIALS_CSV=/home/ubuntu/chatbot/app/processed_clinical_trials.csv
OPENAI_MODEL=gpt-4-turbo
```
3) Create service:
```bash
sudo cp service/ctchat.service /etc/systemd/system/ctchat.service
sudo systemctl daemon-reload
sudo systemctl enable --now ctchat
```
4) (Optional) Caddy HTTPS:
```bash
sudo apt install -y caddy
sudo cp caddy/Caddyfile /etc/caddy/Caddyfile
sudo systemctl enable --now caddy
sudo systemctl reload caddy
```
DNS: point A records for your domain to your Elastic IP.

## GitHub Pages?
GitHub Pages hosts **static** sites only (HTML/CSS/JS). This backend needs a server (EC2). You *can* host just the frontend on Pages and point its JS to your EC2 API (enable CORS).
