import React, { useState } from 'react';
import { createPolicy } from '../../services/api';
import Modal from '../common/Modal';

const PolicyFormModal = ({ show, onClose, onPolicyCreated }) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('Data Privacy');
  const [description, setDescription] = useState('');
  const [content, setContent] = useState('');
  const [error, setError] = useState(null);
  
  // Policy categories aligned with backend GovernanceAgent
  const policyCategories = [
    "Data Privacy", 
    "Model Transparency", 
    "Ethical AI", 
    "Bias Mitigation",
    "Security", 
    "Compliance",
    "Accountability",
    "Human Oversight"
  ];
  
  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    
    if (!title.trim() || !category || !description.trim()) {
      setError('Please fill in all required fields');
      return;
    }
    
    setIsSubmitting(true);
    setError(null);
    
    try {
      const policy = {
        title,
        category,
        description,
        content,
        status: 'Draft'
      };
      
      const response = await createPolicy(policy);
      
      if (onPolicyCreated) {
        onPolicyCreated(response);
      }
      
      // Reset form and close modal
      resetForm();
      onClose();
      
    } catch (err) {
      console.error('Error creating policy:', err);
      setError(err.message || 'Failed to create policy');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  const resetForm = () => {
    setTitle('');
    setCategory('Data Privacy');
    setDescription('');
    setContent('');
    setError(null);
  };
  
  // Handle generating a policy using the AI agent
  const handleGeneratePolicy = () => {
    // Placeholder for AI-powered policy generation
    // This would make an API call to the backend governance agent
    
    // For now, we'll add a template based on the selected category
    const templates = {
      "Data Privacy": "Data Privacy Policy for AI Systems\n\n## Purpose\nThis policy establishes guidelines for protecting personal data in AI systems.\n\n## Requirements\n1. All AI systems must implement privacy by design\n2. Personal data must be minimized and protected\n3. Regular privacy impact assessments must be conducted",
      "Model Transparency": "Model Transparency Policy for AI Systems\n\n## Purpose\nThis policy defines requirements for making AI models transparent and explainable.\n\n## Requirements\n1. All AI systems must provide explanations for key decisions\n2. Technical documentation must describe model functioning\n3. User interfaces must communicate model confidence levels",
      "Ethical AI": "Ethical AI Policy\n\n## Purpose\nThis policy outlines ethical principles guiding AI development and deployment.\n\n## Requirements\n1. AI systems must be designed to benefit humanity\n2. AI systems must not perpetuate unjust bias\n3. Ethical review must be conducted throughout development",
    };
    
    setContent(templates[category] || "# Policy Content\n\nEnter detailed policy content here...");
  };
  
  const modalContent = (
    <>
      {error && (
        <div className="alert alert-danger">{error}</div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="title" className="form-label">Policy Title <span className="text-danger">*</span></label>
          <input
            type="text"
            className="form-control"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>
        
        <div className="mb-3">
          <label htmlFor="category" className="form-label">Category <span className="text-danger">*</span></label>
          <select
            className="form-select"
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            required
          >
            {policyCategories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
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
          <div className="d-flex justify-content-between align-items-center mb-2">
            <label htmlFor="content" className="form-label">Policy Content</label>
            <button 
              type="button"
              className="btn btn-sm btn-outline-primary"
              onClick={handleGeneratePolicy}
            >
              <i className="fas fa-magic me-1"></i> Generate with AI
            </button>
          </div>
          <textarea
            className="form-control"
            id="content"
            rows="12"
            value={content}
            onChange={(e) => setContent(e.target.value)}
          ></textarea>
          <div className="form-text">
            Use Markdown format for rich text formatting
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
            Creating...
          </>
        ) : (
          'Create Policy'
        )}
      </button>
    </>
  );
  
  return (
    <Modal
      show={show}
      onClose={onClose}
      title="Create Governance Policy"
      size="lg"
      actions={modalActions}
      closeOnBackdropClick={true}
      closeOnEscape={true}
    >
      {modalContent}
    </Modal>
  );
};

export default PolicyFormModal;