# app.py
import streamlit as st
from config.settings import Settings
from config.styles import CSS_STYLES
from services.incident_manager import IncidentManager
from services.detail_extractor import IncidentDetailExtractor
from services.email_service import EmailService
from ui.components import ( display_incident_details, display_detailed_issue_info, display_email_section)
from utils.session_state import initialize_session_state, update_file_state


def main():
    st.set_page_config(
        page_title="Major Incident Management",
        page_icon="🚨",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    st.markdown(CSS_STYLES, unsafe_allow_html=True)
    
    st.title("🚨 Major Incident Management")
    initialize_session_state()
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

        if st.button("Send Notification"):
            subject = f"Major Incident: {st.session_state.incident_data.get('short_description', 'N/A')}"
            recipients = list(set(
                st.session_state.recipients +
                [email.strip() for email in additional_recipients.split(',') if email.strip()]
            ))
            html_content = EmailService.generate_email_html(st.session_state.incident_data)
            EmailService.send_email(recipients, subject, html_content)
            st.success("Notification sent successfully!")

    if 'transcript' in st.session_state and st.session_state.transcript:
        if 'detailed_issue_info' not in st.session_state:
            detailed_extractor = IncidentDetailExtractor(incident_manager.settings.OPENAI_API_KEY)
            detailed_issue_info = detailed_extractor.extract_detailed_issue_info(st.session_state.transcript)
            if detailed_issue_info:
                st.session_state.detailed_issue_info = detailed_issue_info

        # Display detailed issue information if it exists

    if 'detailed_issue_info' in st.session_state and st.session_state.detailed_issue_info:
        display_detailed_issue_info(st.session_state.detailed_issue_info)



if __name__ == "__main__":
    main()