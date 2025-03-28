import React, { useState, useEffect } from 'react';
import { fetchPolicies } from '../services/api';
import PageHeader from '../components/common/PageHeader';
import LoadingSpinner from '../components/common/LoadingSpinner';
import StatusBadge from '../components/common/StatusBadge';

const Governance = () => {
  const [policies, setPolicies] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadPolicies = async () => {
      try {
        setIsLoading(true);
        const data = await fetchPolicies();
        setPolicies(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching policies:', err);
        setError('Failed to load governance policies');
      } finally {
        setIsLoading(false);
      }
    };

    loadPolicies();
  }, []);

  const handleCreatePolicy = () => {
    // Handle policy creation - open modal, redirect to form, etc.
    console.log('Create policy clicked');
  };

  if (isLoading) {
    return <LoadingSpinner message="Loading governance policies..." />;
  }

  return (
    <div className="governance-container">
      <PageHeader 
        title="Governance Policies" 
        subtitle="Manage and monitor your AI governance policies"
        actions={
          <button 
            className="btn btn-primary" 
            onClick={handleCreatePolicy}
          >
            <i className="fas fa-plus me-2"></i>
            Create Policy
          </button>
        }
      />

      {error ? (
        <div className="alert alert-danger">
          <i className="fas fa-exclamation-circle me-2"></i>
          {error}
        </div>
      ) : (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Category</th>
                <th>Status</th>
                <th>Created</th>
                <th>Updated</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {policies.length === 0 ? (
                <tr>
                  <td colSpan={6} className="text-center py-4">No policies found</td>
                </tr>
              ) : (
                policies.map((policy) => (
                  <tr key={policy.id}>
                    <td>{policy.title}</td>
                    <td>{policy.category}</td>
                    <td>
                      <StatusBadge status={policy.status} />
                    </td>
                    <td>{new Date(policy.created_at).toLocaleDateString()}</td>
                    <td>{new Date(policy.updated_at).toLocaleDateString()}</td>
                    <td>
                      <div className="d-flex gap-2">
                        <button className="btn btn-sm btn-light" title="View">
                          <i className="fas fa-eye"></i>
                        </button>
                        <button className="btn btn-sm btn-light" title="Edit">
                          <i className="fas fa-edit"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Governance;