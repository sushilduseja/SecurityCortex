import React, { useState } from 'react';
import Modal from '../common/Modal';
import { sendSmsNotification } from '../../services/api';

const SmsNotificationModal = ({ show, onClose, entityType, entityId, entityData, notificationType }) => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [customMessage, setCustomMessage] = useState('');
  const [useCustomMessage, setUseCustomMessage] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  
  // Reset state when modal is opened
  React.useEffect(() => {
    if (show) {
      setPhoneNumber('');
      setCustomMessage('');
      setUseCustomMessage(false);
      setError(null);
      setSuccess(null);
    }
  }, [show]);
  
  const getDefaultTitle = () => {
    switch (notificationType) {
      case 'compliance_alert':
        return 'Send Compliance Alert';
      case 'risk_assessment':
        return 'Send Risk Assessment Alert';
      default:
        return 'Send SMS Notification';
    }
  };
  
  const getDefaultMessage = () => {
    switch (notificationType) {
      case 'compliance_alert':
        return `AI Governance Dashboard Alert: Compliance issue detected with monitor "${entityData?.name || 'Unknown'}" at alert level "${entityData?.alert_level || 'Warning'}"`;
      case 'risk_assessment':
        return `AI Governance Dashboard Alert: Risk assessment for model "${entityData?.model_name || 'Unknown'}" shows a risk score of ${entityData?.risk_score || '0'}.`;
      default:
        return 'AI Governance Dashboard notification: ';
    }
  };
  
  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    
    if (!phoneNumber) {
      setError('Please enter a phone number');
      return;
    }
    
    setIsSubmitting(true);
    setError(null);
    setSuccess(null);
    
    try {
      const data = {
        phone_number: phoneNumber,
        entity_type: entityType,
        entity_id: entityId
      };
      
      if (useCustomMessage) {
        data.message = customMessage;
      } else {
        data.notification_type = notificationType;
        
        // Add entity data based on notification type
        if (notificationType === 'compliance_alert') {
          data.monitor_id = entityId;
        } else if (notificationType === 'risk_assessment') {
          data.assessment_id = entityId;
        }
      }
      
      const result = await sendSmsNotification(data);
      
      if (result.success) {
        setSuccess('SMS notification sent successfully!');
        setTimeout(() => {
          onClose();
        }, 2000);
      } else {
        setError(result.message || 'Failed to send SMS notification');
      }
    } catch (err) {
      console.error('Error sending SMS notification:', err);
      setError(err.message || 'Failed to send SMS notification');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  const modalContent = (
    <div>
      {error && (
        <div className="alert alert-danger">{error}</div>
      )}
      
      {success && (
        <div className="alert alert-success">{success}</div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="phoneNumber" className="form-label">Phone Number <span className="text-danger">*</span></label>
          <div className="input-group">
            <span className="input-group-text">+</span>
            <input
              type="tel"
              className="form-control"
              id="phoneNumber"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              placeholder="15551234567 (no spaces or dashes)"
              required
            />
          </div>
          <div className="form-text">
            Include country code without the + sign (e.g., 15551234567 for US)
          </div>
        </div>
        
        <div className="mb-3 form-check">
          <input
            type="checkbox"
            className="form-check-input"
            id="useCustomMessage"
            checked={useCustomMessage}
            onChange={() => setUseCustomMessage(!useCustomMessage)}
          />
          <label className="form-check-label" htmlFor="useCustomMessage">
            Use custom message
          </label>
        </div>
        
        {useCustomMessage ? (
          <div className="mb-3">
            <label htmlFor="customMessage" className="form-label">Custom Message <span className="text-danger">*</span></label>
            <textarea
              className="form-control"
              id="customMessage"
              rows="5"
              value={customMessage}
              onChange={(e) => setCustomMessage(e.target.value)}
              required={useCustomMessage}
              placeholder="Enter your custom SMS message..."
            ></textarea>
            <div className="form-text">
              Max 160 characters for standard SMS
            </div>
          </div>
        ) : (
          <div className="mb-3">
            <label className="form-label">Default Message Preview</label>
            <div className="card">
              <div className="card-body bg-light">
                <small className="text-muted">{getDefaultMessage()}</small>
              </div>
            </div>
            <div className="form-text">
              A detailed message will be automatically generated
            </div>
          </div>
        )}
      </form>
    </div>
  );
  
  const modalActions = (
    <>
      <button 
        type="button" 
        className="btn btn-secondary" 
        onClick={onClose}
        disabled={isSubmitting}
      >
        Cancel
      </button>
      <button 
        type="button" 
        className="btn btn-primary" 
        onClick={handleSubmit}
        disabled={isSubmitting || success}
      >
        {isSubmitting ? (
          <>
            <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Sending...
          </>
        ) : (
          'Send SMS'
        )}
      </button>
    </>
  );
  
  return (
    <Modal
      show={show}
      onClose={onClose}
      title={getDefaultTitle()}
      size="md"
      actions={modalActions}
      closeOnBackdropClick={!isSubmitting}
      closeOnEscape={!isSubmitting}
    >
      {modalContent}
    </Modal>
  );
};

export default SmsNotificationModal;