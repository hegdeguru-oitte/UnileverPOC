import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd
import io

def initialize_session_state():
    """
    Initialize session state variables for incident timing and phases.
    
    Sets up the following state variables:
    - incident_active (bool): Whether an incident is currently active
    - start_time (datetime): When the incident started
    - current_phase (int): Current phase number (1-4)
    - phase_history (list): History of completed phases
    - current_phase_start (datetime): When current phase started
    """
    if 'incident_active' not in st.session_state:
        st.session_state.incident_active = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = 1
    if 'phase_history' not in st.session_state:
        st.session_state.phase_history = []
    if 'current_phase_start' not in st.session_state:
        st.session_state.current_phase_start = None

def update_phase_history(phase_num, end_time):
    """
    Update phase history when a phase ends
    """
    PHASE_NAMES = {
        1: "P1/PMI Decision",
        2: "First Update",
        3: "Second Update",
        4: "Third Update"
    }
    
    if st.session_state.current_phase_start:
        duration = (end_time - st.session_state.current_phase_start).total_seconds() / 60  # in minutes
        st.session_state.phase_history.append({
            'Phase': PHASE_NAMES[phase_num],
            'Start Time': st.session_state.current_phase_start.strftime('%Y-%m-%d %H:%M:%S'),
            'End Time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'Duration (minutes)': round(duration, 2)
        })

def export_phase_data():
    """
    Create and return exportable phase history data
    """
    if not st.session_state.phase_history:
        return None
    
    df = pd.DataFrame(st.session_state.phase_history)
    
    # Add current phase if incident is active
    if st.session_state.incident_active and st.session_state.current_phase_start:
        current_duration = (datetime.now() - st.session_state.current_phase_start).total_seconds() / 60
        current_phase = {
            'Phase': f"Phase {st.session_state.current_phase}",
            'Start Time': st.session_state.current_phase_start.strftime('%Y-%m-%d %H:%M:%S'),
            'End Time': 'Ongoing',
            'Duration (minutes)': round(current_duration, 2)
        }
        df = pd.concat([df, pd.DataFrame([current_phase])], ignore_index=True)
    
    return df

def create_status_cards():
    """
    Creates the status cards with live timers using HTML/JavaScript
    """
    # Phase configurations
    PHASE_DURATIONS = {
        1: 15 * 60,  # 15 minutes in seconds
        2: 60 * 60,  # 60 minutes in seconds
        3: 60 * 60,  # 60 minutes in seconds
        4: 60 * 60   # 60 minutes in seconds
    }
    
    PHASE_DESCRIPTIONS = {
        1: "Awaiting P1/PMI Decision",
        2: "Time until 1st Update",
        3: "Time until 2nd Update",
        4: "Time until 3rd Update"
    }

    start_time_str = st.session_state.start_time.strftime('%Y-%m-%d %H:%M:%S') if st.session_state.start_time else ''
    current_phase = st.session_state.current_phase
    
    cards_html = f"""
    <div style="display: flex; gap: 1rem;">
        <!-- Incident Status Card -->
        <div style="flex: 1; padding: 1rem; border-radius: 0.5rem; border: 1px solid #e0e0e0; background-color: #f8f9fa;">
            <h4 style="margin: 0; color: #1f77b4;">Incident Status</h4>
            <p style="font-size: 1.25rem; margin: 0.5rem 0; color: #2c3e50; font-weight: bold;">
                {("Active" if st.session_state.incident_active else "Inactive")}
            </p>
        </div>
        
        <!-- Reported Time Card -->
        <div style="flex: 1; padding: 1rem; border-radius: 0.5rem; border: 1px solid #e0e0e0; background-color: #f8f9fa;">
            <h4 style="margin: 0; color: #1f77b4;">Reported Time</h4>
            <p style="font-size: 1.25rem; margin: 0.5rem 0; color: #2c3e50; font-weight: bold;">
                {(st.session_state.start_time.strftime("%Y-%m-%d %H:%M") if st.session_state.start_time else "Not Started")}
            </p>
        </div>
        
        <!-- Incident Duration Card -->
        <div style="flex: 1; padding: 1rem; border-radius: 0.5rem; border: 1px solid #e0e0e0; background-color: #f8f9fa;">
            <h4 style="margin: 0; color: #1f77b4;">Incident Duration</h4>
            <p id="timer" style="font-size: 1.25rem; margin: 0.5rem 0; color: #2c3e50; font-weight: bold;">
                00:00:00
            </p>
        </div>
        
        <!-- Phase Timer Card -->
        <div style="flex: 1; padding: 1rem; border-radius: 0.5rem; border: 1px solid #e0e0e0; background-color: #f8f9fa;">
            <h4 style="margin: 0; color: #1f77b4;">Phase Timer</h4>
            <p id="phase-timer" style="font-size: 1.25rem; margin: 0.5rem 0; color: #2c3e50; font-weight: bold;">
                00:00
            </p>
            <p id="phase-description" style="font-size: 0.9rem; margin: 0.25rem 0; color: #2c3e50;">
                {PHASE_DESCRIPTIONS.get(current_phase, '')}
            </p>
        </div>
    </div>

    <script>
        const startTime = new Date("{start_time_str}");
        const currentPhase = {current_phase};
        const phaseDurations = {PHASE_DURATIONS};
        let phaseStartTime = new Date();

        function formatTime(seconds) {{
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = seconds % 60;
            
            if (hours > 0) {{
                return `${{String(hours).padStart(2, '0')}}:${{String(minutes).padStart(2, '0')}}:${{String(secs).padStart(2, '0')}}`;
            }}
            return `${{String(minutes).padStart(2, '0')}}:${{String(secs).padStart(2, '0')}}`;
        }}

        function updateIncidentTimer() {{
            if (!startTime || startTime == "Invalid Date") return;
            
            const now = new Date();
            const diff = Math.floor((now - startTime) / 1000);
            
            const hours = Math.floor(diff / 3600);
            const minutes = Math.floor((diff % 3600) / 60);
            const seconds = diff % 60;
            
            const formattedTime = 
                String(hours).padStart(2, '0') + ':' +
                String(minutes).padStart(2, '0') + ':' +
                String(seconds).padStart(2, '0');
            
            document.getElementById('timer').innerText = formattedTime;
        }}

        function updatePhaseTimer() {{
            if (!startTime || startTime == "Invalid Date") return;
            
            const now = new Date();
            const phaseDuration = phaseDurations[currentPhase];
            const elapsedSeconds = Math.floor((now - phaseStartTime) / 1000);
            const remainingSeconds = Math.max(0, phaseDuration - elapsedSeconds);
            
            document.getElementById('phase-timer').innerText = formatTime(remainingSeconds);
            
            // If time's up, notify Streamlit
            if (remainingSeconds === 0) {{
                // Use window.streamlitPython to communicate with Streamlit
                if (typeof window.streamlitPython !== 'undefined') {{
                    window.streamlitPython.setComponentValue({{
                        phase_completed: true,
                        current_phase: currentPhase
                    }});
                }}
            }}
        }}
        
        // Update both timers
        if (startTime && startTime != "Invalid Date") {{
            updateIncidentTimer();
            updatePhaseTimer();
            setInterval(updateIncidentTimer, 1000);
            setInterval(updatePhaseTimer, 1000);
        }}
    </script>
    """
    
    return cards_html

def create_timer_app():
    # st.set_page_config(page_title="Incident Timer", layout="wide")
    initialize_session_state()
    
    # Start/Stop Incident and Next Phase buttons
    col1, col2, col3 = st.columns([5, 1, 1])
    with col1:
        if not st.session_state.incident_active:
            if st.button("Start Incident"):
                st.session_state.incident_active = True
                st.session_state.start_time = datetime.now()
                st.session_state.current_phase = 1
                st.session_state.current_phase_start = datetime.now()
                st.experimental_rerun()
    
    with col2:
        if st.session_state.incident_active:
            if st.button("Next Phase"):
                if st.session_state.current_phase < 4:  # Max 4 phases
                    # Record end of current phase
                    update_phase_history(st.session_state.current_phase, datetime.now())
                    # Move to next phase
                    st.session_state.current_phase += 1
                    st.session_state.current_phase_start = datetime.now()
                    st.experimental_rerun()
    
    with col3:
        if st.session_state.incident_active:
            # Export button
            df = export_phase_data()
            if df is not None:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Export Phases",
                    data=csv,
                    file_name=f"incident_phases_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime='text/csv'
                )
    
    # Create and display status cards
    cards_html = create_status_cards()
    components.html(cards_html, height=150)
    
    # Display phase history table if available
    if st.session_state.phase_history:
        st.markdown("### Phase History")
        df = export_phase_data()
        if df is not None:
            st.dataframe(df)

if __name__ == "__main__":
    create_timer_app()
