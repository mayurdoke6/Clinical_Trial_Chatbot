# Clinical_Trial_Chatbot
Frontend (GitHub Pages) + backend service for clinical trial chatbot.

A conversational AI tool designed to help users search, filter, and understand information from clinical trial databases such as [ClinicalTrials.gov](https://clinicaltrials.gov/).

This project has two main components:
1. **Frontend (UI)** — Hosted on GitHub Pages for easy access via a browser.
2. **Backend API** — Handles chatbot logic, calls to LLM APIs, and data retrieval.

---

## 🚀 Features
- **Natural Language Queries** — Users can ask questions in plain English about ongoing or completed clinical trials.
- **Advanced Search Filters** — Narrow results by condition, location, study phase, sponsor, and more.
- **Summarized Results** — Provides easy-to-read summaries of trial eligibility, interventions, and outcomes.
- **Integration Ready** — Can connect to OpenAI API, Hugging Face models, or custom-trained LLMs.
- **Web-based Interface** — Accessible via desktop and mobile browsers.

---

A conversational AI tool to search, filter, and understand information from clinical trial databases such as [ClinicalTrials.gov](https://clinicaltrials.gov/).

Clinical_Trial_Chatbot/
├── backend/             # Python backend (Flask/FastAPI) - API & chatbot logic
│   ├── app.py            # Main server script
│   ├── requirements.txt  # Backend-specific dependencies
│   └── ...               # Other backend files/modules
│
├── docs/                 # Frontend files (served via GitHub Pages)
│   ├── index.html         # Main chatbot UI
│   ├── style.css          # Optional CSS
│   └── script.js          # Optional JS logic
│
├── data/                 # (Optional) datasets or preprocessed files
│   └── ...                
│
├── requirements.txt      # Full project dependencies (if shared)
├── LICENSE               # Project license
└── README.md             # Documentation (this file)
