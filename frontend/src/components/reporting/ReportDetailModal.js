import React, { useState, useEffect } from 'react';
import { fetchReport } from '../../services/api';
import LoadingSpinner from '../common/LoadingSpinner';
import StatusBadge from '../common/StatusBadge';

const ReportDetailModal = ({ show, reportId, onClose }) => {
  const [report, setReport] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadReport = async () => {
      if (!reportId || !show) return;
      
      try {
        setIsLoading(true);
        const data = await fetchReport(reportId);
        setReport(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching report details:', err);
        setError('Failed to load report details');
      } finally {
        setIsLoading(false);
      }
    };

    loadReport();
  }, [reportId, show]);

  const formatContent = (content) => {
    // This is a simple implementation that splits by newlines and applies basic styling
    // In a real implementation, you'd use a Markdown renderer
    if (!content) return '';
    
    return content.split('\n').map((line, index) => {
      // Apply basic styling for headers
      if (line.startsWith('# ')) {
        return <h1 key={index} className="mt-4 mb-3">{line.substring(2)}</h1>;
      } else if (line.startsWith('## ')) {
        return <h2 key={index} className="mt-3 mb-2">{line.substring(3)}</h2>;
      } else if (line.startsWith('### ')) {
        return <h3 key={index} className="mt-3 mb-2">{line.substring(4)}</h3>;
      } else if (line.startsWith('- ')) {
        return <li key={index} className="ms-3">{line.substring(2)}</li>;
      } else if (line.startsWith('**')) {
        return <strong key={index}>{line.replace(/\*\*/g, '')}</strong>;
      } else if (line.trim() === '') {
        return <br key={index} />;
      } else {
        return <p key={index} className="mb-2">{line}</p>;
      }
    });
  };

  if (!show) return null;

  return (
    <div className="modal fade show" style={{ display: 'block' }} tabIndex="-1">
      <div className="modal-dialog modal-lg modal-dialog-scrollable">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Report Details</h5>
            <button 
              type="button" 
              className="btn-close" 
              onClick={onClose}
              aria-label="Close"
            ></button>
          </div>
          <div className="modal-body">
            {isLoading ? (
              <LoadingSpinner message="Loading report details..." />
            ) : error ? (
              <div className="alert alert-danger">{error}</div>
            ) : report ? (
              <div className="report-details">
                <div className="row mb-4">
                  <div className="col-md-8">
                    <h3>{report.title}</h3>
                    <p className="text-muted">{report.description}</p>
                  </div>
                  <div className="col-md-4 text-md-end">
                    <div className="mb-2">
                      <StatusBadge status={report.status} />
                    </div>
                    <small className="text-muted">
                      Type: {report.report_type}
                    </small>
                  </div>
                </div>
                
                <div className="card mb-3">
                  <div className="card-header bg-light">
                    <h6 className="mb-0">Report Insights</h6>
                  </div>
                  <div className="card-body bg-light">
                    <div className="insights">
                      {formatContent(report.insights)}
                    </div>
                  </div>
                </div>
                
                <div className="card mb-3">
                  <div className="card-header bg-light">
                    <h6 className="mb-0">Report Content</h6>
                  </div>
                  <div className="card-body">
                    <div className="report-content">
                      {formatContent(report.content)}
                    </div>
                  </div>
                </div>
                
                <div className="text-muted mt-3">
                  Report generated on {new Date(report.created_at).toLocaleString()}
                </div>
              </div>
            ) : (
              <div className="alert alert-warning">Report not found</div>
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
            {report && (
              <button 
                type="button" 
                className="btn btn-primary"
              >
                <i className="fas fa-file-export me-2"></i>
                Export Report
              </button>
            )}
          </div>
        </div>
      </div>
      <div className="modal-backdrop fade show"></div>
    </div>
  );
};

export default ReportDetailModal;