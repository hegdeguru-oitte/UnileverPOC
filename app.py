# app.py
import streamlit as st
from pages import incident_details, incident_summary
from config.styles import CSS_STYLES
from utils.session_state import initialize_session_state
from config.settings import Settings

def main():
    st.set_page_config(
        page_title="Major Incident Management",
        page_icon="🚨",
        layout="wide"
    )
    st.markdown(CSS_STYLES, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    if 'settings' not in st.session_state:
        st.session_state.settings = Settings()

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Incident Details", "Incident Summary"])

    # Page routing
    if page == "Incident Details":
        incident_details.show()
    else:
        incident_summary.show()

if __name__ == "__main__":
    main()
