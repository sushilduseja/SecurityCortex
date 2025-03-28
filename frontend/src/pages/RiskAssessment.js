import React, { useState, useEffect } from 'react';
import { fetchRiskAssessments } from '../services/api';
import PageHeader from '../components/common/PageHeader';
import LoadingSpinner from '../components/common/LoadingSpinner';
import StatusBadge from '../components/common/StatusBadge';
import RiskAssessmentFormModal from '../components/risk/RiskAssessmentFormModal';
import RiskAssessmentDetailModal from '../components/risk/RiskAssessmentDetailModal';

const RiskAssessment = () => {
  const [assessments, setAssessments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [selectedAssessmentId, setSelectedAssessmentId] = useState(null);

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

  useEffect(() => {
    loadAssessments();
  }, []);

  const handleCreateAssessment = () => {
    setShowCreateModal(true);
  };

  const handleViewAssessment = (assessmentId) => {
    setSelectedAssessmentId(assessmentId);
    setShowDetailModal(true);
  };

  const handleAssessmentCreated = () => {
    // Reload assessments after creation
    loadAssessments();
  };

  const getRiskLevel = (score) => {
    if (score >= 75) return 'High';
    if (score >= 50) return 'Medium';
    return 'Low';
  };

  const getRiskLevelClass = (level) => {
    switch (level) {
      case 'High':
        return 'danger';
      case 'Medium':
        return 'warning';
      case 'Low':
        return 'success';
      default:
        return 'secondary';
    }
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
        <>
          <div className="card mb-4">
            <div className="card-body">
              <p className="mb-0">
                <i className="fas fa-info-circle me-2 text-primary"></i>
                AI risk assessments identify, evaluate, and mitigate potential risks in AI systems.
                The Risk Assessment Agent analyzes model documentation to provide risk scores and recommendations.
              </p>
            </div>
          </div>

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
                  assessments.map((assessment) => {
                    const riskLevel = getRiskLevel(assessment.risk_score);
                    const riskClass = getRiskLevelClass(riskLevel);
                    
                    return (
                      <tr key={assessment.id}>
                        <td>{assessment.model_name}</td>
                        <td>{assessment.risk_score.toFixed(1)}</td>
                        <td>
                          <StatusBadge status={riskLevel} type={riskClass} />
                        </td>
                        <td>
                          <StatusBadge status={assessment.status} />
                        </td>
                        <td>{new Date(assessment.created_at).toLocaleDateString()}</td>
                        <td>
                          <div className="d-flex gap-2">
                            <button 
                              className="btn btn-sm btn-light" 
                              title="View Details"
                              onClick={() => handleViewAssessment(assessment.id)}
                            >
                              <i className="fas fa-eye"></i>
                            </button>
                            <button className="btn btn-sm btn-light" title="Export Report">
                              <i className="fas fa-file-export"></i>
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </>
      )}

      {/* Create Assessment Modal */}
      <RiskAssessmentFormModal 
        show={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onAssessmentCreated={handleAssessmentCreated}
      />

      {/* View Assessment Details Modal */}
      <RiskAssessmentDetailModal
        show={showDetailModal}
        assessmentId={selectedAssessmentId}
        onClose={() => setShowDetailModal(false)}
      />
    </div>
  );
};

export default RiskAssessment;