# Clinical_Trial_Chatbot

Frontend (GitHub Pages) + backend service for clinical trial chatbot.

A conversational AI tool designed to help users search, filter, and understand information from clinical trial databases such as [ClinicalTrials.gov](https://clinicaltrials.gov/).

---

## ✨ Features
- **Natural language queries** about ongoing or completed clinical trials
- **Filter by** condition, location, phase, sponsor, etc.
- **Readable summaries** of eligibility, interventions, arms, and outcomes
- **Integration-ready** with OpenAI/Hugging Face/custom models
- **Web UI** that runs on GitHub Pages (no install for end users)

---

## 📦 Project Structure
```text
Clinical_Trial_Chatbot/
├── backend/                   # Python backend (Flask/FastAPI) - API & chatbot logic
│   ├── app.py                 # Main server script (exposes /api/health, /api/chat)
│   ├── requirements.txt       # Backend-specific dependencies (if separate)
│   └── ...                    # Other backend modules (routers, services, utils)
│
├── docs/                      # Frontend (served via GitHub Pages)
│   ├── index.html             # Main chatbot UI (calls backend /api/chat)
│   ├── style.css              # Optional styles
│   └── script.js              # Optional JS (set BACKEND_URL here if split)
│
├── data/                      # (Optional) datasets or preprocessed files
│   └── ...
│
├── requirements.txt           # Project-wide Python dependencies (if used)
├── LICENSE                    # License (MIT recommended)
└── README.md                  # This file
