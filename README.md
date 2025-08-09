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


  
**Live App:** http://52.15.154.10/

---
  
## 🧰 Local Setup (optional, for developers)

### 1) Clone
```bash
git clone git@github.com:mayurdoke6/Clinical_Trial_Chatbot.git
cd Clinical_Trial_Chatbot

##  Environment & deps
python3 -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

# If using a single root requirements.txt:
pip install -r requirements.txt

# OR if backend has its own requirements.txt:
pip install -r backend/requirements.txt

---
  
## 👩‍💻 Usage (hosted)
End users can directly access the chatbot here:

http://52.15.154.10/

---  
## 📄 License
MIT License — see LICENSE.
---  
## 📬 Contact
Author: Mayur Doke
Email: mayurdoke@gmail.com
Repo: https://github.com/mayurdoke6/Clinical_Trial_Chatbot

