import React from 'react';

const StatusBadge = ({ status, className }) => {
  const getStatusConfig = (status) => {
    const statusLower = status.toLowerCase();
    
    switch (statusLower) {
      case 'active':
      case 'completed':
      case 'approved':
      case 'normal':
        return { className: 'success', icon: 'check-circle' };
      
      case 'pending':
      case 'in progress':
      case 'review':
      case 'draft':
        return { className: 'warning', icon: 'clock' };
      
      case 'critical':
      case 'error':
      case 'failed':
      case 'high':
        return { className: 'danger', icon: 'exclamation-triangle' };
        
      case 'medium':
      case 'caution':
      case 'warning':
        return { className: 'warning', icon: 'exclamation-circle' };
        
      case 'low':
      case 'info':
      case 'inactive':
        return { className: 'info', icon: 'info-circle' };
        
      default:
        return { className: 'secondary', icon: 'circle' };
    }
  };

  const { className: statusClass, icon } = getStatusConfig(status);
  
  return (
    <span className={`badge badge-${statusClass} ${className || ''}`}>
      <i className={`fas fa-${icon} me-1`}></i>
      {status}
    </span>
  );
};

export default StatusBadge;