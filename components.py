from datetime import datetime
import streamlit as st
import data
import ai_nlp


def show_doctor_ui(doctor_name: str):
    st.header("Doctor Dashboard")
    st.subheader(f"Logged in as: {doctor_name}")

    patient_name = st.selectbox("Select Patient", data.PATIENTS, key="doctor_selected_patient")

    st.markdown("### Generate New Report")
    symptoms = st.text_area("Patient Symptoms", "")

    if st.button("Generate Report"):
        if patient_name and symptoms:
            with st.spinner("Generating report..."):
                report_text = ai_nlp.generate_report(patient_name, symptoms)
            st.session_state.draft_report_text = report_text
            st.session_state.draft_patient = patient_name
            st.session_state.draft_doctor = doctor_name

            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.audit_log.append(
                f"{ts}: Doctor {doctor_name} generated a report for {patient_name} (draft)."
            )
            st.rerun()
        else:
            st.warning("Please provide both patient name and symptoms.")

    # === Draft Editing Section ===
    if (
        st.session_state.get("draft_report_text")
        and st.session_state.get("draft_patient") == patient_name
        and st.session_state.get("draft_doctor") == doctor_name
    ):
        st.subheader("Edit and Save Report")
        edited_text = st.text_area(
            "Generated Report",
            value=st.session_state.draft_report_text,
            #value=st.session_state.draft_report_text.replace("**", ""),
            height=400,
            key="edit_report_text"
        )

        if st.button("Save Report"):
            patient = st.session_state.draft_patient
            doctor = st.session_state.draft_doctor
            final_text = f"**Saved by {doctor}**\n\n" + edited_text  # Optional tag

            if patient not in st.session_state.reports:
                st.session_state.reports[patient] = []
            st.session_state.reports[patient].append({
                "doctor": doctor,
                "report": final_text,
                "feedback": []
            })

            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.audit_log.append(
                f"{ts}: Doctor {doctor} saved a report for {patient}."
            )

            del st.session_state["draft_report_text"]
            del st.session_state["draft_patient"]
            del st.session_state["draft_doctor"]

            st.success("Report saved successfully.")
            st.rerun()

    # === Past Reports Section ===
    st.markdown("### Your Past Reports for This Patient")
    reports = st.session_state.reports.get(patient_name, [])
    own_reports = [r for r in reports if r["doctor"] == doctor_name]

    if not own_reports:
        st.info("No reports found.")
    else:
        for idx, rep in enumerate(own_reports):
            st.markdown(rep["report"])  # display as markdown
            if rep["feedback"]:
                st.markdown("**Feedback from Patient:**")
                for fb in rep["feedback"]:
                    st.markdown(f"- {fb}")
            else:
                st.markdown("_No feedback yet._")

            # Edit/Delete options
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"Edit Report {idx+1}"):
                    st.session_state.draft_report_text = rep["report"]
                    st.session_state.draft_patient = patient_name
                    st.session_state.draft_doctor = doctor_name
                    st.session_state.reports[patient_name].remove(rep)
                    st.rerun()
            with col2:
                if st.button(f"Delete Report {idx+1}"):
                    st.session_state.reports[patient_name].remove(rep)
                    st.success("Report deleted.")
                    st.rerun()
            st.markdown("---")



def show_patient_ui(patient_name: str):
    """Display the Patient interface for viewing reports and giving feedback."""
    st.header("Patient Dashboard")
    st.subheader(f"Logged in as {patient_name}")
    reports = st.session_state.reports.get(patient_name, [])
    if not reports:
        st.info("No reports available for you yet.")
    else:
        safe_patient = patient_name.replace(' ', '_')
        for idx, rep in enumerate(reports):
            st.markdown(f"**Report {idx+1} – Doctor: {rep['doctor']}**")
            # st.text_area(f"Report {idx+1}", value=rep['report'], height=450, key=f"patient_report_{safe_patient}_{idx}", disabled=True)
            st.markdown(rep["report"])
            if rep['feedback']:
                st.markdown("**Your Feedback:**")
                for fb in rep['feedback']:
                    st.write(f"- {fb}")
            fb_key = f"feedback_input_{safe_patient}_{idx}"
            st.text_input("Add feedback", key=fb_key)
            if st.button("Submit Feedback", key=f"feedback_btn_{safe_patient}_{idx}"):
                feedback_text = st.session_state.get(fb_key, "")
                if feedback_text:
                    rep['feedback'].append(feedback_text)
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.audit_log.append(f"{ts}: Patient {patient_name} submitted feedback on report {idx+1}.")
                    st.success("Feedback submitted.")
                else:
                    st.warning("Feedback text is empty.")
            st.write("---")

def show_admin_ui():
    """Admin interface: view/edit reports, manage users, audit log."""
    st.header("Admin Dashboard")

    # ============================
    # Reports Viewer
    # ============================
    st.subheader("📄 All Reports")
    if not st.session_state.reports:
        st.info("No reports available.")
    else:
        for patient, rep_list in st.session_state.reports.items():
            if rep_list:
                st.markdown(f"**Patient: {patient}**")
                safe_patient = patient.replace(' ', '_')
                for idx, rep in enumerate(rep_list):
                    st.markdown(f"- Report {idx+1} by **{rep['doctor']}**:")
                    # st.text_area(
                    #     f"admin_report_{safe_patient}_{idx}",
                    #     value=rep['report'],
                    #     height=400,
                    #     disabled=True
                    # )
                    st.markdown(rep["report"])
                    if rep['feedback']:
                        st.markdown(f"➡ Feedback: {', '.join(rep['feedback'])}")
                    else:
                        st.markdown("➡ Feedback: (No feedback)")
            st.markdown("---")

    # ============================
    # Feedback Summary
    # ============================
    st.subheader("💬 All Feedback")
    feedback_found = False
    for patient, rep_list in st.session_state.reports.items():
        for idx, rep in enumerate(rep_list):
            for fb in rep['feedback']:
                feedback_found = True
                st.write(f"- {patient} (Report {idx+1} by {rep['doctor']}): {fb}")
    if not feedback_found:
        st.info("No feedback submitted yet.")

    # ============================
    # User Management
    # ============================
    st.subheader("👤 Manage Users")

    col1, col2 = st.columns(2)

    # --- Manage Doctors ---
    with col1:
        st.markdown("### 🩺 Doctors")
        new_doctor = st.text_input("Add new doctor")
        if st.button("Add Doctor"):
            if new_doctor and new_doctor not in data.DOCTORS:
                data.DOCTORS.append(new_doctor)
                st.success(f"Doctor '{new_doctor}' added.")
            else:
                st.warning("Doctor already exists or name is empty.")

        if st.selectbox("Delete Doctor", [""] + data.DOCTORS, key="delete_doc") != "":
            doc_to_delete = st.session_state["delete_doc"]
            if st.button("Confirm Delete Doctor"):
                data.DOCTORS.remove(doc_to_delete)
                st.success(f"Doctor '{doc_to_delete}' deleted.")
                st.rerun()

    # --- Manage Patients ---
    with col2:
        st.markdown("### 🧑 Patients")
        new_patient = st.text_input("Add new patient")
        if st.button("Add Patient"):
            if new_patient and new_patient not in data.PATIENTS:
                data.PATIENTS.append(new_patient)
                st.success(f"Patient '{new_patient}' added.")
            else:
                st.warning("Patient already exists or name is empty.")

        if st.selectbox("Delete Patient", [""] + data.PATIENTS, key="delete_pat") != "":
            pat_to_delete = st.session_state["delete_pat"]
            if st.button("Confirm Delete Patient"):
                data.PATIENTS.remove(pat_to_delete)
                st.success(f"Patient '{pat_to_delete}' deleted.")
                st.rerun()

    # ============================
    # Audit Logs
    # ============================
    st.subheader("🕵️ Audit Log")
    if st.session_state.audit_log:
        for entry in st.session_state.audit_log:
            st.markdown(f"- {entry}")
    else:
        st.info("Audit log is empty.")
