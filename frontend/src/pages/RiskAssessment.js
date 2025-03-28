import React, { useState, useEffect } from 'react';
import { fetchRiskAssessments } from '../services/api';
import PageHeader from '../components/common/PageHeader';
import LoadingSpinner from '../components/common/LoadingSpinner';
import StatusBadge from '../components/common/StatusBadge';

const RiskAssessment = () => {
  const [assessments, setAssessments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadAssessments = async () => {
      try {
        setIsLoading(true);
        const data = await fetchRiskAssessments();
        setAssessments(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching risk assessments:', err);
        setError('Failed to load risk assessment data');
      } finally {
        setIsLoading(false);
      }
    };

    loadAssessments();
  }, []);

  const handleCreateAssessment = () => {
    // Handle assessment creation - open modal, redirect to form, etc.
    console.log('Create assessment clicked');
  };

  const getRiskLevel = (score) => {
    if (score >= 7) return 'High';
    if (score >= 4) return 'Medium';
    return 'Low';
  };

  if (isLoading) {
    return <LoadingSpinner message="Loading risk assessments..." />;
  }

  return (
    <div className="risk-assessment-container">
      <PageHeader 
        title="Risk Assessments" 
        subtitle="Evaluate and manage AI system risks"
        actions={
          <button 
            className="btn btn-primary" 
            onClick={handleCreateAssessment}
          >
            <i className="fas fa-plus me-2"></i>
            New Assessment
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
                <th>Model Name</th>
                <th>Risk Score</th>
                <th>Risk Level</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {assessments.length === 0 ? (
                <tr>
                  <td colSpan={6} className="text-center py-4">No risk assessments found</td>
                </tr>
              ) : (
                assessments.map((assessment) => (
                  <tr key={assessment.id}>
                    <td>{assessment.model_name}</td>
                    <td>{assessment.risk_score.toFixed(1)}</td>
                    <td>
                      <StatusBadge status={getRiskLevel(assessment.risk_score)} />
                    </td>
                    <td>
                      <StatusBadge status={assessment.status} />
                    </td>
                    <td>{new Date(assessment.created_at).toLocaleDateString()}</td>
                    <td>
                      <div className="d-flex gap-2">
                        <button className="btn btn-sm btn-light" title="View">
                          <i className="fas fa-eye"></i>
                        </button>
                        <button className="btn btn-sm btn-light" title="Review">
                          <i className="fas fa-clipboard-check"></i>
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

export default RiskAssessment;