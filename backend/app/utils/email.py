"""
utils/email.py — SendGrid-based email utility functions for visitor notifications and badge delivery.
"""

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from app.logger_config import setup_logger

# Load environment variables and initialize logger
load_dotenv()
logger = setup_logger()

# Email Configuration
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_visitor_notification(to_email: str, visitor_name: str, purpose: str) -> int | None:
    """
    Sends an approval request email to the host employee when a visitor registers.

    Args:
        to_email (str): Host employee's email address.
        visitor_name (str): Name of the registered visitor.
        purpose (str): Purpose of the visit.

    Returns:
        int | None: HTTP status code if sent successfully, None otherwise.
    """
    if not SENDGRID_API_KEY or not FROM_EMAIL:
        logger.error("❌ SendGrid API key or FROM_EMAIL is not configured.")
        return None

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject="🔔 New Visitor Approval Request",
        html_content=f"""
            <div style="font-family: Arial, sans-serif; font-size: 15px; color: #333;">
                <p><strong>New Visitor Registered</strong></p>
                <p>
                    <b>Name:</b> {visitor_name}<br>
                    <b>Purpose:</b> {purpose}
                </p>
                <p>Please log in to your dashboard to approve or reject this request.</p>
                <p>Regards,<br><b>Visitor Management System</b></p>
            </div>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"📧 Visitor request email sent to {to_email} — status {response.status_code}")
        return response.status_code
    except Exception as e:
        logger.error(f"❌ Error sending approval email to {to_email}: {e}")
        return None

def send_badge_email(to_email: str, visitor_name: str, badge_url: str) -> int | None:
    """
    Sends the visitor their QR badge via email after pre-approval.

    Args:
        to_email (str): Visitor's email address.
        visitor_name (str): Visitor's name.
        badge_url (str): URL to the hosted QR badge.

    Returns:
        int | None: HTTP status code if sent successfully, None otherwise.
    """
    if not SENDGRID_API_KEY or not FROM_EMAIL:
        logger.error("❌ SendGrid API key or FROM_EMAIL is not configured.")
        return None

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject="🪪 Your Visitor QR Badge",
        html_content=f"""
            <div style="font-family: Arial, sans-serif; font-size: 15px; color: #333;">
                <p><strong>Hello {visitor_name},</strong></p>
                <p>
                    You have been pre-approved for a visit. Please present the QR badge below at the security checkpoint.
                </p>
                <img src="{badge_url}" alt="Visitor Badge" style="width: 200px; margin: 15px 0;">
                <p>This badge is valid only for your approved time window.</p>
                <p>Thank you,<br><b>Visitor Management System</b></p>
            </div>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"📧 Badge email sent to {to_email} — status {response.status_code}")
        return response.status_code
    except Exception as e:
        logger.error(f"❌ Error sending badge email to {to_email}: {e}")
        return None
