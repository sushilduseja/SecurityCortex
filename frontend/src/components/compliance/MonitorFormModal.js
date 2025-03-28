import React, { useState, useEffect } from 'react';
import { createComplianceMonitor } from '../../services/api';

const MonitorFormModal = ({ show, onClose, onMonitorCreated }) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    model_or_system: '',
    threshold_value: 0.8,
  });
  const [error, setError] = useState(null);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    let newValue = value;
    
    // Convert to number for numeric fields
    if (name === 'threshold_value') {
      newValue = parseFloat(value) || 0;
    }
    
    setFormData({
      ...formData,
      [name]: newValue
    });
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!formData.name) {
      setError('Monitor name is required');
      return;
    }
    
    if (!formData.model_or_system) {
      setError('Model/System name is required');
      return;
    }
    
    // Validate threshold value is between 0 and 1
    if (formData.threshold_value < 0 || formData.threshold_value > 1) {
      setError('Threshold value must be between 0 and 1 (0% - 100%)');
      return;
    }
    
    setIsSubmitting(true);
    setError(null);
    
    try {
      const monitor = {
        ...formData,
        status: 'Active',
        current_value: Math.random() * formData.threshold_value * 1.2, // Simulate initial value
        alert_level: 'Normal'
      };
      
      const response = await createComplianceMonitor(monitor);
      
      if (onMonitorCreated) {
        onMonitorCreated(response);
      }
      
      // Reset form and close modal
      resetForm();
      onClose();
      
    } catch (err) {
      console.error('Error creating compliance monitor:', err);
      setError(err.message || 'Failed to create compliance monitor');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      model_or_system: '',
      threshold_value: 0.8,
    });
    setError(null);
  };
  
  // Model types suggestions for dropdown
  const modelTypes = [
    'Large Language Model',
    'Computer Vision Model',
    'Recommendation System',
    'Chatbot',
    'ML Decision System',
    'Voice Assistant',
    'Business Intelligence Tool',
    'Data Analytics Platform',
    'AI Service'
  ];
  
  // Handle ESC key to close the modal
  useEffect(() => {
    const handleEscKey = (e) => {
      if (e.key === 'Escape' && show) {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscKey);
    return () => {
      document.removeEventListener('keydown', handleEscKey);
    };
  }, [show, onClose]);
  
  // Handle backdrop click to close the modal
  const handleBackdropClick = (e) => {
    if (e.target.classList.contains('modal') || e.target.classList.contains('modal-backdrop')) {
      onClose();
    }
  };
  
  if (!show) return null;
  
  return (
    <div className="modal-wrapper">
      <div 
        className="modal fade show" 
        style={{ display: 'block' }} 
        tabIndex="-1"
        onClick={handleBackdropClick}
      >
        <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Create Compliance Monitor</h5>
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
                Compliance monitors track key metrics for AI systems to ensure they meet governance requirements.
                When metrics fall outside acceptable thresholds, alerts will be generated.
              </div>
              
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="name" className="form-label">Monitor Name <span className="text-danger">*</span></label>
                  <input
                    type="text"
                    className="form-control"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="e.g., Model Accuracy Monitor, Bias Detection Monitor"
                    required
                  />
                </div>
                
                <div className="mb-3">
                  <label htmlFor="model_or_system" className="form-label">Model/System <span className="text-danger">*</span></label>
                  <input
                    type="text"
                    className="form-control"
                    id="model_or_system"
                    name="model_or_system"
                    list="modelTypesList"
                    value={formData.model_or_system}
                    onChange={handleChange}
                    placeholder="e.g., Customer Service LLM, Recommendation Engine"
                    required
                  />
                  <datalist id="modelTypesList">
                    {modelTypes.map((type, index) => (
                      <option key={index} value={type} />
                    ))}
                  </datalist>
                </div>
                
                <div className="mb-3">
                  <label htmlFor="description" className="form-label">Description</label>
                  <textarea
                    className="form-control"
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    placeholder="Describe what this monitor tracks and why it's important..."
                    rows={3}
                  />
                </div>
                
                <div className="mb-3">
                  <label htmlFor="threshold_value" className="form-label">
                    Threshold Value <span className="text-danger">*</span>
                    <small className="text-muted ms-2">(0-1, where 1 is 100%)</small>
                  </label>
                  <div className="input-group">
                    <input
                      type="range"
                      className="form-range"
                      id="threshold_value_range"
                      min="0"
                      max="1"
                      step="0.01"
                      value={formData.threshold_value}
                      onChange={e => setFormData({...formData, threshold_value: parseFloat(e.target.value)})}
                    />
                    <input
                      type="number"
                      className="form-control ms-2"
                      id="threshold_value"
                      name="threshold_value"
                      min="0"
                      max="1"
                      step="0.01"
                      style={{ width: '80px' }}
                      value={formData.threshold_value}
                      onChange={handleChange}
                      required
                    />
                    <span className="input-group-text">({(formData.threshold_value * 100).toFixed(0)}%)</span>
                  </div>
                  <div className="form-text">
                    Set the threshold at which alerts will be triggered. Values below this threshold will generate alerts.
                  </div>
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
                    Creating...
                  </>
                ) : (
                  'Create Monitor'
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
      <div className="modal-backdrop fade show" onClick={onClose}></div>
    </div>
  );
};

export default MonitorFormModal;