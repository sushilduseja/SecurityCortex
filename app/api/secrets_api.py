"""
API endpoints for managing API keys and secrets
"""
import os
from flask import Blueprint, jsonify, request
import logging
from app.infrastructure.logging.error_handler import handle_exceptions

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of allowed secrets that can be checked and managed
ALLOWED_SECRETS = [
    'TWILIO_ACCOUNT_SID', 
    'TWILIO_AUTH_TOKEN', 
    'TWILIO_PHONE_NUMBER',
    'DEFAULT_NOTIFICATION_PHONE'
]

def register_secrets_routes(app):
    """
    Register secret management routes with the Flask app
    
    Args:
        app: The Flask application
    """
    secrets_bp = Blueprint('secrets', __name__, url_prefix='/api/secrets')
    
    @secrets_bp.route('/status', methods=['GET'])
    @handle_exceptions
    def get_secrets_status():
        """
        Get the status of required secrets (whether they are set or not)
        """
        status = {}
        
        for secret_name in ALLOWED_SECRETS:
            # Only check if the secret is set, not its value
            status[secret_name] = {
                'is_set': bool(os.environ.get(secret_name)),
                'description': get_secret_description(secret_name)
            }
            
        return jsonify({
            'success': True,
            'data': status
        })
    
    @secrets_bp.route('/update', methods=['POST'])
    @handle_exceptions
    def update_secret():
        """
        Update a secret value
        """
        data = request.json
        
        # Validate required fields
        if 'name' not in data or 'value' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: name and value'
            }), 400
            
        secret_name = data['name'].strip()
        secret_value = data['value'].strip()
        
        # Validate that the secret is allowed to be set
        if secret_name not in ALLOWED_SECRETS:
            return jsonify({
                'success': False,
                'error': f'Secret {secret_name} is not allowed to be set via API'
            }), 403
        
        # Set the environment variable
        os.environ[secret_name] = secret_value
        
        logger.info(f"Secret {secret_name} has been updated")
        
        return jsonify({
            'success': True,
            'message': f'Secret {secret_name} has been updated'
        })
    
    app.register_blueprint(secrets_bp)

def get_secret_description(secret_name):
    """
    Get a description for a secret
    
    Args:
        secret_name: The name of the secret
        
    Returns:
        str: A description of the secret
    """
    descriptions = {
        'TWILIO_ACCOUNT_SID': 'Twilio Account SID for sending SMS notifications',
        'TWILIO_AUTH_TOKEN': 'Twilio Auth Token for authentication',
        'TWILIO_PHONE_NUMBER': 'Twilio phone number to send SMS from',
        'DEFAULT_NOTIFICATION_PHONE': 'Default phone number to send notifications to'
    }
    
    return descriptions.get(secret_name, 'No description available')