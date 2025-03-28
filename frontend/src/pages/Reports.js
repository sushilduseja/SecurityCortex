import React, { useState, useEffect } from 'react';
import { fetchReports } from '../services/api';
import PageHeader from '../components/common/PageHeader';
import LoadingSpinner from '../components/common/LoadingSpinner';
import StatusBadge from '../components/common/StatusBadge';

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadReports = async () => {
      try {
        setIsLoading(true);
        const data = await fetchReports();
        setReports(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching reports:', err);
        setError('Failed to load reports data');
      } finally {
        setIsLoading(false);
      }
    };

    loadReports();
  }, []);

  const handleCreateReport = () => {
    // Handle report creation - open modal, redirect to form, etc.
    console.log('Create report clicked');
  };

  if (isLoading) {
    return <LoadingSpinner message="Loading reports..." />;
  }

  return (
    <div className="reports-container">
      <PageHeader 
        title="Reports" 
        subtitle="Generate and view governance reports"
        actions={
          <button 
            className="btn btn-primary" 
            onClick={handleCreateReport}
          >
            <i className="fas fa-plus me-2"></i>
            Generate Report
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
                <th>Title</th>
                <th>Report Type</th>
                <th>Created</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {reports.length === 0 ? (
                <tr>
                  <td colSpan={5} className="text-center py-4">No reports found</td>
                </tr>
              ) : (
                reports.map((report) => (
                  <tr key={report.id}>
                    <td>{report.title}</td>
                    <td>{report.report_type}</td>
                    <td>{new Date(report.created_at).toLocaleDateString()}</td>
                    <td>
                      <StatusBadge status={report.status} />
                    </td>
                    <td>
                      <div className="d-flex gap-2">
                        <button className="btn btn-sm btn-light" title="View">
                          <i className="fas fa-eye"></i>
                        </button>
                        <button className="btn btn-sm btn-light" title="Download">
                          <i className="fas fa-download"></i>
                        </button>
                        <button className="btn btn-sm btn-light" title="Share">
                          <i className="fas fa-share-alt"></i>
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

export default Reports;