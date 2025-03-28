import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = ({ collapsed }) => {
  return (
    <div className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <div className="d-flex flex-column h-100">
        <div className="sidebar-header mb-4">
          <div className="d-flex align-items-center">
            <div className="sidebar-logo me-2">
              <i className="fas fa-robot fa-2x"></i>
            </div>
            <div>
              <h5 className="mb-0">AI Governance</h5>
              <small>Dashboard v1.0</small>
            </div>
          </div>
        </div>

        <div className="sidebar-menu flex-grow-1">
          <div className="menu-section mb-3">
            <h6 className="menu-header text-uppercase fs-7 mb-2 text-white-50">Main</h6>
            <ul className="nav flex-column">
              <li className="nav-item mb-2">
                <NavLink to="/" className={({ isActive }) => `nav-link py-2 px-3 rounded ${isActive ? 'bg-white bg-opacity-10' : ''}`}>
                  <i className="fas fa-tachometer-alt me-2"></i>
                  <span>Dashboard</span>
                </NavLink>
              </li>
              <li className="nav-item mb-2">
                <NavLink to="/governance" className={({ isActive }) => `nav-link py-2 px-3 rounded ${isActive ? 'bg-white bg-opacity-10' : ''}`}>
                  <i className="fas fa-sitemap me-2"></i>
                  <span>Governance</span>
                </NavLink>
              </li>
              <li className="nav-item mb-2">
                <NavLink to="/risk-assessment" className={({ isActive }) => `nav-link py-2 px-3 rounded ${isActive ? 'bg-white bg-opacity-10' : ''}`}>
                  <i className="fas fa-exclamation-triangle me-2"></i>
                  <span>Risk Assessment</span>
                </NavLink>
              </li>
              <li className="nav-item mb-2">
                <NavLink to="/compliance" className={({ isActive }) => `nav-link py-2 px-3 rounded ${isActive ? 'bg-white bg-opacity-10' : ''}`}>
                  <i className="fas fa-check-square me-2"></i>
                  <span>Compliance</span>
                </NavLink>
              </li>
              <li className="nav-item mb-2">
                <NavLink to="/reports" className={({ isActive }) => `nav-link py-2 px-3 rounded ${isActive ? 'bg-white bg-opacity-10' : ''}`}>
                  <i className="fas fa-chart-bar me-2"></i>
                  <span>Reports</span>
                </NavLink>
              </li>
            </ul>
          </div>

          <div className="menu-section mb-3">
            <h6 className="menu-header text-uppercase fs-7 mb-2 text-white-50">Configuration</h6>
            <ul className="nav flex-column">
              <li className="nav-item mb-2">
                <a href="#" className="nav-link py-2 px-3 rounded">
                  <i className="fas fa-cog me-2"></i>
                  <span>Settings</span>
                </a>
              </li>
              <li className="nav-item mb-2">
                <a href="#" className="nav-link py-2 px-3 rounded">
                  <i className="fas fa-user-shield me-2"></i>
                  <span>Permissions</span>
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="sidebar-footer mt-auto pt-3">
          <div className="upgrade-card mb-3 p-3 rounded bg-white bg-opacity-10">
            <h6 className="mb-2">AI Governance Pro</h6>
            <p className="mb-2 small">Unlock advanced features and integrations</p>
            <button className="btn btn-sm btn-light w-100">Upgrade Now</button>
          </div>
          <div className="version-info text-center small">
            <p className="mb-0 text-white-50">Version 1.0.0</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;