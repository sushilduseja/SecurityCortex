import React, { useState, useEffect } from 'react';
import { fetchComplianceMonitor, updateComplianceMonitor } from '../../services/api';
import LoadingSpinner from '../common/LoadingSpinner';
import StatusBadge from '../common/StatusBadge';

const MonitorDetailModal = ({ show, monitorId, onClose, onMonitorUpdated }) => {
  const [monitor, setMonitor] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isUpdating, setIsUpdating] = useState(false);
  const [newValue, setNewValue] = useState('');

  useEffect(() => {
    const loadMonitor = async () => {
      if (!monitorId || !show) return;
      
      try {
        setIsLoading(true);
        const data = await fetchComplianceMonitor(monitorId);
        setMonitor(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching compliance monitor details:', err);
        setError('Failed to load compliance monitor details');
      } finally {
        setIsLoading(false);
      }
    };

    loadMonitor();
  }, [monitorId, show]);

  const handleUpdateValue = async () => {
    if (!monitor) return;
    
    try {
      setIsUpdating(true);
      const updatedMonitor = { 
        ...monitor,
        current_value: parseFloat(newValue) 
      };
      
      await updateComplianceMonitor(monitor.id, updatedMonitor);
      
      // Refresh the monitor data
      const refreshedData = await fetchComplianceMonitor(monitorId);
      setMonitor(refreshedData);
      
      if (onMonitorUpdated) {
        onMonitorUpdated(refreshedData);
      }
      
      setNewValue('');
    } catch (err) {
      console.error('Error updating monitor value:', err);
      setError('Failed to update monitor value');
    } finally {
      setIsUpdating(false);
    }
  };

  const getAlertLevelClass = (level) => {
    switch (level) {
      case 'Critical':
        return 'bg-danger text-white';
      case 'Warning':
        return 'bg-warning text-dark';
      case 'Normal':
        return 'bg-info text-white';
      case 'Good':
        return 'bg-success text-white';
      default:
        return 'bg-secondary text-white';
    }
  };

  const getAlertDescription = (level) => {
    switch (level) {
      case 'Critical':
        return 'Immediate action required. Compliance threshold severely breached.';
      case 'Warning':
        return 'Attention needed. Compliance metrics approaching threshold limits.';
      case 'Normal':
        return 'All compliance metrics within acceptable thresholds.';
      case 'Good':
        return 'Compliance metrics exceeding minimum requirements.';
      default:
        return '';
    }
  };

  if (!show) return null;

  return (
    <div className="modal fade show" style={{ display: 'block' }} tabIndex="-1">
      <div className="modal-dialog modal-lg">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Compliance Monitor Details</h5>
            <button 
              type="button" 
              className="btn-close" 
              onClick={onClose}
              aria-label="Close"
            ></button>
          </div>
          <div className="modal-body">
            {isLoading ? (
              <LoadingSpinner message="Loading compliance monitor details..." />
            ) : error ? (
              <div className="alert alert-danger">{error}</div>
            ) : monitor ? (
              <div className="monitor-details">
                <div className="row mb-4">
                  <div className="col-md-8">
                    <h4>{monitor.name}</h4>
                    <p className="text-muted">{monitor.description}</p>
                  </div>
                  <div className="col-md-4 text-md-end">
                    <div className="mb-2">
                      <StatusBadge status={monitor.status} />
                    </div>
                    <div className={`alert-level-badge ${getAlertLevelClass(monitor.alert_level)} p-2 rounded`}>
                      <strong>{monitor.alert_level}</strong>
                    </div>
                  </div>
                </div>
                
                <div className="card mb-3">
                  <div className="card-header bg-light">
                    <h6 className="mb-0">Monitor Status</h6>
                  </div>
                  <div className="card-body">
                    <div className="row">
                      <div className="col-md-6">
                        <div className="mb-3">
                          <strong>Current Value:</strong>
                          <div className="progress mt-2">
                            <div 
                              className={`progress-bar ${monitor.alert_level === 'Critical' ? 'bg-danger' : 
                                          monitor.alert_level === 'Warning' ? 'bg-warning' : 
                                          monitor.alert_level === 'Good' ? 'bg-success' : 'bg-info'}`} 
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
                          <strong>Threshold Value:</strong>
                          <div className="progress mt-2">
                            <div 
                              className="progress-bar bg-secondary" 
                              role="progressbar" 
                              style={{ width: `${monitor.threshold_value * 100}%` }}
                              aria-valuenow={monitor.threshold_value * 100} 
                              aria-valuemin="0" 
                              aria-valuemax="100"
                            >
                              {(monitor.threshold_value * 100).toFixed(1)}%
                            </div>
                          </div>
                        </div>
                      </div>
                      <div className="col-12">
                        <div className="alert alert-light mt-2">
                          <strong>Alert Status:</strong> {monitor.alert_level}
                          <div className="mt-1">{getAlertDescription(monitor.alert_level)}</div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="update-value-form mt-3">
                      <h6>Update Monitor Value</h6>
                      <div className="input-group">
                        <input
                          type="number"
                          className="form-control"
                          placeholder="Enter new value (0-1)"
                          value={newValue}
                          onChange={(e) => setNewValue(e.target.value)}
                          min="0"
                          max="1"
                          step="0.05"
                        />
                        <span className="input-group-text">
                          {newValue ? `${(parseFloat(newValue) * 100).toFixed(1)}%` : '0%'}
                        </span>
                        <button 
                          className="btn btn-primary" 
                          type="button"
                          onClick={handleUpdateValue}
                          disabled={isUpdating || !newValue}
                        >
                          {isUpdating ? (
                            <>
                              <span className="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
                              Updating...
                            </>
                          ) : (
                            'Update'
                          )}
                        </button>
                      </div>
                      <div className="form-text">
                        Enter a value between 0 and 1 to update the monitor's current value.
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="card mb-3">
                  <div className="card-header bg-light">
                    <h6 className="mb-0">Monitor Information</h6>
                  </div>
                  <div className="card-body">
                    <div className="row">
                      <div className="col-md-6">
                        <p><strong>Model/System:</strong> {monitor.model_or_system}</p>
                        <p><strong>Status:</strong> {monitor.status}</p>
                      </div>
                      <div className="col-md-6">
                        <p><strong>Last Checked:</strong> {new Date(monitor.last_checked).toLocaleString()}</p>
                        <p><strong>Created:</strong> {new Date(monitor.created_at).toLocaleString()}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="alert alert-warning">Compliance monitor not found</div>
            )}
          </div>
          <div className="modal-footer">
            <button 
              type="button" 
              className="btn btn-secondary" 
              onClick={onClose}
            >
              Close
            </button>
            {monitor && monitor.alert_level === 'Critical' && (
              <button 
                type="button" 
                className="btn btn-danger"
              >
                <i className="fas fa-bell me-2"></i>
                Send Alert
              </button>
            )}
          </div>
        </div>
      </div>
      <div className="modal-backdrop fade show"></div>
    </div>
  );
};

export default MonitorDetailModal;