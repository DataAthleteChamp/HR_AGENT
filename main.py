import streamlit as st
import data
import components

st.set_page_config(page_title="HR Agent - AI Medical Reports", layout="wide")

if "reports" not in st.session_state:
    if "patients" not in st.session_state:
        st.session_state.patients = data.PATIENTS.copy()
    if "doctors" not in st.session_state:
        st.session_state.doctors = data.DOCTORS.copy()
    st.session_state.reports = {p: [] for p in data.PATIENTS}
    for p, reps in data.INITIAL_REPORTS.items():
        if p in st.session_state.reports:
            st.session_state.reports[p].extend(reps)
        else:
            st.session_state.reports[p] = reps
    st.session_state.audit_log = []

# Sidebar: Role selection
st.sidebar.title("User Role")
role = st.sidebar.radio("Select role:", ("Doctor", "Patient", "Admin"), index=0)

# Sidebar: Depending on role, allow user selection (for Doctor/Patient)
if role == "Doctor":
    doctor_name = st.sidebar.selectbox("Doctor User", data.DOCTORS, index=0)
    components.show_doctor_ui(doctor_name)
elif role == "Patient":
    patient_name = st.sidebar.selectbox("Patient User", data.PATIENTS, index=0)
    components.show_patient_ui(patient_name)
elif role == "Admin":
    components.show_admin_ui()
