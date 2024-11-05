# pages/incident_details.py
import streamlit as st
from services.incident_manager import IncidentManager
from services.email_service import EmailService
from ui.components import display_incident_details, display_email_section
from utils.session_state import update_file_state

def show():
    st.title("🚨 Incident Details")

    incident_manager = IncidentManager()

    uploaded_file = st.file_uploader("Choose a DOCX file", type="docx")
    if uploaded_file:
        if 'transcript' not in st.session_state:
            transcript = incident_manager.read_docx(uploaded_file)
            st.session_state.transcript = transcript
            st.session_state.incident_data = incident_manager.extract_incident_details(transcript)
            st.success("Transcript processed successfully!")
            update_file_state()

    if st.session_state.incident_data:
        display_incident_details(st.session_state.incident_data)
        additional_recipients = display_email_section(
            st.session_state.incident_data,
            st.session_state.recipients,
            st.session_state.show_process_button
        )

        if st.button("Send Notification", key="send_notification_btn"):
            subject = f"Major Incident: {st.session_state.incident_data.get('short_description', 'N/A')}"
            recipients = list(set(
                st.session_state.recipients +
                [email.strip() for email in additional_recipients.split(',') if email.strip()]
            ))
            html_content = EmailService.generate_email_html(st.session_state.incident_data)
            EmailService.send_email(recipients, subject, html_content)
            st.success("Notification sent successfully!")
