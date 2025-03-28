import React, { useState, useEffect } from 'react';
import { fetchReports } from '../services/api';
import PageHeader from '../components/common/PageHeader';
import LoadingSpinner from '../components/common/LoadingSpinner';
import StatusBadge from '../components/common/StatusBadge';
import ReportFormModal from '../components/reporting/ReportFormModal';
import ReportDetailModal from '../components/reporting/ReportDetailModal';
import ReportCard from '../components/reporting/ReportCard';

// Format the report type to be more readable
const formatReportType = (type) => {
  if (!type) return '';
  
  // Convert from snake_case or camelCase to Title Case with spaces
  return type
    .replace(/_/g, ' ')  // Replace underscores with spaces
    .replace(/([A-Z])/g, ' $1')  // Add space before capital letters
    .replace(/^\w/, c => c.toUpperCase())  // Capitalize first letter
    .trim();  // Remove any leading/trailing spaces
};

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [selectedReportId, setSelectedReportId] = useState(null);
  const [reportsByType, setReportsByType] = useState({});

  const loadReports = async () => {
    try {
      setIsLoading(true);
      const data = await fetchReports();
      setReports(data);
      
      // Group reports by type for summary
      const grouped = data.reduce((acc, report) => {
        const type = report.report_type;
        if (!acc[type]) {
          acc[type] = [];
        }
        acc[type].push(report);
        return acc;
      }, {});
      
      setReportsByType(grouped);
      setError(null);
    } catch (err) {
      console.error('Error fetching reports:', err);
      setError('Failed to load reports data');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadReports();
  }, []);

  const handleCreateReport = () => {
    setShowCreateModal(true);
  };
  
  const handleViewReport = (reportId) => {
    setSelectedReportId(reportId);
    setShowDetailModal(true);
  };
  
  const handleReportCreated = () => {
    // Reload reports after creation
    loadReports();
  };

  if (isLoading && reports.length === 0) {
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
        <>
          <div className="row mb-4">
            {Object.keys(reportsByType).length > 0 ? (
              Object.keys(reportsByType).map(type => (
                <div className="col-md-6 col-lg-3 mb-3" key={type}>
                  <ReportCard 
                    reportType={type} 
                    count={reportsByType[type].length} 
                  />
                </div>
              ))
            ) : (
              <div className="col-12">
                <div className="card mb-4 border-0 shadow-sm">
                  <div className="card-body">
                    <p className="mb-0 text-center">
                      <i className="fas fa-info-circle me-2 text-primary"></i>
                      No reports found. Generate your first report to get started.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
          
          <div className="card mb-4 border-0 shadow-sm">
            <div className="card-body">
              <div className="d-flex">
                <div className="me-3">
                  <i className="fas fa-lightbulb text-warning fs-3"></i>
                </div>
                <div>
                  <h6 className="mb-1">AI Governance Reports</h6>
                  <p className="mb-0 text-muted">
                    These reports provide insights into your organization's AI governance practices.
                    Generate reports to track policy compliance, risk assessments, and overall governance status.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white py-3 border-0">
              <h5 className="mb-0">
                <i className="fas fa-file-alt me-2 text-primary"></i>
                Available Reports
              </h5>
            </div>
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
                        <td>{formatReportType(report.report_type)}</td>
                        <td>{new Date(report.created_at).toLocaleDateString()}</td>
                        <td>
                          <StatusBadge status={report.status} />
                        </td>
                        <td>
                          <div className="d-flex gap-2">
                            <button 
                              className="btn btn-sm btn-light" 
                              title="View Report"
                              onClick={() => handleViewReport(report.id)}
                            >
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
          </div>
        </>
      )}
      
      {/* Create Report Modal */}
      <ReportFormModal 
        show={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onReportCreated={handleReportCreated}
      />

      {/* View Report Details Modal */}
      <ReportDetailModal
        show={showDetailModal}
        reportId={selectedReportId}
        onClose={() => setShowDetailModal(false)}
      />
    </div>
  );
};

export default Reports;