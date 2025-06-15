# 🏥 AI Clinical Documentation Assistant

An interactive Streamlit-based web app designed to assist doctors in generating, managing, and reviewing clinical reports using OpenAI's GPT models. The app supports markdown-rendered reports, feedback from patients, and full administrative control over users and audit logs.

---

## 📆 Features

### 👨‍⚕️ Doctor Panel
- Generate structured medical reports based on patient symptoms
- Edit and save reports
- View only your own previously submitted reports
- See feedback submitted by patients
- Edit/delete your own past reports

### 🧑‍⚕️ Patient Panel
- View reports submitted by doctors
- Submit feedback on individual reports
- Read markdown-formatted reports with proper styling

### 🔐 Admin Panel
- View **all** reports and feedback across users
- Add or delete doctors and patients
- Monitor audit logs for all user activity

---

## 🧠 AI Report Generation

Utilizes `gpt-3.5-turbo` via the OpenAI API. The AI:
- Formats reports in markdown with clinical sections:
  - Chief Complaint
  - Diagnosis
  - Recommended Investigations
  - Medications Prescribed
  - Treatment Plan
  - Signature block
- Randomly assigns clinic names and locations for realism

---

## 📁 File Structure

```
HR_Agent_app/
│
├── ai_nlp.py             # AI report generation logic using OpenAI
├── components.py         # Streamlit UI components for roles
├── data.py               # Static lists of doctors, patients, and sample reports
├── main.py               # App launcher with login and navigation
├── .env                  # API key config (not shared)
├── requirements.txt      # All Python dependencies
└── README.md             # You're reading it!
```

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-user/HR_Agent_app.git
cd HR_Agent_app
```

### 2. Set up a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Set up OpenAI API Key

Create a `.env` file:

```
OPENAI_API_KEY=your-api-key-here
```

Or set it via terminal:

```bash
export OPENAI_API_KEY=your-api-key-here  # macOS/Linux
set OPENAI_API_KEY=your-api-key-here     # Windows
```

### 5. Run the App

```bash
streamlit run main.py
```

Then open your browser to `http://localhost:8501`.

---

## 📝 Initial Users

```python
# data.py
DOCTORS = ["Dr. Alice Smith", "Dr. Bob Jones"]
PATIENTS = ["John Doe", "Jane Roe"]
```

---

## 📌 Notes

- Markdown rendering is used for medical reports.
- Doctors can only access their own reports.
- Patient feedback and audit logs are preserved in session.
- Admins can fully manage system data in real time.

---

## 📃 License

MIT License © 2025 HR Agent Team

## 📧 Contact
For any issues or contributions, please open an issue on GitHub or contact us at 266502@student.pwr.edu.pl
