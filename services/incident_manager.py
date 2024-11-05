# services/incident_manager.py
import docx
import openai
import json
import logging
from config.settings import Settings

class IncidentManager:
    """
    Manages incident processing, document reading, and OpenAI API interactions.
    
    This class handles the core functionality of processing incident reports,
    including reading DOCX files and extracting structured information using OpenAI.
    """

    def __init__(self):
        """
        Initialize the IncidentManager with OpenAI API settings.
        
        Raises:
            ValueError: If required environment variables are missing
        """
        self.settings = Settings()
        openai.api_key = self.settings.OPENAI_API_KEY

    def read_docx(self, file):
        """
        Read and extract text content from a DOCX file.
        
        Args:
            file: A file-like object containing a DOCX document
            
        Returns:
            str: Concatenated text content from the document
            
        Raises:
            Exception: If there's an error reading the DOCX file
        """
        try:
            doc = docx.Document(file)
            full_text = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    full_text.append(paragraph.text)
            return "\n".join(full_text)
        except Exception as e:
            logging.error(f"Error reading DOCX file: {e}")
            raise

    def call_openai_api(self, system_content, user_content):
        """
        Make a call to OpenAI's API for text processing.
        
        Args:
            system_content (str): Instructions for the AI model
            user_content (str): The actual content to be processed
            
        Returns:
            str: The processed response from OpenAI
            
        Raises:
            Exception: If there's an error calling the OpenAI API
        """
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            raise

    def extract_incident_details(self, transcript):
        """
        Extract structured incident details from a transcript using OpenAI.
        
        Args:
            transcript (str): The incident transcript text
            
        Returns:
            dict: Structured incident data including ID, status, description, etc.
            
        Raises:
            Exception: If there's an error in extraction or JSON parsing
        """
        system_content = """You are an expert at extracting incident management information. 
        Extract the following details from the provided transcript and return them in valid JSON format:
        {
            "incident_id": "ID number",
            "status": "MAJOR INCIDENT",
            "short_description": "Brief description",
            "outage_time": "Time in UTC",
            "mim_notified_time": "Time in UTC",
            "reported_by": "Name and role",
            "description": "Incident description",
            "business_impact": "Business impact description",
            "impacted_services": ["List", "of", "impacted", "services"],
            "next_update": "Time in UTC",
            "bridge_details": {
                "platform": "e.g. Zoom",
                "meeting_id": "Meeting ID",
                "passcode": "Passcode"
            },
            "resolution_teams": ["List of teams involved in the resolution"]
        }"""

        try:
            json_response = self.call_openai_api(system_content, transcript)
            incident_data = json.loads(json_response)
            return incident_data
        except Exception as e:
            logging.error(f"Error extracting incident details: {e}")
            raise
