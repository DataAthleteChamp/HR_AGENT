# HR Agent – AI-Powered Medical Documentation System

## 🔍 Overview

HR Agent is a Streamlit-based simulation of an AI-assisted medical documentation system. It mimics a hospital-like environment for three roles: Doctor, Patient, and Admin.

* Doctors generate reports based on patient symptoms using a locally hosted language model (`distilgpt2`).
* Patients can view their personal reports and provide feedback.
* Admins audit all reports and user activities via a central dashboard.

The app runs entirely **offline**, uses **no API keys**, and includes **dummy users and data** for testing.

---

## 📆 Project Structure

```
hr_agent_streamlit/
├── main.py           # Main Streamlit app
├── ai_nlp.py         # AI generation logic using distilgpt2
├── data.py           # Dummy users and test reports
├── components.py     # UI logic for Doctor, Patient, Admin
├── requirements.txt  # Dependencies
```

---

## 🚀 How to Run

### 1. ✅ Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate      # On Windows
```

### 2. ✅ Install dependencies

```bash
pip install -r requirements.txt
```

### 3. ✅ Run the app

```bash
streamlit run main.py
```

---

## 👥 Roles and Features

| Role    | Features                                                                        |
| ------- | ------------------------------------------------------------------------------- |
| Doctor  | - Select patient<br>- Enter symptoms<br>- Generate/edit reports<br>- Save final |
| Patient | - View own reports<br>- Submit feedback                                         |
| Admin   | - View all reports<br>- See all feedback<br>- Audit user actions                |

---

## 📚 Tech Stack

* **Streamlit** – interactive UI
* **Transformers** – AI model (distilgpt2)
* **Torch** – model engine
* **Session State** – in-memory mock database

---

## 🧪 Notes

* Data resets when the app restarts (uses `session_state`).
* AI generation is simulated locally using `distilgpt2`.
* Feedback and audit logs are stored per session.
