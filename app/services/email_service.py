"""Email service for sending OTPs via SendGrid API"""

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from app.config import settings
import logging

logger = logging.getLogger(__name__)


def send_otp_email(email: str, otp_code: str) -> bool:
    """
    Send OTP to user's email via SendGrid API.
    
    Args:
        email: Recipient email address
        otp_code: 6-digit OTP code
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Check if SendGrid credentials are configured
        if not settings.SENDGRID_API_KEY or not settings.SENDGRID_FROM_EMAIL:
            logger.error("SendGrid credentials not configured in .env")
            logger.error("Required: SENDGRID_API_KEY and SENDGRID_FROM_EMAIL")
            return False
        
        # Create SendGrid client
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        
        # Email subject and sender
        subject = "Password Reset OTP - Brain Tumor MRI Analyzer"
        from_email = Email(settings.SENDGRID_FROM_EMAIL)
        to_email = To(email)
        
        # HTML email template
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <h2 style="color: #333; text-align: center;">Password Reset Request</h2>
                    
                    <p style="color: #666; font-size: 16px;">Hello,</p>
                    
                    <p style="color: #666; font-size: 16px;">
                        We received a request to reset your password for your Brain Tumor MRI Analyzer account. 
                        If you didn't make this request, please ignore this email.
                    </p>
                    
                    <p style="color: #666; font-size: 16px;">
                        Your One-Time Password (OTP) to reset your password is:
                    </p>
                    
                    <div style="background-color: #f0f0f0; padding: 20px; border-radius: 5px; text-align: center; margin: 20px 0;">
                        <h1 style="color: #00a8e8; letter-spacing: 3px; margin: 0;">{otp_code}</h1>
                    </div>
                    
                    <p style="color: #666; font-size: 14px;">
                        <strong>⏰ This OTP will expire in 10 minutes.</strong>
                    </p>
                    
                    <p style="color: #666; font-size: 14px;">
                        To reset your password:
                    </p>
                    <ol style="color: #666; font-size: 14px;">
                        <li>Go to the password reset page</li>
                        <li>Enter your email address</li>
                        <li>Enter the OTP code above</li>
                        <li>Create a new password</li>
                    </ol>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <p style="color: #999; font-size: 12px; text-align: center;">
                        If you have any questions, please contact our support team.
                    </p>
                    
                    <p style="color: #999; font-size: 12px; text-align: center;">
                        <em>Brain Tumor MRI Analyzer - Powered by AI</em>
                    </p>
                </div>
            </body>
        </html>
        """
        
        # Create mail message
        mail = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        
        # Send email via SendGrid
        response = sg.send(mail)
        
        # Check response status
        if response.status_code in [200, 201, 202]:
            logger.info(f"✅ OTP email sent successfully to {email}")
            return True
        else:
            logger.error(f"SendGrid API error: Status {response.status_code}")
            logger.error(f"Response body: {response.body}")
            return False
        
    except Exception as e:
        logger.error(f"Error sending OTP email via SendGrid: {str(e)}")
        return False
