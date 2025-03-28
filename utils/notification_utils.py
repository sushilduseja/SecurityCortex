import os
import logging
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_sms_notification(phone_number, message):
    """
    Send an SMS notification using Twilio.
    
    Args:
        phone_number (str): The recipient's phone number including country code (e.g., +15551234567)
        message (str): The message to send
        
    Returns:
        dict: Result with status and details
    """
    # Get Twilio credentials from environment variables
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    twilio_phone = os.environ.get("TWILIO_PHONE_NUMBER")
    
    # Check if Twilio credentials are configured
    if not all([account_sid, auth_token, twilio_phone]):
        logger.error("Twilio credentials not properly configured")
        return {
            "success": False,
            "message": "Twilio credentials not properly configured. Please ensure TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER are set."
        }
    
    # Ensure phone number is properly formatted
    if not phone_number.startswith('+'):
        phone_number = f"+{phone_number}"
    
    try:
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Send SMS
        sms = client.messages.create(
            body=message,
            from_=twilio_phone,
            to=phone_number
        )
        
        logger.info(f"SMS notification sent successfully. SID: {sms.sid}")
        return {
            "success": True,
            "message": "SMS notification sent successfully",
            "sid": sms.sid
        }
        
    except TwilioRestException as e:
        logger.error(f"Twilio error: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to send SMS: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error while sending SMS: {str(e)}")
        return {
            "success": False,
            "message": f"An unexpected error occurred: {str(e)}"
        }


def format_compliance_alert_message(monitor_data):
    """
    Format a compliance alert message for SMS notification.
    
    Args:
        monitor_data (dict): Data about the compliance monitor
        
    Returns:
        str: Formatted message
    """
    alert_level = monitor_data.get('alert_level', 'Unknown')
    monitor_name = monitor_data.get('name', 'Unknown Monitor')
    model = monitor_data.get('model_or_system', 'Unknown System')
    current_value = monitor_data.get('current_value', 0.0)
    threshold = monitor_data.get('threshold_value', 0.0)
    
    # Create message based on alert level
    if alert_level == 'Critical':
        urgency = "CRITICAL ALERT"
    elif alert_level == 'Warning':
        urgency = "WARNING"
    else:
        urgency = "NOTIFICATION"
        
    message = (
        f"{urgency}: AI Governance Dashboard\n\n"
        f"Monitor: {monitor_name}\n"
        f"System: {model}\n"
        f"Current Value: {current_value}\n"
        f"Threshold: {threshold}\n"
        f"Status: {alert_level}\n\n"
        f"Please review this issue in the AI Governance Dashboard."
    )
    
    return message


def format_risk_assessment_message(assessment_data):
    """
    Format a risk assessment message for SMS notification.
    
    Args:
        assessment_data (dict): Data about the risk assessment
        
    Returns:
        str: Formatted message
    """
    model_name = assessment_data.get('model_name', 'Unknown Model')
    risk_score = assessment_data.get('risk_score', 0.0)
    
    # Determine risk level
    if risk_score >= 75:
        risk_level = "HIGH RISK"
    elif risk_score >= 50:
        risk_level = "MEDIUM RISK"
    else:
        risk_level = "LOW RISK"
    
    # Format recommendations
    recommendations = assessment_data.get('recommendations', 'No recommendations provided.')
    if len(recommendations) > 100:
        # Truncate long recommendations for SMS
        recommendations = recommendations[:97] + "..."
    
    message = (
        f"RISK ASSESSMENT: {risk_level}\n\n"
        f"Model: {model_name}\n"
        f"Risk Score: {risk_score}\n\n"
        f"Key Recommendation: {recommendations}\n\n"
        f"View complete assessment in the AI Governance Dashboard."
    )
    
    return message