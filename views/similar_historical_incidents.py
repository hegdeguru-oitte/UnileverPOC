import streamlit as st
from History.Similar_Incidents3 import EnhancedIncidentAnalysisSystem
from config.settings import Settings

def show():
    st.title("🔍 Similar Historical Incidents")

    if 'detailed_issue_info' in st.session_state:
        # Concatenate detailed issue info into a single string
        incident_description = " ".join(
            f"{key}: {value}" for key, value in st.session_state.detailed_issue_info.items()
        )

        # Initialize the analysis system
        analysis_system = EnhancedIncidentAnalysisSystem(
            groq_api_key=Settings().GROQ_API_KEY    ,
            historical_incidents_file=r'C:\Users\gurhegde\OneDrive - Deloitte (O365D)\CAI Playground\Pratik-Tasks\Unilever POC\Integration 1.2\History\Incidents_4X3.xlsx'
        )

        # Perform analysis
        # EnhancedIncidentAnalysisSystem.delete_all_data()
        result = analysis_system.analyze_incident(incident_description)

        # Display root cause analysis
        st.subheader("Root Cause Analysis")
        for key, value in result['current_incident']['analysis'].items():
            st.markdown(f"**{key}:** {value}")

        # Display similar incidents
        st.subheader("Similar Incidents")
        for incident in result['similar_incidents']:
            st.markdown(f"**Incident ID:** {incident['incident_id']}")
            st.markdown(f"**Similarity Score:** {incident['similarity_score']}")
            st.markdown(f"**Description:** {incident['description']}")
            st.markdown(f"**Actions Taken:** {incident['actions_taken']}")
            st.markdown(f"**Participants:** {incident['participants']}")
            st.markdown("---")

        # Export button
        if st.button("Export Analysis"):
            # Convert result to a downloadable format
            st.download_button(
                label="Download Analysis",
                data=str(result),
                file_name="similar_incidents_analysis.txt",
                mime="text/plain"
            )
    else:
        st.warning("Please process an incident document first.")
import streamlit as st
from services.incident_manager import IncidentManager
from History.Similar_Incidents3 import EnhancedIncidentAnalysisSystem
from ui.components import display_incident_details

def show():
    st.title("🔍 Similar Historical Incidents")

    # Initialize the incident analysis system
    analysis_system = EnhancedIncidentAnalysisSystem()

    # Input for incident description
    incident_description = st.text_area("Describe the current incident", height=150)

    if st.button("Analyze Incident"):
        if incident_description:
            with st.spinner("Analyzing..."):
                result = analysis_system.analyze_incident(incident_description)

                # Display root cause analysis
                st.subheader("Root Cause Analysis")
                root_cause = result['current_incident']['analysis']
                st.markdown(f"""
                    <div class="card">
                        <h4>Category: {root_cause.get('CATEGORY', 'N/A')}</h4>
                        <p><strong>Root Cause:</strong> {root_cause.get('ROOT_CAUSE', 'N/A')}</p>
                        <p><strong>Impact Level:</strong> {root_cause.get('IMPACT', 'N/A')}</p>
                        <p><strong>Component:</strong> {root_cause.get('COMPONENT', 'N/A')}</p>
                        <p><strong>Solution:</strong> {root_cause.get('SOLUTION', 'N/A')}</p>
                        <p><strong>Prevention:</strong> {root_cause.get('PREVENTION', 'N/A')}</p>
                    </div>
                """, unsafe_allow_html=True)

                # Display similar incidents
                st.subheader("Similar Incidents")
                for incident in result['similar_incidents']:
                    st.markdown(f"""
                        <div class="card">
                            <h4>Incident ID: {incident['incident_id']}</h4>
                            <p><strong>Similarity Score:</strong> {incident['similarity_score']}%</p>
                            <p><strong>Description:</strong> {incident['description']}</p>
                            <p><strong>Actions Taken:</strong> {incident['actions_taken']}</p>
                            <p><strong>Participants:</strong> {incident['participants']}</p>
                        </div>
                    """, unsafe_allow_html=True)

                # Export button
                if st.button("Export Analysis Results"):
                    st.success("Analysis results exported successfully!")
        else:
            st.warning("Please enter an incident description to analyze.")
