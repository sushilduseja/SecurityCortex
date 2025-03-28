import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import { gsap } from 'gsap';

// Layout components
import Sidebar from './components/layout/Sidebar';
import Header from './components/layout/Header';

// Page components
import Dashboard from './pages/Dashboard';
import Governance from './pages/Governance';
import RiskAssessment from './pages/RiskAssessment';
import Compliance from './pages/Compliance';
import Reports from './pages/Reports';

// Service imports
import { fetchDashboardMetrics } from './services/api';

const App = () => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [dashboardMetrics, setDashboardMetrics] = useState({
    policy_count: 0,
    avg_risk_score: 0,
    compliance_rate: 0,
    active_monitors: 0,
    deltas: {
      policy_count: 0,
      avg_risk_score: 0,
      compliance_rate: 0,
      active_monitors: 0
    }
  });

  useEffect(() => {
    // Initialize GSAP animations
    gsap.config({
      nullTargetWarn: false,
    });
    
    // Fetch initial dashboard data
    const fetchInitialData = async () => {
      try {
        setIsLoading(true);
        const metricsData = await fetchDashboardMetrics();
        setDashboardMetrics(metricsData);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchInitialData();
    
    // Set up polling for real-time updates (every 30 seconds)
    const interval = setInterval(async () => {
      try {
        const metricsData = await fetchDashboardMetrics();
        setDashboardMetrics(metricsData);
      } catch (error) {
        console.error('Error fetching dashboard updates:', error);
      }
    }, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  return (
    <div className={`app-container ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
      <Sidebar collapsed={sidebarCollapsed} />
      <div className="main-content">
        <Header toggleSidebar={toggleSidebar} />
        <div className="content-wrapper">
          <Routes>
            <Route path="/" element={<Dashboard metrics={dashboardMetrics} isLoading={isLoading} />} />
            <Route path="/governance" element={<Governance />} />
            <Route path="/risk-assessment" element={<RiskAssessment />} />
            <Route path="/compliance" element={<Compliance />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
        </div>
      </div>
    </div>
  );
};

export default App;