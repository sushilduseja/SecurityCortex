"""
SMS Provider implementation using Twilio
"""
import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SmsProvider:
    """
    Base SMS provider interface
    """
    def send_message(self, to_number: str, message: str) -> bool:
        """
        Send an SMS message
        
        Args:
            to_number: The recipient's phone number
            message: The message content
            
        Returns:
            bool: True if the message was sent successfully, False otherwise
        """
        raise NotImplementedError("Subclasses must implement send_message")

class TwilioSmsProvider(SmsProvider):
    """
    Twilio implementation of the SMS provider
    """
    def __init__(self):
        """Initialize the Twilio SMS provider"""
        try:
            from twilio.rest import Client
            
            # Get Twilio credentials from environment variables
            self.account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
            self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
            self.from_number = os.environ.get('TWILIO_PHONE_NUMBER')
            
            if not all([self.account_sid, self.auth_token, self.from_number]):
                logger.warning("Twilio credentials are not properly configured")
                self.client = None
            else:
                self.client = Client(self.account_sid, self.auth_token)
                logger.info("Twilio SMS provider initialized successfully")
        except ImportError:
            logger.error("Twilio package is not installed")
            self.client = None
    
    def send_message(self, to_number: str, message: str) -> bool:
        """
        Send an SMS message using Twilio
        
        Args:
            to_number: The recipient's phone number in E.164 format (+1XXXXXXXXXX)
            message: The message content
            
        Returns:
            bool: True if the message was sent successfully, False otherwise
        """
        if not self.client:
            logger.error("Twilio client is not initialized. Check your credentials.")
            return False
        
        try:
            # Format the number to E.164 format if not already formatted
            if not to_number.startswith('+'):
                to_number = f"+1{to_number}"  # Assuming US numbers by default
            
            # Send the SMS message
            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            logger.info(f"Message sent with SID: {message_obj.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending SMS message: {str(e)}")
            return False

class MockSmsProvider(SmsProvider):
    """
    Mock implementation of the SMS provider for testing
    """
    def send_message(self, to_number: str, message: str) -> bool:
        """
        Simulate sending an SMS message
        
        Args:
            to_number: The recipient's phone number
            message: The message content
            
        Returns:
            bool: Always returns True
        """
        logger.info(f"MOCK SMS to {to_number}: {message}")
        return True

def get_sms_provider() -> SmsProvider:
    """
    Factory function to get the appropriate SMS provider based on configuration
    
    Returns:
        SmsProvider: An instance of an SMS provider
    """
    if os.environ.get('USE_MOCK_SMS', '').lower() == 'true':
        return MockSmsProvider()
    
    return TwilioSmsProvider()