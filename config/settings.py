# config/settings.py
import os
import logging
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Application configuration settings loaded from environment variables.
    
    Attributes:
        OPENAI_API_KEY (str): OpenAI API authentication key
        GROQ_API_KEY (str): GROQ API authentication key
        DEFAULT_RECIPIENTS (list): Default email recipients for notifications
        
    Raises:
        ValueError: If required environment variables are missing
    """
    def __init__(self):
        """Initialize settings from environment variables."""
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.DEFAULT_RECIPIENTS = os.getenv("RECIPIENTS_EMAILS", "").split(",")
        
        if not self.OPENAI_API_KEY:
            logging.error("Missing required OPENAI_API_KEY environment variable")
            raise ValueError("Missing required OPENAI_API_KEY environment variable")
        if not self.GROQ_API_KEY:
            logging.error("Missing required GROQ_API_KEY environment variable")
            raise ValueError("Missing required GROQ_API_KEY environment variable")
