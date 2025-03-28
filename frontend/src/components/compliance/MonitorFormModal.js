import React, { useState } from 'react';
import { createComplianceMonitor } from '../../services/api';

const MonitorFormModal = ({ show, onClose, onMonitorCreated }) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [modelOrSystem, setModelOrSystem] = useState('');
  const [thresholdValue, setThresholdValue] = useState(0.8);
  const [error, setError] = useState(null);
  
  // Standard compliance metrics from backend
  const standardMetrics = [
    {
      name: "Data Privacy Compliance",
      description: "Monitors compliance with data privacy policies and regulations",
      threshold: 0.9
    },
    {
      name: "Fairness Metric",
      description: "Monitors fairness across different demographic groups",
      threshold: 0.85
    },
    {
      name: "Explainability Index",
      description: "Tracks the explainability level of model decisions",
      threshold: 0.7
    },
    {
      name: "Security Control Compliance",
      description: "Monitors adherence to security controls and policies",
      threshold: 0.95
    },
    {
      name: "Documentation Completeness",
      description: "Tracks the completeness of model documentation",
      threshold: 0.8
    },
    {
      name: "Model Performance Stability",
      description: "Monitors stability of model performance over time",
      threshold: 0.9
    },
    {
      name: "Data Drift Detection",
      description: "Monitors for drift in input data distribution",
      threshold: 0.05
    },
    {
      name: "Human Oversight Confirmation",
      description: "Tracks the percentage of decisions reviewed by humans",
      threshold: 0.25
    }
  ];
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!name.trim() || !description.trim() || !modelOrSystem.trim() || thresholdValue === null) {
      setError('Please fill in all required fields');
      return;
    }
    
    if (thresholdValue < 0 || thresholdValue > 1) {
      setError('Threshold value must be between 0 and 1');
      return;
    }
    
    setIsSubmitting(true);
    setError(null);
    
    try {
      const monitor = {
        name,
        description,
        model_or_system: modelOrSystem,
        threshold_value: Number(thresholdValue)
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
    setName('');
    setDescription('');
    setModelOrSystem('');
    setThresholdValue(0.8);
    setError(null);
  };
  
  const handleSelectPreset = (preset) => {
    setName(preset.name);
    setDescription(preset.description);
    setThresholdValue(preset.threshold);
  };
  
  if (!show) return null;
  
  return (
    <div className="modal fade show" style={{ display: 'block' }} tabIndex="-1">
      <div className="modal-dialog modal-lg">
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
            
            <div className="alert alert-info mb-3">
              <i className="fas fa-info-circle me-2"></i>
              Compliance monitors track key metrics to ensure AI systems meet governance requirements.
            </div>
            
            <div className="row mb-4">
              <div className="col-12">
                <label className="form-label">Quick Start: Select Standard Metric</label>
                <div className="d-flex flex-wrap gap-2">
                  {standardMetrics.map((metric, index) => (
                    <button
                      key={index}
                      type="button"
                      className="btn btn-sm btn-outline-secondary"
                      onClick={() => handleSelectPreset(metric)}
                      title={metric.description}
                    >
                      {metric.name}
                    </button>
                  ))}
                </div>
              </div>
            </div>
            
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label htmlFor="name" className="form-label">Monitor Name <span className="text-danger">*</span></label>
                <input
                  type="text"
                  className="form-control"
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
              
              <div className="mb-3">
                <label htmlFor="description" className="form-label">Description <span className="text-danger">*</span></label>
                <textarea
                  className="form-control"
                  id="description"
                  rows="2"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  required
                ></textarea>
              </div>
              
              <div className="mb-3">
                <label htmlFor="modelOrSystem" className="form-label">Model or System <span className="text-danger">*</span></label>
                <input
                  type="text"
                  className="form-control"
                  id="modelOrSystem"
                  value={modelOrSystem}
                  onChange={(e) => setModelOrSystem(e.target.value)}
                  required
                  placeholder="e.g., SentimentAnalyzer-v2, ProductRecommender, etc."
                />
              </div>
              
              <div className="mb-3">
                <label htmlFor="thresholdValue" className="form-label">
                  Threshold Value <span className="text-danger">*</span>
                  <small className="text-muted ms-2">(0-1)</small>
                </label>
                <div className="input-group">
                  <input
                    type="number"
                    className="form-control"
                    id="thresholdValue"
                    value={thresholdValue}
                    onChange={(e) => setThresholdValue(e.target.value)}
                    required
                    min="0"
                    max="1"
                    step="0.05"
                  />
                  <span className="input-group-text">
                    {thresholdValue * 100}%
                  </span>
                </div>
                <div className="form-text">
                  Set the threshold that determines when an alert will be triggered.
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
      <div className="modal-backdrop fade show"></div>
    </div>
  );
};

export default MonitorFormModal;