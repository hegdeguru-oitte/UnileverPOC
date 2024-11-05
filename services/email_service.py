# services/email_service.py
import pythoncom
import win32com.client as win32
import logging

class EmailService:
    @staticmethod
    def generate_email_html(incident_data):
        try:
            html_content = f"""[Your existing HTML template]"""
            return html_content
        except Exception as e:
            logging.error(f"Error generating email HTML: {e}")
            raise

    @staticmethod
    def send_email(recipient_list, subject, html_content):
        try:
            pythoncom.CoInitialize()
            outlook = win32.Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            mail.To = "; ".join(recipient_list)
            mail.Subject = subject
            mail.HTMLBody = html_content
            mail.Send()
            logging.info("Email sent successfully via Outlook")
        except Exception as e:
            logging.error(f"Error sending email via Outlook: {e}")
            raise
