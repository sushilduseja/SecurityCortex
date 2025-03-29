import React, { useState, useEffect } from 'react';
import { gsap } from 'gsap';
import PageHeader from '../components/common/PageHeader';
import MetricCard from '../components/dashboard/MetricCard';
import ComplianceStatusChart from '../components/dashboard/ComplianceStatusChart';
import RiskDistributionChart from '../components/dashboard/RiskDistributionChart';
import RecentActivities from '../components/dashboard/RecentActivities';
import LoadingSpinner from '../components/common/LoadingSpinner';

// Animate dashboard components with enhanced effects
const animateDashboard = () => {
  // Clear any existing animations
  gsap.killTweensOf('.dashboard-container *');
  
  // Main container fade in
  gsap.fromTo(
    '.dashboard-container',
    { opacity: 0 },
    { 
      opacity: 1, 
      duration: 0.5,
      ease: 'power2.out',
    }
  );
  
  // Staggered animation for metric cards
  gsap.fromTo(
    '.dashboard-metrics .metric-card',
    { y: 30, opacity: 0, scale: 0.95 },
    { 
      y: 0, 
      opacity: 1, 
      scale: 1,
      stagger: 0.08, 
      duration: 0.6,
      ease: 'back.out(1.4)',
    }
  );

  // Animated entrance for charts
  gsap.fromTo(
    '.chart-card',
    { y: 40, opacity: 0 },
    { 
      y: 0, 
      opacity: 1, 
      stagger: 0.15, 
      duration: 0.7,
      delay: 0.2,
      ease: 'power2.out',
    }
  );

  // Timeline animation for activity section
  gsap.fromTo(
    '.dashboard-activities',
    { y: 30, opacity: 0 },
    { 
      y: 0, 
      opacity: 1, 
      duration: 0.6,
      delay: 0.4,
      ease: 'power2.out',
    }
  );
};

const Dashboard = ({ metrics = {}, isLoading }) => {
  const [activeTab, setActiveTab] = useState('overview'); // 'overview', 'compliance', 'risk'
  const [collapsed, setCollapsed] = useState(false);
  
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

  useEffect(() => {
    animateDashboard();
  }, [activeTab]);

  if (isLoading) {
    return <LoadingSpinner message="Loading dashboard data..." />;
  }
  
  const renderMetricCards = () => (
    <div className="dashboard-metrics row">
      <div className="col-lg-3 col-md-6 col-sm-6 mb-4">
        <div className="metric-card">
          <MetricCard 
            title="Governance Policies" 
            value={policy_count} 
            delta={deltas.policy_count} 
            icon="sitemap"
          />
        </div>
      </div>
      <div className="col-lg-3 col-md-6 col-sm-6 mb-4">
        <div className="metric-card">
          <MetricCard 
            title="Avg. Risk Score" 
            value={avg_risk_score} 
            delta={deltas.avg_risk_score} 
            icon="exclamation-triangle"
          />
        </div>
      </div>
      <div className="col-lg-3 col-md-6 col-sm-6 mb-4">
        <div className="metric-card">
          <MetricCard 
            title="Compliance Rate" 
            value={`${compliance_rate}%`} 
            delta={deltas.compliance_rate} 
            icon="check-square"
          />
        </div>
      </div>
      <div className="col-lg-3 col-md-6 col-sm-6 mb-4">
        <div className="metric-card">
          <MetricCard 
            title="Active Monitors" 
            value={active_monitors} 
            delta={deltas.active_monitors} 
            icon="eye"
          />
        </div>
      </div>
    </div>
  );
  
  const renderOverviewContent = () => (
    <>
      {renderMetricCards()}
      
      <div className="dashboard-charts row mb-4">
        <div className="col-lg-6 mb-4">
          <div className="card h-100 border-0 shadow-sm chart-card">
            <div className="card-header bg-white border-0 pb-0 pt-3">
              <div className="d-flex justify-content-between align-items-center">
                <h5 className="card-title mb-0">
                  <i className="fas fa-check-circle text-primary me-2"></i>
                  Compliance Status
                </h5>
                <div className="chart-actions">
                  <button 
                    className="btn btn-sm btn-outline-primary me-2"
                    onClick={() => setActiveTab('compliance')}
                  >
                    <i className="fas fa-expand-alt me-1"></i>
                    Expand
                  </button>
                  <div className="dropdown d-inline-block">
                    <button className="btn btn-sm btn-outline-secondary border-0" type="button" id="complianceOptions" data-bs-toggle="dropdown" aria-expanded="false">
                      <i className="fas fa-ellipsis-v"></i>
                    </button>
                    <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="complianceOptions">
                      <li><button className="dropdown-item" type="button"><i className="fas fa-file-export me-2"></i>Export</button></li>
                      <li><button className="dropdown-item" type="button"><i className="fas fa-redo-alt me-2"></i>Refresh</button></li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
            <div className="card-body pt-2">
              <ComplianceStatusChart />
            </div>
          </div>
        </div>
        <div className="col-lg-6 mb-4">
          <div className="card h-100 border-0 shadow-sm chart-card">
            <div className="card-header bg-white border-0 pb-0 pt-3">
              <div className="d-flex justify-content-between align-items-center">
                <h5 className="card-title mb-0">
                  <i className="fas fa-chart-bar text-warning me-2"></i>
                  Risk Distribution
                </h5>
                <div className="chart-actions">
                  <button 
                    className="btn btn-sm btn-outline-primary me-2"
                    onClick={() => setActiveTab('risk')}
                  >
                    <i className="fas fa-expand-alt me-1"></i>
                    Expand
                  </button>
                  <div className="dropdown d-inline-block">
                    <button className="btn btn-sm btn-outline-secondary border-0" type="button" id="riskOptions" data-bs-toggle="dropdown" aria-expanded="false">
                      <i className="fas fa-ellipsis-v"></i>
                    </button>
                    <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="riskOptions">
                      <li><button className="dropdown-item" type="button"><i className="fas fa-file-export me-2"></i>Export</button></li>
                      <li><button className="dropdown-item" type="button"><i className="fas fa-redo-alt me-2"></i>Refresh</button></li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
            <div className="card-body pt-2">
              <RiskDistributionChart />
            </div>
          </div>
        </div>
      </div>
      
      <div className="dashboard-activities row">
        <div className="col-12">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-0 pb-0 pt-3">
              <div className="d-flex justify-content-between align-items-center">
                <h5 className="card-title mb-0">
                  <i className="fas fa-history text-info me-2"></i>
                  Recent Activities
                </h5>
                <div className="dropdown">
                  <button 
                    className="btn btn-sm btn-link text-muted p-0 me-2" 
                    onClick={() => setCollapsed(!collapsed)}
                  >
                    <i className={`fas fa-chevron-${collapsed ? 'down' : 'up'}`}></i>
                  </button>
                  <button className="btn btn-sm btn-outline-secondary border-0" type="button" id="activityOptions" data-bs-toggle="dropdown" aria-expanded="false">
                    <i className="fas fa-ellipsis-v"></i>
                  </button>
                  <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="activityOptions">
                    <li><button className="dropdown-item" type="button"><i className="fas fa-filter me-2"></i>Filter</button></li>
                    <li><button className="dropdown-item" type="button"><i className="fas fa-sync me-2"></i>Refresh</button></li>
                    <li><button className="dropdown-item" type="button"><i className="fas fa-external-link-alt me-2"></i>View All</button></li>
                  </ul>
                </div>
              </div>
            </div>
            {!collapsed && (
              <div className="card-body pt-2">
                <RecentActivities />
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
  
  const renderComplianceContent = () => (
    <div className="row">
      <div className="col-12 mb-4">
        <div className="card border-0 shadow-sm">
          <div className="card-header bg-white border-0 pb-0 pt-3">
            <div className="d-flex justify-content-between align-items-center">
              <h5 className="card-title mb-0">
                <i className="fas fa-check-circle text-primary me-2"></i>
                Detailed Compliance Status
              </h5>
              <button 
                className="btn btn-sm btn-outline-secondary"
                onClick={() => setActiveTab('overview')}
              >
                <i className="fas fa-arrow-left me-1"></i>
                Back to Dashboard
              </button>
            </div>
          </div>
          <div className="card-body">
            <div className="row">
              <div className="col-md-4 mb-4">
                {renderMetricCards()[2]}
              </div>
              <div className="col-md-8 mb-4">
                <div className="alert alert-info">
                  <i className="fas fa-info-circle me-2"></i>
                  Detailed compliance view showing system-specific compliance status and trends.
                </div>
              </div>
            </div>
            <div style={{ height: '500px' }}>
              <ComplianceStatusChart />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
  
  const renderRiskContent = () => (
    <div className="row">
      <div className="col-12 mb-4">
        <div className="card border-0 shadow-sm">
          <div className="card-header bg-white border-0 pb-0 pt-3">
            <div className="d-flex justify-content-between align-items-center">
              <h5 className="card-title mb-0">
                <i className="fas fa-chart-bar text-warning me-2"></i>
                Detailed Risk Analysis
              </h5>
              <button 
                className="btn btn-sm btn-outline-secondary"
                onClick={() => setActiveTab('overview')}
              >
                <i className="fas fa-arrow-left me-1"></i>
                Back to Dashboard
              </button>
            </div>
          </div>
          <div className="card-body">
            <div className="row">
              <div className="col-md-4 mb-4">
                {renderMetricCards()[1]}
              </div>
              <div className="col-md-8 mb-4">
                <div className="alert alert-warning">
                  <i className="fas fa-exclamation-triangle me-2"></i>
                  Expanded risk view showing detailed risk factors and system-specific assessments.
                </div>
              </div>
            </div>
            <div style={{ height: '500px' }}>
              <RiskDistributionChart />
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="dashboard-container">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <PageHeader 
          title="AI Governance Dashboard" 
          subtitle="Monitor your AI governance metrics and activities"
        />
        
        <div className="dashboard-actions">
          {/* Actions removed */}
        </div>
      </div>
      
      {/* Tab Navigation */}
      {activeTab === 'overview' && (
        <div className="dashboard-tabs mb-4">
          <ul className="nav nav-pills nav-fill">
            <li className="nav-item">
              <button 
                className={`nav-link ${activeTab === 'overview' ? 'active' : ''}`}
                onClick={() => setActiveTab('overview')}
              >
                <i className="fas fa-th-large me-2"></i>
                Overview
              </button>
            </li>
            <li className="nav-item">
              <button 
                className={`nav-link ${activeTab === 'compliance' ? 'active' : ''}`}
                onClick={() => setActiveTab('compliance')}
              >
                <i className="fas fa-check-circle me-2"></i>
                Compliance
              </button>
            </li>
            <li className="nav-item">
              <button 
                className={`nav-link ${activeTab === 'risk' ? 'active' : ''}`}
                onClick={() => setActiveTab('risk')}
              >
                <i className="fas fa-exclamation-triangle me-2"></i>
                Risk Analysis
              </button>
            </li>
          </ul>
        </div>
      )}
      
      {/* Content based on active tab */}
      {activeTab === 'overview' && renderOverviewContent()}
      {activeTab === 'compliance' && renderComplianceContent()}
      {activeTab === 'risk' && renderRiskContent()}
    </div>
  );
};

export default Dashboard;