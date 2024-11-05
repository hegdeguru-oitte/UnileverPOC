# ui/components.py
import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components
from  ui.counter import create_timer_app

import time

def display_incident_details(incident_data):
    """Display basic incident details from the initial extraction."""
    st.markdown("<div class='incident-header'><h2>Incident Details</h2></div>", unsafe_allow_html=True)
    for key, value in incident_data.items():
        if isinstance(value, dict):
            st.write(f"**{key.replace('_', ' ').title()}:**")
            for sub_key, sub_value in value.items():
                st.write(f"  - {sub_key}: {sub_value}")
        elif isinstance(value, list):
            st.write(f"**{key.replace('_', ' ').title()}:** {', '.join(value)}")
        else:
            st.write(f"**{key.replace('_', ' ').title()}:** {value}")

def display_email_section(incident_data, recipients, show_process_button):
    """Display the email composition section."""
    st.subheader("Send Incident Notification Email")
    if show_process_button:
        st.write(", ".join(recipients))
        additional_recipients = st.text_input(
            "Add additional recipients (comma-separated)",
            key="additional_recipients"
        )
        return additional_recipients
    return ""

def display_incident_header(detailed_data):
    """Display the incident summary header."""
    st.markdown(f"""
        <div class="incident-header">
            <h3>📝 Incident Summary</h3>
        </div>
    """, unsafe_allow_html=True)

def display_primary_info(detailed_data):
    """Display primary incident information in the left column."""
    with st.container():
        st.markdown(f"""
        <div class="info-box">
            <p><strong>🚨 Incident ID:</strong> {detailed_data.get('issue_id', 'N/A')}</p>
            <p><strong>📍 Location:</strong> {detailed_data.get('issue_description', {}).get('affected_location', 'N/A')}</p>
            <p><strong>👥 Users Affected:</strong> {detailed_data.get('issue_description', {}).get('users_affected', 'N/A')}</p>
            <p><strong>🔧 Ticket:</strong> {detailed_data.get('issue_description', {}).get('ticket_number', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

def display_impact_info(detailed_data):
    """Display impact information in the right column."""
    with st.container():
        st.markdown(f"""
        <div class="info-box">
            <p><strong>Business Impact:</strong> {detailed_data.get('issue_description', {}).get('business_impact', 'N/A')}</p>
            <p><strong>Financial Impact:</strong> {detailed_data.get('issue_description', {}).get('financial_sales_loss', 'N/A')}</p>
            <p><strong>Business working hours:</strong> {detailed_data.get('issue_description', {}).get('business_working_hours', 'N/A')}</p>
            <p><strong>Workaround Available:</strong> {detailed_data.get('issue_description', {}).get('workaround_available', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

def display_actions_timeline(actions):
    """Display the actions timeline."""
    st.markdown("### 🔄 Actions Timeline")
    with st.container():
        for i, action in enumerate(actions, 1):
            st.markdown(f"""
            <div class="info-box">
                <strong>Step {i}:</strong> {action}
            </div>
            """, unsafe_allow_html=True)

def display_participants(participants):
    """Display the participants list."""
    st.markdown("### 👥 Participants")
    with st.container():
        for participant in participants:
            st.markdown(f"""
            <div class="info-box">
                {participant}
            </div>
            """, unsafe_allow_html=True)

def display_additional_info(additional_info):
    """Display additional information."""
    st.markdown("### 📋 Additional Information")
    with st.container():
        for info in additional_info:
            st.markdown(f"""
            <div class="info-box">
                {info}
            </div>
            """, unsafe_allow_html=True)

def display_detailed_issue_info(detailed_data):
    """Display all detailed issue information in a structured layout."""
    if not detailed_data:
        st.warning("No detailed information available")
        return

    # Display header
    display_incident_header(detailed_data)
    # display_status_cards()
    create_timer_app()
    
    # Layout for primary and impact information
    col1, col2 = st.columns(2)
    
    with col1:
        display_primary_info(detailed_data)
    
    with col2:
        display_impact_info(detailed_data)

    st.markdown("---")

    # Layout for timeline, participants, and additional info
    col4, col5, col6 = st.columns([3,3,3])
    
    with col4:
        display_actions_timeline(detailed_data.get("actions_taken", []))
    
    with col5:
        display_participants(detailed_data.get("participants", []))
    
    with col6:
        display_additional_info(detailed_data.get("additional_info", []))


def get_incident_start_time():
    """
    Returns the incident start time. Currently returns a fixed time for display.
    TODO: In the future, this can be modified to get the time from:
    - API call
    - Database
    - Incident management system
    - External service
    """
    # Fixed time for display (13:00 today)
    today = datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)
    return today

    # Future implementation examples (commented out):
    # return api_service.get_incident_start_time()  # From API
    # return db.query_incident_start_time()         # From database
    # return incident_system.get_start_time()       # From incident system
    # return external_service.fetch_start_time()    # From external service


#Pass the incident_data later to this function
# def display_status_cards():
#     # Create three columns for the cards
#     col1, col2, col3 = st.columns(3)
    
#     # Card 1: Incident Status
#     with col1:
#         st.markdown("""
#             <div style="padding: 1rem; border-radius: 0.5rem; border: 1px solid #e0e0e0; background-color: #f8f9fa">
#                 <h4 style="margin: 0; color: #1f77b4;">Incident Status</h4>
#                 <p style="font-size: 1.25rem; margin: 0.5rem 0; color: #2c3e50; font-weight: bold;">
#                     {status}
#                 </p>
#             </div>
#         """.format(status='Active'
#                     #"""incident_data.get('status', 'Active')"""
#                     ), unsafe_allow_html=True)
    
#     # Card 2: Incident Reported Time
#     with col2:
#         reported_time = get_incident_start_time().strftime("%Y-%m-%d %H:%M")
#         st.markdown("""
#             <div style="padding: 1rem; border-radius: 0.5rem; border: 1px solid #e0e0e0; background-color: #f8f9fa">
#                 <h4 style="margin: 0; color: #1f77b4;">Reported Time</h4>
#                 <p style="font-size: 1.25rem; margin: 0.5rem 0; color: #2c3e50; font-weight: bold;">
#                     {time}
#                 </p>
#             </div>
#         """.format(time=reported_time), unsafe_allow_html=True)
    
#        # Card 3: Live Incident Timer
#     with col3:
#         # Header for the timer card and timer display combined
#         st.markdown(f"""
#             <div style="padding: 1rem; border-radius: 0.5rem; border: 1px solid #e0e0e0; background-color: #f8f9fa">
#                 <h4 style="margin: 0; color: #1f77b4;">Incident Duration</h4>
#                 <p id="timer" style="font-size: 1.5rem; margin: 0.5rem 0; color: #2c3e50; font-weight: bold;">
#                 </p>
#             </div>
#         """, unsafe_allow_html=True)

#         # Timer JavaScript
#         timer_script = """
#             <script>
#                 function updateTimer() {
#                     const startTime = new Date();
#                     startTime.setHours(13, 0, 0, 0);  // Set to 13:00:00
                    
#                     const now = new Date();
#                     const diff = Math.floor((now - startTime) / 1000);
                    
#                     const hours = Math.floor(diff / 3600);
#                     const minutes = Math.floor((diff % 3600) / 60);
#                     const seconds = diff % 60;
                    
#                     const formattedTime = 
#                         String(hours).padStart(2, '0') + ':' +
#                         String(minutes).padStart(2, '0') + ':' +
#                         String(seconds).padStart(2, '0');
                    
#                     document.getElementById('timer').innerText = formattedTime;
#                 }
                
#                 // Update timer immediately and every second
#                 updateTimer();
#                 setInterval(updateTimer, 1000);
#             </script>
#         """

#         # Inject the timer script to execute
#         components.html(timer_script, height=0)  # Height is set to 0 because we only need to run the script








# def display_status_cards():
#     # Get the reported start time
#     reported_time = get_incident_start_time().strftime("%Y-%m-%d %H:%M")
    
#     # Create HTML content for all cards with consistent styling
#     cards_html = f"""
#     <div style="display: flex; gap: 1rem;">
        
#         <!-- Incident Status Card -->
#         <div style="flex: 1; padding: 1rem; border-radius: 0.5rem; border: 1px solid #e0e0e0; background-color: #f8f9fa;">
#             <h4 style="margin: 0; color: #1f77b4;">Incident Status</h4>
#             <p style="font-size: 1.25rem; margin: 0.5rem 0; color: #2c3e50; font-weight: bold;">
#                 Active
#             </p>
#         </div>
        
#         <!-- Reported Time Card -->
#         <div style="flex: 1; padding: 1rem; border-radius: 0.5rem; border: 1px solid #e0e0e0; background-color: #f8f9fa;">
#             <h4 style="margin: 0; color: #1f77b4;">Reported Time</h4>
#             <p style="font-size: 1.25rem; margin: 0.5rem 0; color: #2c3e50; font-weight: bold;">
#                 {reported_time}
#             </p>
#         </div>
        
#         <!-- Incident Duration Card with JavaScript Timer -->
#         <div style="flex: 1; padding: 1rem; border-radius: 0.5rem; border: 1px solid #e0e0e0; background-color: #f8f9fa;">
#             <h4 style="margin: 0; color: #1f77b4;">Incident Duration</h4>
#             <p id="timer" style="font-size: 1.25rem; margin: 0.5rem 0; color: #2c3e50; font-weight: bold;">
#                 00:00:00
#             </p>
#         </div>
        
#     </div>

#     <script>
#         const startTime = new Date("{get_incident_start_time().strftime('%Y-%m-%d %H:%M:%S')}");

#         function updateTimer() {{
#             const now = new Date();
#             const diff = Math.floor((now - startTime) / 1000);
            
#             const hours = Math.floor(diff / 3600);
#             const minutes = Math.floor((diff % 3600) / 60);
#             const seconds = diff % 60;
            
#             const formattedTime = 
#                 String(hours).padStart(2, '0') + ':' +
#                 String(minutes).padStart(2, '0') + ':' +
#                 String(seconds).padStart(2, '0');
            
#             document.getElementById('timer').innerText = formattedTime;
#         }}
        
#         updateTimer();
#         setInterval(updateTimer, 1000);
#     </script>
#     """

#     # Use components.html to render HTML/JS in Streamlit
#     components.html(cards_html, height=100)







