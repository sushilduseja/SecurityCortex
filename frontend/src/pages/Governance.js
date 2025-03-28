import React, { useState, useEffect } from 'react';
import { fetchPolicies } from '../services/api';
import PageHeader from '../components/common/PageHeader';
import LoadingSpinner from '../components/common/LoadingSpinner';
import StatusBadge from '../components/common/StatusBadge';
import PolicyFormModal from '../components/governance/PolicyFormModal';
import PolicyDetailModal from '../components/governance/PolicyDetailModal';

const Governance = () => {
  const [policies, setPolicies] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [selectedPolicyId, setSelectedPolicyId] = useState(null);

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

  useEffect(() => {
    loadPolicies();
  }, []);

  const handleCreatePolicy = () => {
    setShowCreateModal(true);
  };

  const handleViewPolicy = (policyId) => {
    setSelectedPolicyId(policyId);
    setShowDetailModal(true);
  };

  const handlePolicyCreated = () => {
    // Reload policies after creation
    loadPolicies();
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
        <>
          <div className="card mb-4">
            <div className="card-body">
              <p className="mb-0">
                <i className="fas fa-info-circle me-2 text-primary"></i>
                AI governance policies establish guidelines for responsible AI development and deployment. 
                Create, review, and enforce policies to ensure ethical AI practices.
              </p>
            </div>
          </div>

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
                          <button 
                            className="btn btn-sm btn-light" 
                            title="View"
                            onClick={() => handleViewPolicy(policy.id)}
                          >
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
        </>
      )}

      {/* Create Policy Modal */}
      <PolicyFormModal 
        show={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onPolicyCreated={handlePolicyCreated}
      />

      {/* View Policy Details Modal */}
      <PolicyDetailModal
        show={showDetailModal}
        policyId={selectedPolicyId}
        onClose={() => setShowDetailModal(false)}
      />
    </div>
  );
};

export default Governance;