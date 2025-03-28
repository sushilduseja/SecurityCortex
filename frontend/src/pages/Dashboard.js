import React from 'react';
import { gsap } from 'gsap';
import PageHeader from '../components/common/PageHeader';
import MetricCard from '../components/dashboard/MetricCard';
import ComplianceStatusChart from '../components/dashboard/ComplianceStatusChart';
import RiskDistributionChart from '../components/dashboard/RiskDistributionChart';
import RecentActivities from '../components/dashboard/RecentActivities';
import LoadingSpinner from '../components/common/LoadingSpinner';

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

const Dashboard = ({ metrics, isLoading }) => {
  React.useEffect(() => {
    animateDashboard();
  }, []);

  if (isLoading) {
    return <LoadingSpinner message="Loading dashboard data..." />;
  }

  return (
    <div className="dashboard-container">
      <PageHeader 
        title="AI Governance Dashboard" 
        subtitle="Monitor your AI governance metrics and activities"
      />
      
      <div className="dashboard-metrics row mb-4">
        <div className="col-md-3 col-sm-6 mb-4 mb-md-0">
          <MetricCard 
            title="Governance Policies" 
            value={metrics.policy_count} 
            delta={metrics.deltas.policy_count} 
            icon="sitemap"
          />
        </div>
        <div className="col-md-3 col-sm-6 mb-4 mb-md-0">
          <MetricCard 
            title="Avg. Risk Score" 
            value={metrics.avg_risk_score} 
            delta={metrics.deltas.avg_risk_score} 
            icon="exclamation-triangle"
          />
        </div>
        <div className="col-md-3 col-sm-6 mb-4 mb-md-0">
          <MetricCard 
            title="Compliance Rate" 
            value={`${metrics.compliance_rate}%`} 
            delta={metrics.deltas.compliance_rate} 
            icon="check-square"
          />
        </div>
        <div className="col-md-3 col-sm-6">
          <MetricCard 
            title="Active Monitors" 
            value={metrics.active_monitors} 
            delta={metrics.deltas.active_monitors} 
            icon="eye"
          />
        </div>
      </div>
      
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