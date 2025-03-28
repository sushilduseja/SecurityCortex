import React, { useState, useEffect } from 'react';
import { fetchRiskAssessment } from '../../services/api';
import LoadingSpinner from '../common/LoadingSpinner';
import StatusBadge from '../common/StatusBadge';
import Modal from '../common/Modal';

const RiskAssessmentDetailModal = ({ show, assessmentId, onClose }) => {
  const [assessment, setAssessment] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadAssessment = async () => {
      if (!assessmentId || !show) return;
      
      try {
        setIsLoading(true);
        const data = await fetchRiskAssessment(assessmentId);
        setAssessment(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching risk assessment details:', err);
        setError('Failed to load risk assessment details');
      } finally {
        setIsLoading(false);
      }
    };

    loadAssessment();
  }, [assessmentId, show]);

  const getRiskLevelClass = (score) => {
    if (score >= 75) return 'bg-danger text-white';
    if (score >= 50) return 'bg-warning text-dark';
    return 'bg-success text-white';
  };

  const getRiskLevelText = (score) => {
    if (score >= 75) return 'High Risk';
    if (score >= 50) return 'Medium Risk';
    return 'Low Risk';
  };
  
  const modalContent = (
    <>
      {isLoading ? (
        <LoadingSpinner message="Loading risk assessment details..." />
      ) : error ? (
        <div className="alert alert-danger">{error}</div>
      ) : assessment ? (
        <div className="risk-assessment-details">
          <div className="row mb-4">
            <div className="col-md-8">
              <h4>{assessment.title}</h4>
              <p className="text-muted">Model: {assessment.model_name}</p>
            </div>
            <div className="col-md-4 text-md-end">
              <div className="mb-2">
                <StatusBadge status={assessment.status} />
              </div>
              <div className={`risk-score-badge ${getRiskLevelClass(assessment.risk_score)} p-2 rounded`}>
                <strong>Risk Score: {assessment.risk_score.toFixed(1)}</strong> - {getRiskLevelText(assessment.risk_score)}
              </div>
            </div>
          </div>
          
          <div className="card mb-3">
            <div className="card-header bg-light">
              <h6 className="mb-0">Findings</h6>
            </div>
            <div className="card-body">
              <div className="findings">
                {/* In a real implementation, use a Markdown renderer here */}
                <pre className="findings-pre">{assessment.findings}</pre>
              </div>
            </div>
          </div>
          
          <div className="card mb-3">
            <div className="card-header bg-light">
              <h6 className="mb-0">Recommendations</h6>
            </div>
            <div className="card-body">
              <div className="recommendations">
                {/* In a real implementation, use a Markdown renderer here */}
                <pre className="recommendations-pre">{assessment.recommendations}</pre>
              </div>
            </div>
          </div>
          
          <div className="row mt-4">
            <div className="col-md-6">
              <small className="text-muted">
                Created: {new Date(assessment.created_at).toLocaleString()}
              </small>
            </div>
          </div>
        </div>
      ) : (
        <div className="alert alert-warning">Risk assessment not found</div>
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
      {assessment && (
        <button 
          type="button" 
          className="btn btn-primary"
        >
          Export as PDF
        </button>
      )}
    </>
  );

  return (
    <Modal
      show={show}
      onClose={onClose}
      title="Risk Assessment Details"
      size="lg"
      actions={modalActions}
      closeOnBackdropClick={true}
      closeOnEscape={true}
    >
      {modalContent}
    </Modal>
  );
};

export default RiskAssessmentDetailModal;