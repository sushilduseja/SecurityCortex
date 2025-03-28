import React, { useState, useEffect } from 'react';
import { createReport } from '../../services/api';

const ReportFormModal = ({ show, onClose, onReportCreated }) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [reportType, setReportType] = useState('');
  const [error, setError] = useState(null);
  
  // Report types aligned with backend ReportingAgent
  const reportTypes = [
    {
      type: "Governance Summary",
      description: "Summary of AI governance policies and their status"
    },
    {
      type: "Risk Assessment Overview",
      description: "Overview of AI risk assessments and key findings"
    },
    {
      type: "Compliance Status",
      description: "Current status of compliance monitoring across AI systems"
    },
    {
      type: "Comprehensive Governance Report",
      description: "A comprehensive report covering all governance aspects"
    }
  ];
  
  useEffect(() => {
    if (show && reportTypes.length > 0 && !reportType) {
      setReportType(reportTypes[0].type);
    }
  }, [show, reportType, reportTypes]);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!reportType) {
      setError('Please select a report type');
      return;
    }
    
    setIsSubmitting(true);
    setError(null);
    
    try {
      const response = await createReport({ report_type: reportType });
      
      if (onReportCreated) {
        onReportCreated(response);
      }
      
      // Reset form and close modal
      resetForm();
      onClose();
      
    } catch (err) {
      console.error('Error generating report:', err);
      setError(err.message || 'Failed to generate report');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  const resetForm = () => {
    setReportType(reportTypes[0]?.type || '');
    setError(null);
  };
  
  if (!show) return null;
  
  return (
    <div className="modal fade show" style={{ display: 'block' }} tabIndex="-1">
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Generate New Report</h5>
            <button 
              type="button" 
              className="btn-close" 
              onClick={onClose}
              aria-label="Close"
            ></button>
          </div>
          <div className="modal-body">
            {error && (
              <div className="alert alert-danger">{error}</div>
            )}
            
            <div className="alert alert-info">
              <i className="fas fa-info-circle me-2"></i>
              Reports are generated using AI-powered analysis of your governance data.
              The Reporting Agent will compile relevant information into a comprehensive report.
            </div>
            
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label htmlFor="reportType" className="form-label">Report Type <span className="text-danger">*</span></label>
                <select
                  className="form-select"
                  id="reportType"
                  value={reportType}
                  onChange={(e) => setReportType(e.target.value)}
                  required
                >
                  {reportTypes.map(rt => (
                    <option key={rt.type} value={rt.type}>{rt.type}</option>
                  ))}
                </select>
                {reportType && (
                  <div className="form-text mt-2">
                    {reportTypes.find(rt => rt.type === reportType)?.description || ''}
                  </div>
                )}
              </div>
            </form>
          </div>
          <div className="modal-footer">
            <button 
              type="button" 
              className="btn btn-secondary" 
              onClick={onClose}
            >
              Cancel
            </button>
            <button 
              type="button" 
              className="btn btn-primary" 
              onClick={handleSubmit}
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Generating...
                </>
              ) : (
                'Generate Report'
              )}
            </button>
          </div>
        </div>
      </div>
      <div className="modal-backdrop fade show"></div>
    </div>
  );
};

export default ReportFormModal;