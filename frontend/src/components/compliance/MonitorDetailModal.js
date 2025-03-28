import React, { useState, useEffect } from 'react';
import { fetchComplianceMonitor, updateComplianceMonitor } from '../../services/api';
import LoadingSpinner from '../common/LoadingSpinner';
import StatusBadge from '../common/StatusBadge';
import Modal from '../common/Modal';

const MonitorDetailModal = ({ show, monitorId, onClose, onMonitorUpdated }) => {
  const [monitor, setMonitor] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isUpdating, setIsUpdating] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadMonitor = async () => {
      if (!monitorId || !show) return;
      
      try {
        setIsLoading(true);
        const data = await fetchComplianceMonitor(monitorId);
        setMonitor(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching monitor details:', err);
        setError('Failed to load monitor details');
      } finally {
        setIsLoading(false);
      }
    };

    loadMonitor();
  }, [monitorId, show]);

  const handleRefreshMonitor = async () => {
    if (!monitor) return;
    
    try {
      setIsUpdating(true);
      
      // Call API to update monitor (this will trigger backend to recalculate values)
      await updateComplianceMonitor(monitor.id, monitor);
      
      // Reload the monitor with new values
      const updatedMonitor = await fetchComplianceMonitor(monitorId);
      setMonitor(updatedMonitor);
      
      if (onMonitorUpdated) {
        onMonitorUpdated();
      }
      
    } catch (err) {
      console.error('Error refreshing monitor:', err);
      setError('Failed to refresh monitor data');
    } finally {
      setIsUpdating(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Critical': return 'danger';
      case 'Warning': return 'warning';
      case 'Good': return 'success';
      default: return 'info';
    }
  };

  const modalContent = (
    <>
      {isLoading ? (
        <LoadingSpinner message="Loading monitor details..." />
      ) : error ? (
        <div className="alert alert-danger">{error}</div>
      ) : monitor ? (
        <div className="monitor-details">
          <div className="row mb-4">
            <div className="col-md-8">
              <h3>{monitor.name}</h3>
              <p className="text-muted">{monitor.description}</p>
            </div>
            <div className="col-md-4 text-md-end">
              <div className="mb-2">
                <StatusBadge status={monitor.status} />
                {' '}
                <StatusBadge status={monitor.alert_level} type={getStatusColor(monitor.alert_level)} />
              </div>
              <small className="text-muted">
                Last Updated: {monitor.last_checked ? 
                  new Date(monitor.last_checked).toLocaleString() : 
                  'Not checked yet'}
              </small>
            </div>
          </div>
          
          <div className="card mb-4">
            <div className="card-header">
              <h6 className="mb-0">Metrics Overview</h6>
            </div>
            <div className="card-body">
              <div className="row">
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Model/System</label>
                    <div className="form-control bg-light">{monitor.model_or_system}</div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Alert Level</label>
                    <div className="form-control bg-light d-flex align-items-center">
                      <StatusBadge status={monitor.alert_level} type={getStatusColor(monitor.alert_level)} />
                      <span className="ms-2">
                        {monitor.alert_level === 'Critical' ? 'Immediate action required' :
                         monitor.alert_level === 'Warning' ? 'Attention needed' : 
                         monitor.alert_level === 'Good' ? 'Exceeding expectations' : 'Within normal range'}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="row align-items-end">
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Current Value</label>
                    <div className="progress" style={{ height: '30px' }}>
                      <div 
                        className={`progress-bar bg-${getStatusColor(monitor.alert_level)}`}
                        role="progressbar" 
                        style={{ width: `${monitor.current_value * 100}%` }}
                        aria-valuenow={monitor.current_value * 100}
                        aria-valuemin="0" 
                        aria-valuemax="100"
                      >
                        {(monitor.current_value * 100).toFixed(1)}%
                      </div>
                    </div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Threshold Value</label>
                    <div className="progress" style={{ height: '30px' }}>
                      <div 
                        className="progress-bar bg-info"
                        role="progressbar" 
                        style={{ width: `${monitor.threshold_value * 100}%` }}
                        aria-valuenow={monitor.threshold_value * 100}
                        aria-valuemin="0" 
                        aria-valuemax="100"
                      >
                        {(monitor.threshold_value * 100).toFixed(1)}%
                      </div>
                    </div>
                    <small className="text-muted">
                      {monitor.current_value < monitor.threshold_value ? 
                        'Alert: Current value is below threshold' :
                        'Status: Current value meets or exceeds threshold'}
                    </small>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="card mb-3">
            <div className="card-header">
              <h6 className="mb-0">Recommended Actions</h6>
            </div>
            <div className="card-body">
              {monitor.alert_level === 'Critical' ? (
                <div className="alert alert-danger">
                  <h6 className="alert-heading"><i className="fas fa-exclamation-triangle me-2"></i> Critical Issue Detected</h6>
                  <p>The monitored metric is significantly below the required threshold. Immediate action is required.</p>
                  <hr />
                  <ul className="mb-0">
                    <li>Investigate root cause of compliance failure</li>
                    <li>Implement remediation actions to restore compliance</li>
                    <li>Consider temporarily restricting model access until resolved</li>
                    <li>Document incident and response actions for audit purposes</li>
                  </ul>
                </div>
              ) : monitor.alert_level === 'Warning' ? (
                <div className="alert alert-warning">
                  <h6 className="alert-heading"><i className="fas fa-exclamation-circle me-2"></i> Warning: Attention Required</h6>
                  <p>The monitored metric is approaching or slightly below the threshold value.</p>
                  <hr />
                  <ul className="mb-0">
                    <li>Review recent changes to the model or system</li>
                    <li>Monitor more frequently for further degradation</li>
                    <li>Prepare remediation plan if the metric continues to decline</li>
                    <li>Document the warning in your compliance logs</li>
                  </ul>
                </div>
              ) : (
                <div className="alert alert-success">
                  <h6 className="alert-heading"><i className="fas fa-check-circle me-2"></i> Compliant: No Action Required</h6>
                  <p>The monitored metric is meeting or exceeding the required threshold.</p>
                  <hr />
                  <ul className="mb-0">
                    <li>Continue regular monitoring</li>
                    <li>Document compliance status for audit purposes</li>
                    <li>Review threshold values periodically to ensure they remain appropriate</li>
                  </ul>
                </div>
              )}
            </div>
          </div>
          
          <div className="text-muted mt-3">
            Monitor ID: {monitor.id} | Created: {new Date(monitor.created_at).toLocaleString()}
          </div>
        </div>
      ) : (
        <div className="alert alert-warning">Monitor not found</div>
      )}
    </>
  );
  
  const modalActions = (
    <>
      <button 
        type="button" 
        className="btn btn-secondary" 
        onClick={onClose}
      >
        Close
      </button>
      
      {monitor && (
        <button 
          type="button" 
          className="btn btn-primary"
          onClick={handleRefreshMonitor}
          disabled={isUpdating}
        >
          {isUpdating ? (
            <>
              <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Refreshing...
            </>
          ) : (
            <>
              <i className="fas fa-sync-alt me-2"></i>
              Refresh Data
            </>
          )}
        </button>
      )}
    </>
  );

  return (
    <Modal
      show={show}
      onClose={onClose}
      title="Monitor Details"
      size="lg"
      actions={modalActions}
      closeOnBackdropClick={true}
      closeOnEscape={true}
      scrollable={true}
    >
      {modalContent}
    </Modal>
  );
};

export default MonitorDetailModal;