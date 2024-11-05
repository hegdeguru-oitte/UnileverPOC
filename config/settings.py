# config/settings.py
import os
import logging
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.DEFAULT_RECIPIENTS = os.getenv("RECIPIENTS_EMAILS", "").split(",")
        
        if not self.OPENAI_API_KEY:
            logging.error("Missing required environment variables")
            raise ValueError("Missing required environment variables")
