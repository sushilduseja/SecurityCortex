"""
Notification service implementation
"""
import os
import logging
from typing import Dict, List, Optional, Union
from datetime import datetime

from app.infrastructure.messaging.sms_provider import get_sms_provider, SmsProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationMessage:
    """
    DTO for notification messages
    """
    def __init__(
        self,
        recipient: str,
        subject: str,
        body: str,
        notification_type: str = "general",
        urgency: str = "normal",
        metadata: Optional[Dict] = None
    ):
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.notification_type = notification_type  # e.g., "alert", "info", "warning"
        self.urgency = urgency  # e.g., "low", "normal", "high", "critical"
        self.metadata = metadata or {}
        self.timestamp = datetime.now()

class NotificationService:
    """
    Notification service for sending alerts and notifications via various channels
    """
    def __init__(self, sms_provider: Optional[SmsProvider] = None):
        """
        Initialize the notification service
        
        Args:
            sms_provider: Optional SMS provider to use
        """
        self.sms_provider = sms_provider or get_sms_provider()
        
        # Notification preferences - in a real app, these would be loaded from a database
        self._notification_preferences = {
            "governance": {
                "channels": ["sms", "email"],
                "urgency_threshold": "normal",
            },
            "compliance": {
                "channels": ["sms", "email"],
                "urgency_threshold": "low",
            },
            "risk_assessment": {
                "channels": ["sms", "email"],
                "urgency_threshold": "high",
            },
        }
        
        # Load environment settings
        self.default_phone_number = os.environ.get('DEFAULT_NOTIFICATION_PHONE', '')
        self.notification_enabled = os.environ.get('NOTIFICATIONS_ENABLED', 'true').lower() == 'true'
        
        if not self.default_phone_number:
            logger.warning("No default notification phone number set in DEFAULT_NOTIFICATION_PHONE env var")
    
    def should_notify(self, message: NotificationMessage, preferences: Optional[Dict] = None) -> bool:
        """
        Determine if a notification should be sent based on preferences
        
        Args:
            message: The notification message
            preferences: Optional preferences to use instead of the defaults
            
        Returns:
            bool: True if the notification should be sent, False otherwise
        """
        if not self.notification_enabled:
            return False
            
        prefs = preferences or self._notification_preferences.get(
            message.notification_type, 
            {"channels": ["sms"], "urgency_threshold": "normal"}
        )
        
        # Map urgency levels to numeric values for comparison
        urgency_levels = {"low": 1, "normal": 2, "high": 3, "critical": 4}
        
        message_urgency = urgency_levels.get(message.urgency, 2)  # Default to normal
        threshold_urgency = urgency_levels.get(prefs.get("urgency_threshold", "normal"), 2)
        
        return message_urgency >= threshold_urgency
    
    def send_notification(self, message: NotificationMessage) -> bool:
        """
        Send a notification through appropriate channels
        
        Args:
            message: The notification message
            
        Returns:
            bool: True if the notification was sent successfully, False otherwise
        """
        if not self.should_notify(message):
            logger.info(f"Notification suppressed based on preferences: {message.subject}")
            return False
            
        recipient = message.recipient or self.default_phone_number
        
        if not recipient:
            logger.error("No recipient specified for notification and no default available")
            return False
        
        # Format message body with subject
        full_message = f"{message.subject}\n\n{message.body}"
        
        # Send via SMS
        return self.sms_provider.send_message(recipient, full_message)
    
    def send_alert(
        self, 
        recipient: str,
        subject: str,
        body: str,
        alert_type: str = "compliance",
        urgency: str = "high"
    ) -> bool:
        """
        Send an alert notification
        
        Args:
            recipient: The recipient's phone number
            subject: The alert subject
            body: The alert body text
            alert_type: The type of alert
            urgency: The urgency level
            
        Returns:
            bool: True if the alert was sent successfully, False otherwise
        """
        message = NotificationMessage(
            recipient=recipient,
            subject=subject,
            body=body,
            notification_type=alert_type,
            urgency=urgency,
            metadata={"is_alert": True}
        )
        
        return self.send_notification(message)
    
    def send_governance_notification(
        self,
        recipient: str,
        subject: str,
        body: str,
        urgency: str = "normal"
    ) -> bool:
        """
        Send a governance-related notification
        
        Args:
            recipient: The recipient's phone number
            subject: The notification subject
            body: The notification body text
            urgency: The urgency level
            
        Returns:
            bool: True if the notification was sent successfully, False otherwise
        """
        return self.send_alert(
            recipient=recipient,
            subject=subject,
            body=body, 
            alert_type="governance",
            urgency=urgency
        )
    
    def send_compliance_alert(
        self,
        recipient: str,
        monitor_name: str,
        current_value: Union[float, str],
        threshold_value: Union[float, str],
        urgency: str = "high"
    ) -> bool:
        """
        Send a compliance alert notification
        
        Args:
            recipient: The recipient's phone number
            monitor_name: The name of the compliance monitor
            current_value: The current value that triggered the alert
            threshold_value: The threshold value that was exceeded
            urgency: The urgency level
            
        Returns:
            bool: True if the alert was sent successfully, False otherwise
        """
        subject = f"Compliance Alert: {monitor_name}"
        body = (
            f"The compliance monitor '{monitor_name}' has triggered an alert.\n"
            f"Current value: {current_value}\n"
            f"Threshold: {threshold_value}\n\n"
            f"Please review this alert in the AI Governance Dashboard."
        )
        
        return self.send_alert(
            recipient=recipient,
            subject=subject,
            body=body, 
            alert_type="compliance",
            urgency=urgency
        )
    
    def send_risk_assessment_notification(
        self,
        recipient: str,
        model_name: str,
        risk_score: float,
        findings_summary: str,
        urgency: str = "high"
    ) -> bool:
        """
        Send a risk assessment notification
        
        Args:
            recipient: The recipient's phone number
            model_name: The name of the AI model
            risk_score: The risk score (higher is more risky)
            findings_summary: A summary of the findings
            urgency: The urgency level
            
        Returns:
            bool: True if the notification was sent successfully, False otherwise
        """
        risk_level = "Low"
        if risk_score > 0.7:
            risk_level = "High"
        elif risk_score > 0.4:
            risk_level = "Medium"
            
        subject = f"Risk Assessment: {model_name} - {risk_level} Risk"
        body = (
            f"A risk assessment for AI model '{model_name}' has been completed.\n"
            f"Risk Score: {risk_score:.2f} ({risk_level} Risk)\n\n"
            f"Summary: {findings_summary}\n\n"
            f"Please review the full assessment in the AI Governance Dashboard."
        )
        
        return self.send_alert(
            recipient=recipient,
            subject=subject,
            body=body, 
            alert_type="risk_assessment",
            urgency=urgency
        )