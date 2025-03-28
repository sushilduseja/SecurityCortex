import React, { useState, useEffect } from 'react';
import { fetchComplianceMonitors, updateComplianceMonitor } from '../services/api';
import PageHeader from '../components/common/PageHeader';
import LoadingSpinner from '../components/common/LoadingSpinner';
import StatusBadge from '../components/common/StatusBadge';
import MonitorFormModal from '../components/compliance/MonitorFormModal';
import MonitorDetailModal from '../components/compliance/MonitorDetailModal';

const Compliance = () => {
  const [monitors, setMonitors] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [selectedMonitorId, setSelectedMonitorId] = useState(null);
  const [complianceStats, setComplianceStats] = useState({
    overall_status: 'Unknown',
    compliance_rate: 0,
    critical_alerts: 0,
    warning_alerts: 0
  });

  const loadMonitors = async () => {
    try {
      setIsLoading(true);
      const data = await fetchComplianceMonitors();
      setMonitors(data);
      
      // Calculate compliance statistics
      calculateComplianceStats(data);
      
      setError(null);
    } catch (err) {
      console.error('Error fetching compliance monitors:', err);
      setError('Failed to load compliance data');
    } finally {
      setIsLoading(false);
    }
  };

  const calculateComplianceStats = (monitorsData) => {
    if (!monitorsData || !monitorsData.length) {
      setComplianceStats({
        overall_status: 'Unknown',
        compliance_rate: 0,
        critical_alerts: 0,
        warning_alerts: 0
      });
      return;
    }
    
    // Count alerts by level
    const alertCounts = { Critical: 0, Warning: 0, Normal: 0, Good: 0 };
    let compliantCount = 0;
    
    monitorsData.forEach(monitor => {
      const alertLevel = monitor.alert_level;
      alertCounts[alertLevel] = (alertCounts[alertLevel] || 0) + 1;
      
      // Count Normal and Good as compliant
      if (alertLevel === 'Normal' || alertLevel === 'Good') {
        compliantCount++;
      }
    });
    
    // Calculate compliance rate
    const complianceRate = (compliantCount / monitorsData.length) * 100;
    
    // Determine overall status
    let overallStatus = 'Normal';
    if (alertCounts.Critical > 0) {
      overallStatus = 'Critical';
    } else if (alertCounts.Warning > 0) {
      overallStatus = 'Warning';
    } else if (alertCounts.Good > alertCounts.Normal) {
      overallStatus = 'Good';
    }
    
    setComplianceStats({
      overall_status: overallStatus,
      compliance_rate: complianceRate,
      critical_alerts: alertCounts.Critical,
      warning_alerts: alertCounts.Warning,
      normal_monitors: alertCounts.Normal,
      good_monitors: alertCounts.Good
    });
  };

  useEffect(() => {
    loadMonitors();
    
    // Poll for updates every 30 seconds
    const interval = setInterval(loadMonitors, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleCreateMonitor = () => {
    setShowCreateModal(true);
  };
  
  const handleViewMonitor = (monitorId) => {
    setSelectedMonitorId(monitorId);
    setShowDetailModal(true);
  };
  
  const handleRefreshMonitor = async (monitorId) => {
    try {
      const monitor = monitors.find(m => m.id === monitorId);
      if (!monitor) return;
      
      // Update the monitor to trigger a new value calculation on the backend
      await updateComplianceMonitor(monitorId, monitor);
      
      // Reload monitors
      await loadMonitors();
    } catch (err) {
      console.error('Error refreshing monitor:', err);
    }
  };

  const handleMonitorCreated = () => {
    // Reload monitors after creation
    loadMonitors();
  };
  
  const handleMonitorUpdated = () => {
    // Reload monitors after update
    loadMonitors();
  };
  
  const getStatusClass = (status) => {
    switch (status) {
      case 'Critical': return 'danger';
      case 'Warning': return 'warning';
      case 'Good': return 'success';
      default: return 'info';
    }
  };

  if (isLoading && monitors.length === 0) {
    return <LoadingSpinner message="Loading compliance monitors..." />;
  }

  return (
    <div className="compliance-container">
      <PageHeader 
        title="Compliance Monitoring" 
        subtitle="Monitor compliance metrics for your AI systems"
        actions={
          <button 
            className="btn btn-primary" 
            onClick={handleCreateMonitor}
          >
            <i className="fas fa-plus me-2"></i>
            Add Monitor
          </button>
        }
      />

      {error ? (
        <div className="alert alert-danger">
          <i className="fas fa-exclamation-circle me-2"></i>
          {error}
        </div>
      ) : (
        <>
          <div className="row mb-4">
            <div className="col-md-6">
              <div className="card h-100">
                <div className="card-body">
                  <h5 className="card-title">Compliance Status</h5>
                  <div className="d-flex align-items-center mt-3">
                    <div className="me-3">
                      <div 
                        className={`status-circle bg-${getStatusClass(complianceStats.overall_status)}`}
                        style={{ 
                          width: '60px', 
                          height: '60px',  
                          borderRadius: '50%', 
                          display: 'flex', 
                          alignItems: 'center', 
                          justifyContent: 'center' 
                        }}
                      >
                        <i className="fas fa-check-circle text-white fs-3"></i>
                      </div>
                    </div>
                    <div>
                      <h3 className="mb-0">{complianceStats.overall_status}</h3>
                      <p className="text-muted mb-0">
                        {complianceStats.compliance_rate.toFixed(1)}% Compliance Rate
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="col-md-6">
              <div className="card h-100">
                <div className="card-body">
                  <h5 className="card-title">Alert Summary</h5>
                  <div className="row mt-3">
                    <div className="col-6">
                      <div className="d-flex align-items-center">
                        <div className="alert-badge bg-danger text-white p-2 rounded me-2">
                          <i className="fas fa-exclamation-triangle"></i>
                        </div>
                        <div>
                          <h6 className="mb-0">{complianceStats.critical_alerts}</h6>
                          <small className="text-muted">Critical Alerts</small>
                        </div>
                      </div>
                    </div>
                    <div className="col-6">
                      <div className="d-flex align-items-center">
                        <div className="alert-badge bg-warning text-dark p-2 rounded me-2">
                          <i className="fas fa-exclamation-circle"></i>
                        </div>
                        <div>
                          <h6 className="mb-0">{complianceStats.warning_alerts}</h6>
                          <small className="text-muted">Warning Alerts</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="card mb-4">
            <div className="card-body">
              <p className="mb-0">
                <i className="fas fa-info-circle me-2 text-primary"></i>
                AI compliance monitors track key metrics to ensure your AI systems meet governance requirements.
                Set up monitors for different models and receive alerts when metrics fall outside acceptable thresholds.
              </p>
            </div>
          </div>

          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Monitor Name</th>
                  <th>Model/System</th>
                  <th>Current Value</th>
                  <th>Threshold</th>
                  <th>Alert Level</th>
                  <th>Last Checked</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {monitors.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="text-center py-4">No compliance monitors found</td>
                  </tr>
                ) : (
                  monitors.map((monitor) => {
                    const alertClass = 
                      monitor.alert_level === 'Critical' ? 'danger' : 
                      monitor.alert_level === 'Warning' ? 'warning' :
                      monitor.alert_level === 'Good' ? 'success' : 'info';
                      
                    return (
                      <tr key={monitor.id}>
                        <td>{monitor.name}</td>
                        <td>{monitor.model_or_system}</td>
                        <td>
                          <div className="progress" style={{ height: '20px', width: '100px' }}>
                            <div 
                              className={`progress-bar bg-${alertClass}`}
                              role="progressbar" 
                              style={{ width: `${monitor.current_value * 100}%` }}
                              aria-valuenow={monitor.current_value * 100}
                              aria-valuemin="0" 
                              aria-valuemax="100"
                            >
                              {(monitor.current_value * 100).toFixed(0)}%
                            </div>
                          </div>
                        </td>
                        <td>{(monitor.threshold_value * 100).toFixed(0)}%</td>
                        <td>
                          <StatusBadge status={monitor.alert_level} type={alertClass} />
                        </td>
                        <td>
                          {monitor.last_checked ? 
                            new Date(monitor.last_checked).toLocaleString() : 
                            'Not checked yet'}
                        </td>
                        <td>
                          <div className="d-flex gap-2">
                            <button 
                              className="btn btn-sm btn-light" 
                              title="View Details"
                              onClick={() => handleViewMonitor(monitor.id)}
                            >
                              <i className="fas fa-eye"></i>
                            </button>
                            <button 
                              className="btn btn-sm btn-light" 
                              title="Refresh"
                              onClick={() => handleRefreshMonitor(monitor.id)}
                            >
                              <i className="fas fa-sync-alt"></i>
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </>
      )}

      {/* Create Monitor Modal */}
      <MonitorFormModal 
        show={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onMonitorCreated={handleMonitorCreated}
      />

      {/* View Monitor Details Modal */}
      <MonitorDetailModal
        show={showDetailModal}
        monitorId={selectedMonitorId}
        onClose={() => setShowDetailModal(false)}
        onMonitorUpdated={handleMonitorUpdated}
      />
    </div>
  );
};

export default Compliance;