import os
from typing import Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def send_sms_notification(to_phone_number: str, message: str) -> dict:
    """
    Send an SMS notification using Twilio.
    
    Args:
        to_phone_number: The recipient's phone number in E.164 format (+1xxxxxxxxxx)
        message: The message content to send
        
    Returns:
        dict: A dictionary with success status and details
    """
    # Check if we have the required environment variables
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = os.environ.get("TWILIO_PHONE_NUMBER")
    
    if not all([account_sid, auth_token, from_number]):
        return {
            "success": False, 
            "error": "Twilio credentials not configured. Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER."
        }
    
    try:
        # Initialize the Twilio client
        client = Client(account_sid, auth_token)
        
        # Send the message
        message_obj = client.messages.create(
            body=message,
            from_=from_number,
            to=to_phone_number
        )
        
        return {
            "success": True,
            "message_id": message_obj.sid,
            "status": message_obj.status
        }
        
    except TwilioRestException as e:
        return {
            "success": False,
            "error": f"Twilio error: {str(e)}",
            "code": e.code
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error sending SMS: {str(e)}"
        }

def format_compliance_alert_message(monitor_name: str, 
                                    alert_level: str, 
                                    current_value: float, 
                                    threshold: float) -> str:
    """
    Format a compliance alert message.
    
    Args:
        monitor_name: Name of the compliance monitor
        alert_level: The alert level (Normal, Warning, Critical)
        current_value: Current value of the metric
        threshold: Threshold value
        
    Returns:
        str: Formatted message
    """
    return (
        f"AI Governance Alert: {monitor_name}\n"
        f"Alert Level: {alert_level}\n"
        f"Current Value: {current_value}\n"
        f"Threshold: {threshold}\n"
        f"Please check the AI Governance Dashboard for details."
    )

def format_risk_assessment_message(model_name: str, 
                                  risk_score: float, 
                                  status: str) -> str:
    """
    Format a risk assessment notification message.
    
    Args:
        model_name: Name of the AI model
        risk_score: The risk score (0-100)
        status: Assessment status
        
    Returns:
        str: Formatted message
    """
    risk_level = "Low"
    if risk_score >= 80:
        risk_level = "High"
    elif risk_score >= 60:
        risk_level = "Medium-High"
    elif risk_score >= 40:
        risk_level = "Medium"
    elif risk_score >= 20:
        risk_level = "Medium-Low"
    
    return (
        f"Risk Assessment Update: {model_name}\n"
        f"Risk Score: {risk_score} ({risk_level})\n"
        f"Status: {status}\n"
        f"Please review the full assessment on the AI Governance Dashboard."
    )