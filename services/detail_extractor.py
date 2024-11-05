# services/detail_extractor.py
import openai
import json
import logging

class IncidentDetailExtractor:
    """
    Extracts detailed incident information from transcripts using OpenAI.
    
    This class provides detailed extraction of incident information including:
    - Issue identification and location
    - Business impact analysis
    - Action tracking
    - Participant information
    
    Attributes:
        api_key (str): OpenAI API key for authentication
        
    Example:
        >>> extractor = IncidentDetailExtractor(api_key)
        >>> details = extractor.extract_detailed_issue_info("Incident report...")
        >>> print(details['issue_id'])
    """
    
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def extract_detailed_issue_info(self, transcript):
        """
        Extract structured incident details from transcript text.
        
        Args:
            transcript (str): Raw incident transcript
            
        Returns:
            dict: Structured incident data or None if extraction fails
        """
        template = {
            "issue_id": "ID",
            "issue_location": "Location",
            "issue_description": {
                "business_impact": "Impact details",
                "affected_location": "Location and users affected",
                "ticket_number": "Ticket ID",
                "service_offering": "Impacted service",
                "workaround_available": "Yes/No"
            },
            "actions_taken": ["Actions list"],
            "participants": ["Participant list"],
            "additional_info": ["Additional information items"]
        }

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Extract incident details in this JSON format: {json.dumps(template)}"},
                    {"role": "user", "content": transcript}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logging.error(f"Extraction failed: {e}")
            return None
