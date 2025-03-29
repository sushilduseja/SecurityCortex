"""
API endpoints for notification functionality
"""
from flask import Blueprint, jsonify, request
from datetime import datetime

from app.infrastructure.messaging.notification_service import NotificationService
from app.infrastructure.logging.error_handler import handle_exceptions
from app.domain.models import Activity

# Initialize services
notification_service = NotificationService()

def register_notification_routes(app):
    """
    Register notification-related routes with the Flask app
    
    Args:
        app: The Flask application
    """
    notification_bp = Blueprint('notification', __name__, url_prefix='/api/notifications')
    
    @notification_bp.route('/send', methods=['POST'])
    @handle_exceptions
    def send_notification():
        """
        Send a notification via SMS
        """
        data = request.json
        
        # Validate required fields
        required_fields = ['recipient', 'subject', 'body']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        recipient = data['recipient']
        subject = data['subject']
        body = data['body']
        notification_type = data.get('notification_type', 'general')
        urgency = data.get('urgency', 'normal')
        
        # Send the notification
        if notification_type == 'compliance':
            success = notification_service.send_compliance_alert(
                recipient=recipient,
                monitor_name=subject,
                current_value=data.get('current_value', 'N/A'),
                threshold_value=data.get('threshold_value', 'N/A'),
                urgency=urgency
            )
        elif notification_type == 'risk_assessment':
            success = notification_service.send_risk_assessment_notification(
                recipient=recipient,
                model_name=data.get('model_name', subject),
                risk_score=float(data.get('risk_score', 0.5)),
                findings_summary=body,
                urgency=urgency
            )
        elif notification_type == 'governance':
            success = notification_service.send_governance_notification(
                recipient=recipient,
                subject=subject,
                body=body,
                urgency=urgency
            )
        else:
            # Generic notification
            success = notification_service.send_alert(
                recipient=recipient,
                subject=subject,
                body=body,
                alert_type=notification_type,
                urgency=urgency
            )
        
        # Log the activity
        try:
            # If we had a proper database setup, we would log this activity
            activity = Activity(
                activity_type="notification",
                description=f"Sent {notification_type} notification: {subject}",
                created_at=datetime.now(),
                actor="system",
                related_entity_type=notification_type
            )
            print(f"Activity would be logged: {activity.__dict__}")
        except Exception as e:
            print(f"Error logging activity: {str(e)}")
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Notification sent successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to send notification'
            }), 500
    
    @notification_bp.route('/test', methods=['GET'])
    @handle_exceptions
    def test_notification():
        """
        Test endpoint to verify notification service is working
        """
        return jsonify({
            'success': True,
            'message': 'Notification API is working correctly',
            'has_twilio_credentials': all([
                notification_service.sms_provider.account_sid,
                notification_service.sms_provider.auth_token,
                notification_service.sms_provider.from_number
            ]) if hasattr(notification_service.sms_provider, 'account_sid') else False
        })
            
    app.register_blueprint(notification_bp)