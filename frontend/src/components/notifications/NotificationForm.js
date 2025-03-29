import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import notificationService from '../../services/NotificationService';

const NotificationForm = ({ onNotificationSent = () => {} }) => {
  const [formData, setFormData] = useState({
    provider: 'sms',
    recipient: '',
    message: '',
    relatedEntity: '',
    entityId: ''
  });
  
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  
  const navigate = useNavigate();
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSending(true);
    setError(null);
    setSuccess(false);
    
    try {
      // Prepare metadata
      const metadata = {};
      if (formData.relatedEntity && formData.entityId) {
        metadata.entity_type = formData.relatedEntity;
        metadata.entity_id = parseInt(formData.entityId, 10);
      }
      
      // Send notification
      const result = await notificationService.sendNotification(
        formData.provider,
        formData.recipient,
        formData.message,
        metadata
      );
      
      if (result.success) {
        setSuccess(true);
        // Reset form
        setFormData({
          provider: 'sms',
          recipient: '',
          message: '',
          relatedEntity: '',
          entityId: ''
        });
        // Notify parent component
        onNotificationSent(result.data);
      } else {
        setError(result.error || 'Failed to send notification');
      }
    } catch (err) {
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setIsSending(false);
    }
  };
  
  return (
    <div className="notification-form card">
      <div className="card-header">
        <h3>Send Notification</h3>
      </div>
      <div className="card-body">
        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}
        {success && (
          <div className="alert alert-success" role="alert">
            Notification sent successfully!
          </div>
        )}
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="provider" className="form-label">Notification Type</label>
            <select
              id="provider"
              name="provider"
              className="form-select"
              value={formData.provider}
              onChange={handleChange}
              required
            >
              <option value="sms">SMS</option>
              <option value="console">Console (Debug)</option>
            </select>
          </div>
          
          <div className="mb-3">
            <label htmlFor="recipient" className="form-label">
              {formData.provider === 'sms' ? 'Phone Number' : 'Recipient ID'}
            </label>
            <input
              type="text"
              id="recipient"
              name="recipient"
              className="form-control"
              value={formData.recipient}
              onChange={handleChange}
              placeholder={formData.provider === 'sms' ? '+1234567890' : 'recipient-id'}
              required
            />
            {formData.provider === 'sms' && (
              <div className="form-text text-muted">
                Enter phone number in international format (e.g., +1234567890)
              </div>
            )}
          </div>
          
          <div className="mb-3">
            <label htmlFor="message" className="form-label">Message</label>
            <textarea
              id="message"
              name="message"
              className="form-control"
              value={formData.message}
              onChange={handleChange}
              rows="3"
              required
            ></textarea>
          </div>
          
          <div className="mb-3">
            <label className="form-label">Related Entity (Optional)</label>
            <div className="row">
              <div className="col">
                <select
                  name="relatedEntity"
                  className="form-select"
                  value={formData.relatedEntity}
                  onChange={handleChange}
                >
                  <option value="">None</option>
                  <option value="policy">Governance Policy</option>
                  <option value="risk_assessment">Risk Assessment</option>
                  <option value="compliance_monitor">Compliance Monitor</option>
                  <option value="report">Report</option>
                </select>
              </div>
              <div className="col">
                <input
                  type="number"
                  name="entityId"
                  className="form-control"
                  value={formData.entityId}
                  onChange={handleChange}
                  placeholder="Entity ID"
                  disabled={!formData.relatedEntity}
                />
              </div>
            </div>
          </div>
          
          <div className="d-flex justify-content-between">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => navigate(-1)}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={isSending}
            >
              {isSending ? 'Sending...' : 'Send Notification'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default NotificationForm;