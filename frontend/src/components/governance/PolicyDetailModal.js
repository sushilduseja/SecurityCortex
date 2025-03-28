import React, { useState, useEffect } from 'react';
import { fetchPolicy } from '../../services/api';
import LoadingSpinner from '../common/LoadingSpinner';
import StatusBadge from '../common/StatusBadge';

const PolicyDetailModal = ({ show, policyId, onClose }) => {
  const [policy, setPolicy] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadPolicy = async () => {
      if (!policyId || !show) return;
      
      try {
        setIsLoading(true);
        const data = await fetchPolicy(policyId);
        setPolicy(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching policy details:', err);
        setError('Failed to load policy details');
      } finally {
        setIsLoading(false);
      }
    };

    loadPolicy();
  }, [policyId, show]);

  if (!show) return null;

  return (
    <div className="modal fade show" style={{ display: 'block' }} tabIndex="-1">
      <div className="modal-dialog modal-lg">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Policy Details</h5>
            <button 
              type="button" 
              className="btn-close" 
              onClick={onClose}
              aria-label="Close"
            ></button>
          </div>
          <div className="modal-body">
            {isLoading ? (
              <LoadingSpinner message="Loading policy details..." />
            ) : error ? (
              <div className="alert alert-danger">{error}</div>
            ) : policy ? (
              <div className="policy-details">
                <div className="row mb-4">
                  <div className="col-md-8">
                    <h4>{policy.title}</h4>
                    <p className="text-muted">{policy.description}</p>
                  </div>
                  <div className="col-md-4 text-md-end">
                    <div className="mb-2">
                      <StatusBadge status={policy.status} />
                    </div>
                    <small className="text-muted">
                      Category: {policy.category}
                    </small>
                  </div>
                </div>
                
                <div className="card mb-3">
                  <div className="card-header bg-light">
                    <h6 className="mb-0">Policy Content</h6>
                  </div>
                  <div className="card-body">
                    <div className="policy-content">
                      {/* In a real implementation, use a Markdown renderer here */}
                      <pre className="policy-content-pre">{policy.content}</pre>
                    </div>
                  </div>
                </div>
                
                <div className="row mt-4">
                  <div className="col-md-6">
                    <small className="text-muted">
                      Created: {new Date(policy.created_at).toLocaleString()}
                    </small>
                  </div>
                  <div className="col-md-6 text-md-end">
                    <small className="text-muted">
                      Last updated: {new Date(policy.updated_at).toLocaleString()}
                    </small>
                  </div>
                </div>
              </div>
            ) : (
              <div className="alert alert-warning">Policy not found</div>
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
            {policy && (
              <button 
                type="button" 
                className="btn btn-primary"
                // This could link to an edit form in the future
              >
                Edit Policy
              </button>
            )}
          </div>
        </div>
      </div>
      <div className="modal-backdrop fade show"></div>
    </div>
  );
};

export default PolicyDetailModal;