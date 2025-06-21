import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.logger_config import setup_logger
from dotenv import load_dotenv

logger = setup_logger()
load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_visitor_notification(to_email: str, visitor_name: str, purpose: str) -> int | None:
    if not SENDGRID_API_KEY or not FROM_EMAIL:
        logger.error("SendGrid API key or FROM_EMAIL is not configured.")
        return None
    
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject="New visitor Approval Request",
        html_content=f"""
            <div style="font-family: Arial, sans-serif; font-size: 15px; color: #333;">
                <p><strong>New visitor registered</strong></p>
                <p><b>Name:</b> {visitor_name}<br>
                <b>Purpose:</b> {purpose}</p>
                <p>Please login to your dashboard to approve or reject this visitor.</p>
                <p>Regards,<br><b>Visitor Management System</b></p>
            </div>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"Email sent to {to_email} - status: {response.status_code}")
        return response.status_code
    except Exception as e:
        logger.error(f"Error sending email to {to_email}: {e}")
        return None
    
def send_badge_email(to_email: str, visitor_name: str, badge_url: str):
    if not SENDGRID_API_KEY or not FROM_EMAIL:
        logger.error("SendGrid API key or FROM_EMAIL is not configured.")
        return None
    
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject="Your Visitor QR badge",
        html_content=f"""
            <strong>Hello {visitor_name},</strong><br><br>
            You have been pre-approved for your visit.<br>
            Please use the QR code below for entry:<br><br>
            <img src="{badge_url}" alt="Visitor Badge" style="width:200px;"><br><br>
            This badge is valid only for your scheduled time window.
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"Email sent to {to_email} - status: {response.status_code}")
        return response.status_code
    except Exception as e:
        logger.error(f"Error sending badge email: {e}")
        return None