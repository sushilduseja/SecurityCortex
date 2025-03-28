import React from 'react';
import NotificationForm from './NotificationForm';

const NotificationModal = ({ 
  show, 
  onClose, 
  title = 'Send Notification', 
  entityType,
  entityId,
  entityName,
  initialData = {}
}) => {
  if (!show) return null;
  
  return (
    <div className="modal fade show" style={{ display: 'block' }} tabIndex="-1">
      <div className="modal-dialog modal-lg">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">{title}</h5>
            <button 
              type="button" 
              className="btn-close" 
              onClick={onClose}
              aria-label="Close"
            ></button>
          </div>
          <div className="modal-body">
            {entityName && (
              <div className="alert alert-info mb-4">
                <i className="fas fa-info-circle me-2"></i>
                You are sending a notification regarding: <strong>{entityName}</strong>
              </div>
            )}
            
            <NotificationForm 
              entityType={entityType} 
              entityId={entityId}
              initialData={initialData}
            />
          </div>
          <div className="modal-footer">
            <button 
              type="button" 
              className="btn btn-secondary" 
              onClick={onClose}
            >
              Close
            </button>
          </div>
        </div>
      </div>
      <div className="modal-backdrop fade show"></div>
    </div>
  );
};

export default NotificationModal;