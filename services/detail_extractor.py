# services/detail_extractor.py
import openai
import json
import logging

class IncidentDetailExtractor:
    def __init__(self, api_key):
        openai.api_key = api_key

    def extract_detailed_issue_info(self, transcript):
            """Extract detailed issue information from transcript using OpenAI."""
            system_content = """You are an expert at analyzing incident management data.
            "issue_id", "issue_location", "participants" must contain exact values only. Do not mention in sentences. If values are not available in transcript, mention 'Not Available'.
            Extract the following details from the provided transcript in valid JSON format:
            {
                "issue_id": "Unique Issue ID",
                "issue_location": "Location of the issue",
                "issue_description": {
                    "business_impact": "Business impact details",
                    "affected_location": "Affected location and user count",
                    "ticket_number": "Related ticket number",
                    "service_offering": "Service impacted",
                    "financial_sales_loss": "Details of potential loss",
                    "business_working_hours": "Business hours affected",
                    "workaround_available": "Is a workaround available?"
                },
                "actions_taken": ["Step-by-step actions taken to resolve issue"],
                "participants": ["List of all participants with roles"],
                "additional_info": ["List any additional information"]
            }"""

            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": transcript}
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                detailed_data = json.loads(response.choices[0].message.content)
                return detailed_data
            except Exception as e:
                logging.error(f"Error extracting detailed issue information: {e}")
                return None