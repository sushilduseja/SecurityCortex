import React, { useState } from 'react';
import { gsap } from 'gsap';
import PageHeader from '../components/common/PageHeader';
import MetricCard from '../components/dashboard/MetricCard';
import ComplianceStatusChart from '../components/dashboard/ComplianceStatusChart';
import RiskDistributionChart from '../components/dashboard/RiskDistributionChart';
import RecentActivities from '../components/dashboard/RecentActivities';
import LoadingSpinner from '../components/common/LoadingSpinner';
import NotificationModal from '../components/notifications/NotificationModal';

// Animate dashboard components on mount
const animateDashboard = () => {
  gsap.fromTo(
    '.dashboard-metrics .col-md-3',
    { y: 50, opacity: 0 },
    { 
      y: 0, 
      opacity: 1, 
      stagger: 0.1, 
      duration: 0.6,
      ease: 'power2.out',
    }
  );

  gsap.fromTo(
    '.dashboard-charts .col-md-6',
    { y: 50, opacity: 0 },
    { 
      y: 0, 
      opacity: 1, 
      stagger: 0.1, 
      duration: 0.6,
      delay: 0.3,
      ease: 'power2.out',
    }
  );

  gsap.fromTo(
    '.dashboard-activities',
    { y: 50, opacity: 0 },
    { 
      y: 0, 
      opacity: 1, 
      duration: 0.6,
      delay: 0.5,
      ease: 'power2.out',
    }
  );
};

const Dashboard = ({ metrics = {}, isLoading }) => {
  const [showNotificationModal, setShowNotificationModal] = useState(false);
  const [notificationTarget, setNotificationTarget] = useState(null);
  
  const {
    policy_count = 0,
    avg_risk_score = 0,
    compliance_rate = 0,
    active_monitors = 0,
    deltas = {
      policy_count: 0,
      avg_risk_score: 0,
      compliance_rate: 0,
      active_monitors: 0
    }
  } = metrics;

  React.useEffect(() => {
    animateDashboard();
  }, []);
  
  const handleOpenNotificationModal = (entityType, alertType) => {
    setNotificationTarget({
      entityType: entityType,
      entityName: `${entityType} Alert`,
      initialData: {
        notification_type: alertType || 'custom'
      }
    });
    setShowNotificationModal(true);
  };

  if (isLoading) {
    return <LoadingSpinner message="Loading dashboard data..." />;
  }

  return (
    <div className="dashboard-container">
      <PageHeader 
        title="AI Governance Dashboard" 
        subtitle="Monitor your AI governance metrics and activities"
      />
      
      <div className="mb-4 d-flex justify-content-end">
        <div className="dropdown">
          <button className="btn btn-primary dropdown-toggle" type="button" id="notificationDropdown" data-bs-toggle="dropdown" aria-expanded="false">
            <i className="fas fa-bell me-2"></i> Send Notification
          </button>
          <ul className="dropdown-menu" aria-labelledby="notificationDropdown">
            <li>
              <button 
                className="dropdown-item" 
                onClick={() => handleOpenNotificationModal('Compliance', 'compliance_alert')}
              >
                <i className="fas fa-check-square me-2"></i> Compliance Alert
              </button>
            </li>
            <li>
              <button 
                className="dropdown-item" 
                onClick={() => handleOpenNotificationModal('Risk', 'risk_assessment')}
              >
                <i className="fas fa-exclamation-triangle me-2"></i> Risk Assessment Update
              </button>
            </li>
            <li>
              <button 
                className="dropdown-item" 
                onClick={() => handleOpenNotificationModal('System', 'custom')}
              >
                <i className="fas fa-envelope me-2"></i> Custom Message
              </button>
            </li>
          </ul>
        </div>
      </div>
      
      <div className="dashboard-metrics row mb-4">
        <div className="col-md-3 col-sm-6 mb-4 mb-md-0">
          <MetricCard 
            title="Governance Policies" 
            value={policy_count} 
            delta={deltas.policy_count} 
            icon="sitemap"
          />
        </div>
        <div className="col-md-3 col-sm-6 mb-4 mb-md-0">
          <MetricCard 
            title="Avg. Risk Score" 
            value={avg_risk_score} 
            delta={deltas.avg_risk_score} 
            icon="exclamation-triangle"
          />
        </div>
        <div className="col-md-3 col-sm-6 mb-4 mb-md-0">
          <MetricCard 
            title="Compliance Rate" 
            value={`${compliance_rate}%`} 
            delta={deltas.compliance_rate} 
            icon="check-square"
          />
        </div>
        <div className="col-md-3 col-sm-6">
          <MetricCard 
            title="Active Monitors" 
            value={active_monitors} 
            delta={deltas.active_monitors} 
            icon="eye"
          />
        </div>
      </div>
      
      {/* Notification Modal */}
      <NotificationModal
        show={showNotificationModal}
        onClose={() => setShowNotificationModal(false)}
        title={notificationTarget ? `Send ${notificationTarget.entityName} Notification` : 'Send Notification'}
        entityType={notificationTarget?.entityType}
        entityName={notificationTarget?.entityName}
        initialData={notificationTarget?.initialData}
      />
      
      <div className="dashboard-charts row mb-4">
        <div className="col-md-6 mb-4 mb-md-0">
          <div className="card h-100">
            <div className="card-body">
              <h5 className="card-title mb-4">Compliance Status</h5>
              <ComplianceStatusChart />
            </div>
          </div>
        </div>
        <div className="col-md-6">
          <div className="card h-100">
            <div className="card-body">
              <h5 className="card-title mb-4">Risk Distribution</h5>
              <RiskDistributionChart />
            </div>
          </div>
        </div>
      </div>
      
      <div className="dashboard-activities row">
        <div className="col-12">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title mb-4">Recent Activities</h5>
              <RecentActivities />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;