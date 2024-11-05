# services/email_service.py
import pythoncom
import win32com.client as win32
import logging

class EmailService:
    @staticmethod
    def generate_email_html(incident_data):
        """
        Generates HTML email content from incident data.
        
        Args:
            incident_data (dict): Structured incident information
            
        Returns:
            str: Formatted HTML content for email
            
        Raises:
            Exception: If template generation fails
        """
        try:
            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2 style="color: #d9534f;">Major Incident Notification</h2>
                    <div style="margin: 20px 0;">
                        <strong>Incident ID:</strong> {incident_data.get('incident_id', 'N/A')}<br>
                        <strong>Status:</strong> {incident_data.get('status', 'N/A')}<br>
                        <strong>Short Description:</strong> {incident_data.get('short_description', 'N/A')}<br>
                        <strong>Outage Time:</strong> {incident_data.get('outage_time', 'N/A')}<br>
                        <strong>Business Impact:</strong> {incident_data.get('business_impact', 'N/A')}
                    </div>
                    <div style="margin: 20px 0;">
                        <h3>Bridge Details</h3>
                        <p>{incident_data.get('bridge_details', {}).get('platform', 'N/A')}<br>
                        Meeting ID: {incident_data.get('bridge_details', {}).get('meeting_id', 'N/A')}<br>
                        Passcode: {incident_data.get('bridge_details', {}).get('passcode', 'N/A')}</p>
                    </div>
                    <div style="margin: 20px 0;">
                        <strong>Next Update:</strong> {incident_data.get('next_update', 'N/A')}
                    </div>
                </body>
            </html>
            """
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
