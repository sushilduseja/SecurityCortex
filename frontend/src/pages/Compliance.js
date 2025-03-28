import React, { useState, useEffect } from 'react';
import { fetchComplianceMonitors } from '../services/api';
import PageHeader from '../components/common/PageHeader';
import LoadingSpinner from '../components/common/LoadingSpinner';
import StatusBadge from '../components/common/StatusBadge';

const Compliance = () => {
  const [monitors, setMonitors] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadMonitors = async () => {
      try {
        setIsLoading(true);
        const data = await fetchComplianceMonitors();
        setMonitors(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching compliance monitors:', err);
        setError('Failed to load compliance data');
      } finally {
        setIsLoading(false);
      }
    };

    loadMonitors();
    
    // Poll for updates every 30 seconds
    const interval = setInterval(loadMonitors, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleCreateMonitor = () => {
    // Handle monitor creation - open modal, redirect to form, etc.
    console.log('Create monitor clicked');
  };

  if (isLoading) {
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
                monitors.map((monitor) => (
                  <tr key={monitor.id}>
                    <td>{monitor.name}</td>
                    <td>{monitor.model_or_system}</td>
                    <td>{monitor.current_value.toFixed(2)}</td>
                    <td>{monitor.threshold_value.toFixed(2)}</td>
                    <td>
                      <StatusBadge status={monitor.alert_level} />
                    </td>
                    <td>
                      {monitor.last_checked ? 
                        new Date(monitor.last_checked).toLocaleString() : 
                        'Not checked yet'}
                    </td>
                    <td>
                      <div className="d-flex gap-2">
                        <button className="btn btn-sm btn-light" title="View">
                          <i className="fas fa-eye"></i>
                        </button>
                        <button className="btn btn-sm btn-light" title="Edit">
                          <i className="fas fa-edit"></i>
                        </button>
                        <button className="btn btn-sm btn-light" title="Refresh">
                          <i className="fas fa-sync-alt"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Compliance;