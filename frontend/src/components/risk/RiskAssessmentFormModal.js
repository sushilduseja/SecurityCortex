import React, { useState } from 'react';
import { createRiskAssessment } from '../../services/api';
import Modal from '../common/Modal';

const RiskAssessmentFormModal = ({ show, onClose, onAssessmentCreated }) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [modelName, setModelName] = useState('');
  const [documentation, setDocumentation] = useState('');
  const [error, setError] = useState(null);
  
  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    
    if (!modelName.trim() || !documentation.trim()) {
      setError('Please fill in all required fields');
      return;
    }
    
    setIsSubmitting(true);
    setError(null);
    
    try {
      const assessment = {
        model_name: modelName,
        documentation: documentation
      };
      
      const response = await createRiskAssessment(assessment);
      
      if (onAssessmentCreated) {
        onAssessmentCreated(response);
      }
      
      // Reset form and close modal
      resetForm();
      onClose();
      
    } catch (err) {
      console.error('Error creating risk assessment:', err);
      setError(err.message || 'Failed to create risk assessment');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  const resetForm = () => {
    setModelName('');
    setDocumentation('');
    setError(null);
  };
  
  const modalContent = (
    <>
      {error && (
        <div className="alert alert-danger">{error}</div>
      )}
      
      <div className="alert alert-info">
        <i className="fas fa-info-circle me-2"></i>
        The AI Risk Assessment Agent will analyze your AI model documentation to identify potential risks and provide recommendations.
      </div>
      
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="modelName" className="form-label">AI Model Name <span className="text-danger">*</span></label>
          <input
            type="text"
            className="form-control"
            id="modelName"
            value={modelName}
            onChange={(e) => setModelName(e.target.value)}
            required
            placeholder="e.g., SentimentAnalyzer-v2, CustomerSegmentation-2025, etc."
          />
        </div>
        
        <div className="mb-3">
          <label htmlFor="documentation" className="form-label">Model Documentation <span className="text-danger">*</span></label>
          <textarea
            className="form-control"
            id="documentation"
            rows="12"
            value={documentation}
            onChange={(e) => setDocumentation(e.target.value)}
            required
            placeholder="Enter model documentation including details about purpose, training data, model type, limitations, intended use cases, etc."
          ></textarea>
          <div className="form-text">
            Provide detailed information about your AI model to receive a more accurate risk assessment.
          </div>
        </div>
      </form>
    </>
  );
  
  const modalActions = (
    <>
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
            Assessing Risks...
          </>
        ) : (
          'Create Assessment'
        )}
      </button>
    </>
  );
  
  return (
    <Modal
      show={show}
      onClose={onClose}
      title="Create Risk Assessment"
      size="lg"
      actions={modalActions}
      closeOnBackdropClick={true}
      closeOnEscape={true}
    >
      {modalContent}
    </Modal>
  );
};

export default RiskAssessmentFormModal;