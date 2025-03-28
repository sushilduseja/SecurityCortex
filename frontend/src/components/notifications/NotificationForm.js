import React, { useState } from 'react';
import { sendSmsNotification } from '../../services/api';

const NotificationForm = ({ 
  entityType, 
  entityId,
  initialData = {}
}) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [notificationType, setNotificationType] = useState(initialData.notification_type || 'custom');
  const [alertResult, setAlertResult] = useState(null);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!phoneNumber.trim()) {
      setAlertResult({
        type: 'error',
        message: 'Please enter a valid phone number.'
      });
      return;
    }
    
    if (!message.trim()) {
      setAlertResult({
        type: 'error',
        message: 'Please enter a message to send.'
      });
      return;
    }
    
    setIsSubmitting(true);
    setAlertResult(null);
    
    try {
      const formattedNumber = formatPhoneNumber(phoneNumber);
      
      const response = await sendSmsNotification({
        phone_number: formattedNumber,
        message,
        entity_type: entityType,
        entity_id: entityId,
        notification_type: notificationType
      });
      
      setAlertResult({
        type: 'success',
        message: 'Notification sent successfully!'
      });
      
      // Reset form
      setMessage('');
      
    } catch (error) {
      console.error('Error sending notification:', error);
      setAlertResult({
        type: 'error',
        message: error.message || 'Failed to send notification. Please try again.'
      });
    } finally {
      setIsSubmitting(false);
    }
  };
  
  // Format phone number to E.164 format
  const formatPhoneNumber = (number) => {
    // Remove any non-digit characters
    const digitsOnly = number.replace(/\D/g, '');
    
    // Ensure it has the international prefix (+)
    if (!number.startsWith('+')) {
      // If no country code, assume US (+1)
      if (digitsOnly.length === 10) {
        return `+1${digitsOnly}`;
      }
      return `+${digitsOnly}`;
    }
    
    return number;
  };
  
  // Generate template messages based on notification type
  const generateTemplateMessage = (type) => {
    switch(type) {
      case 'compliance_alert':
        return 'ALERT: Compliance monitor "Critical Data Processing" has triggered a WARNING alert. Current value: 78.5%, Threshold: 85%. Please review immediately.';
      case 'risk_assessment':
        return 'NOTIFICATION: Risk assessment for "Recommendation Engine v2" has been completed. Risk Score: 65/100 (Medium). 3 high priority findings require attention.';
      case 'policy_update':
        return 'UPDATE: Governance policy "Data Retention Policy" has been updated. Please review the changes and acknowledge compliance by EOD.';
      default:
        return '';
    }
  };
  
  const handleTypeChange = (e) => {
    const type = e.target.value;
    setNotificationType(type);
    
    if (type !== 'custom') {
      setMessage(generateTemplateMessage(type));
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {alertResult && (
        <div className={`alert alert-${alertResult.type === 'success' ? 'success' : 'danger'} mb-4`}>
          {alertResult.message}
        </div>
      )}
      
      <div className="mb-4">
        <label htmlFor="notificationType" className="form-label">Notification Type</label>
        <select 
          id="notificationType" 
          className="form-select" 
          value={notificationType}
          onChange={handleTypeChange}
        >
          <option value="custom">Custom Message</option>
          <option value="compliance_alert">Compliance Alert</option>
          <option value="risk_assessment">Risk Assessment</option>
          <option value="policy_update">Policy Update</option>
        </select>
      </div>
      
      <div className="mb-4">
        <label htmlFor="phoneNumber" className="form-label">Recipient Phone Number</label>
        <input 
          type="text" 
          className="form-control" 
          id="phoneNumber" 
          placeholder="+1 (555) 123-4567"
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          required
        />
        <div className="form-text">
          Enter phone number in international format (e.g., +1 555 123 4567)
        </div>
      </div>
      
      <div className="mb-4">
        <label htmlFor="message" className="form-label">Message</label>
        <textarea 
          className="form-control" 
          id="message" 
          rows="5"
          placeholder="Enter the notification message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          required
        ></textarea>
        <div className="form-text">
          {message.length}/160 characters {message.length > 160 ? '(may be sent as multiple messages)' : ''}
        </div>
      </div>
      
      <div className="d-grid gap-2">
        <button 
          type="submit" 
          className="btn btn-primary" 
          disabled={isSubmitting}
        >
          {isSubmitting ? (
            <>
              <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Sending...
            </>
          ) : (
            'Send Notification'
          )}
        </button>
      </div>
    </form>
  );
};

export default NotificationForm;