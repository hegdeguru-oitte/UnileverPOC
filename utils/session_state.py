# utils/session_state.py
import streamlit as st
from config.settings import Settings

def initialize_session_state():
    """Initialize session state variables"""
    if 'incident_data' not in st.session_state:
        st.session_state.incident_data = None
    if 'recipients' not in st.session_state:
        st.session_state.recipients = Settings().DEFAULT_RECIPIENTS
    if 'additional_recipients' not in st.session_state:
        st.session_state.additional_recipients = ""
    if 'show_process_button' not in st.session_state:
        st.session_state.show_process_button = False

def update_file_state():
    st.session_state.show_process_button = True