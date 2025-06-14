import openai
import os
import random
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_report(patient_name: str, symptoms: str) -> str:
    date = datetime.now().strftime("%Y-%m-%d")
    clinics = [
        ("Sunrise Medical Center", "New York, NY"),
        ("Harmony Health Clinic", "Los Angeles, CA"),
        ("Greenfield Hospital", "Chicago, IL"),
        ("Starlight Medical Institute", "Austin, TX"),
        ("Evercare Health Center", "Miami, FL")
    ]
    clinic_name, clinic_location = random.choice(clinics)

    prompt = f"""
You are a professional medical documentation assistant.
Generate a brief, structured clinical report in a formal medical tone using the input below.

Date: {date}  
Clinic: {clinic_name}, {clinic_location}  
Patient Name: {patient_name}  
Symptoms: {symptoms}

Format the report with the following sections:

**{clinic_name}, {clinic_location}**  
**Date: {date}**  
**Medical Report for Patient: {patient_name}**

---

**1. Chief Complaint:**  
Brief summary of presenting symptoms.

**2. Diagnosis:**  
Brief clinical explanation of the likely disease.

**3. Recommended Investigations:**  
Bullet list of suggested investigations.

**4. Medications Prescribed:**  
Bullet list of relevant medications, or 'None' if not applicable.

**5. Treatment Plan:**  
Concise instructions for management and follow-up.

**6. Signature:**  
[Your Name]  
Medical Documentation Assistant  
{clinic_name}, {clinic_location}
    """.strip()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=600,
    )

    return response.choices[0].message.content.strip()
