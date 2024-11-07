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
