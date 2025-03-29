"""
Centralized error handling for the application
"""
import logging
import functools
import traceback
from flask import jsonify, current_app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AppError(Exception):
    """Base exception class for application-specific errors"""
    
    def __init__(self, message, status_code=500, details=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        
    def to_dict(self):
        """Convert the exception to a dictionary for JSON responses"""
        return {
            'error': self.message,
            'status_code': self.status_code,
            'details': self.details
        }
        
class ValidationError(AppError):
    """Exception for validation errors"""
    
    def __init__(self, message, details=None):
        super().__init__(message, status_code=400, details=details)
        
class NotFoundError(AppError):
    """Exception for resource not found errors"""
    
    def __init__(self, message, details=None):
        super().__init__(message, status_code=404, details=details)
        
class AuthorizationError(AppError):
    """Exception for authorization errors"""
    
    def __init__(self, message, details=None):
        super().__init__(message, status_code=403, details=details)

def handle_exceptions(f):
    """
    Decorator to handle exceptions in Flask routes
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AppError as e:
            logger.error(f"Application error: {str(e)}")
            return jsonify(e.to_dict()), e.status_code
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                'error': 'An unexpected error occurred',
                'status_code': 500,
                'details': {
                    'message': str(e),
                    'type': e.__class__.__name__
                }
            }), 500
    return decorated_function

def configure_error_handlers(app):
    """
    Configure error handlers for the Flask application
    
    Args:
        app: The Flask application
    """
    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({
            'error': 'The requested resource was not found',
            'status_code': 404
        }), 404
        
    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify({
            'error': 'Bad request',
            'status_code': 400,
            'details': {
                'message': str(e)
            }
        }), 400
        
    @app.errorhandler(500)
    def handle_server_error(e):
        logger.error(f"Internal server error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': 'An internal server error occurred',
            'status_code': 500
        }), 500
        
    @app.errorhandler(403)
    def handle_forbidden(e):
        return jsonify({
            'error': 'Access forbidden',
            'status_code': 403
        }), 403
    
    logger.info("Error handlers configured successfully")