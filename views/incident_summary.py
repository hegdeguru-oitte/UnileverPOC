# pages/incident_summary.py
import streamlit as st
from services.detail_extractor import IncidentDetailExtractor
from ui.components import display_detailed_issue_info
from ui.counter import create_timer_app

def show():
    # st.title("📊 Incident Summary")

    if 'transcript' in st.session_state and st.session_state.transcript:
        if 'detailed_issue_info' not in st.session_state:
            if 'settings' in st.session_state:
                detailed_extractor = IncidentDetailExtractor(st.session_state.settings.OPENAI_API_KEY)
                detailed_issue_info = detailed_extractor.extract_detailed_issue_info(st.session_state.transcript)
                if detailed_issue_info:
                    st.session_state.detailed_issue_info = detailed_issue_info

        # Display timer first
        # create_timer_app()

        # Then display detailed information
        if 'detailed_issue_info' in st.session_state and st.session_state.detailed_issue_info:
            display_detailed_issue_info(st.session_state.detailed_issue_info)
        else:
            st.warning("Detailed incident information not available.")
    else:
        st.warning("Please upload and process an incident document in the Incident Details page first.")
