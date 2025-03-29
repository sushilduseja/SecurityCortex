import React, { useState, useEffect } from 'react';
import { fetchReports } from '../services/api';
import PageHeader from '../components/common/PageHeader';
import LoadingSpinner from '../components/common/LoadingSpinner';
import StatusBadge from '../components/common/StatusBadge';
import ReportFormModal from '../components/reporting/ReportFormModal';
import ReportDetailModal from '../components/reporting/ReportDetailModal';
import ReportCard from '../components/reporting/ReportCard';

// Maps report types to their display titles for consistent naming
const reportTypeTitles = {
  "governance_summary": "Governance Summary",
  "risk_assessment_overview": "Risk Assessment Overview",
  "compliance_status": "Compliance Status",
  "comprehensive_report": "Comprehensive Governance Report",
  // For backward compatibility, also handle any old/irregular values
  "Governance Summary": "Governance Summary",
  "Risk Assessment Overview": "Risk Assessment Overview",
  "Compliance Status": "Compliance Status",
  "Comprehensive Governance Report": "Comprehensive Governance Report",
  "comprehensive_governance_report": "Comprehensive Governance Report"
};

// Format the report type to be more readable with consistent naming
const formatReportType = (type) => {
  if (!type) return '';
  
  // First check if we have a direct mapping
  if (reportTypeTitles[type]) {
    return reportTypeTitles[type];
  }
  
  // Otherwise fallback to transform from snake_case or camelCase to Title Case with spaces
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
            <div className="card-header bg-white py-3 border-0 d-flex justify-content-between align-items-center">
              <h5 className="mb-0">
                <i className="fas fa-file-alt me-2 text-primary"></i>
                Available Reports
              </h5>
              <div className="input-group" style={{width: "280px"}}>
                <span className="input-group-text bg-light border-end-0">
                  <i className="fas fa-search text-muted"></i>
                </span>
                <input 
                  type="text" 
                  className="form-control border-start-0 bg-light" 
                  placeholder="Search reports..." 
                  aria-label="Search reports"
                />
              </div>
            </div>
            <div className="table-container">
              <table className="table table-hover">
                <thead className="table-light">
                  <tr>
                    <th className="ps-4">Title</th>
                    <th>Report Type</th>
                    <th>Created</th>
                    <th>Status</th>
                    <th className="text-end pe-4">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {reports.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="text-center py-4">No reports found</td>
                    </tr>
                  ) : (
                    reports.map((report) => {
                      // Generate a descriptive title if one is missing
                      const reportTitle = report.title || formatReportType(report.report_type) || "Untitled Report";
                      return (
                        <tr key={report.id}>
                          <td className="ps-4">
                            <div className="fw-bold">{reportTitle}</div>
                            {report.description && (
                              <div className="text-muted small">{report.description}</div>
                            )}
                          </td>
                          <td>{formatReportType(report.report_type)}</td>
                          <td>{new Date(report.created_at).toLocaleDateString()}</td>
                          <td>
                            <StatusBadge status={report.status} />
                          </td>
                          <td className="text-end pe-4">
                            <div className="d-flex gap-2 justify-content-end">
                              <button 
                                className="btn btn-sm btn-outline-primary" 
                                title="View Report"
                                onClick={() => handleViewReport(report.id)}
                              >
                                <i className="fas fa-eye"></i>
                              </button>
                              <button className="btn btn-sm btn-outline-secondary" title="Download">
                                <i className="fas fa-download"></i>
                              </button>
                              <button className="btn btn-sm btn-outline-info" title="Share">
                                <i className="fas fa-share-alt"></i>
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