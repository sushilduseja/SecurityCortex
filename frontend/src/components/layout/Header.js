import React from 'react';

const Header = ({ toggleSidebar }) => {
  return (
    <div className="header">
      <div className="d-flex justify-content-between align-items-center w-100">
        <div>
          <button 
            onClick={toggleSidebar}
            className="btn btn-sm btn-light me-3"
          >
            <i className="fas fa-bars"></i>
          </button>
          <span className="d-none d-md-inline">AI Governance Dashboard</span>
        </div>
        
        <div className="d-flex align-items-center">
          <div className="dropdown me-3">
            <button 
              className="btn btn-sm btn-light position-relative"
              type="button" 
              id="notificationsDropdown" 
              data-bs-toggle="dropdown" 
              aria-expanded="false"
            >
              <i className="fas fa-bell"></i>
              <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                3
              </span>
            </button>
            <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="notificationsDropdown">
              <li><h6 className="dropdown-header">Notifications</h6></li>
              <li><hr className="dropdown-divider" /></li>
              <li><a className="dropdown-item" href="#"><i className="fas fa-exclamation-triangle text-warning me-2"></i> New high-risk assessment</a></li>
              <li><a className="dropdown-item" href="#"><i className="fas fa-clipboard-check text-success me-2"></i> Compliance report ready</a></li>
              <li><a className="dropdown-item" href="#"><i className="fas fa-bell text-info me-2"></i> Policy update due</a></li>
            </ul>
          </div>
          
          <div className="dropdown">
            <button 
              className="btn btn-sm btn-light d-flex align-items-center" 
              type="button" 
              id="userDropdown" 
              data-bs-toggle="dropdown" 
              aria-expanded="false"
            >
              <div className="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center me-2" style={{ width: '32px', height: '32px' }}>
                <span>AD</span>
              </div>
              <span className="d-none d-md-block">Admin</span>
              <i className="fas fa-chevron-down ms-2"></i>
            </button>
            <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
              <li><a className="dropdown-item" href="#"><i className="fas fa-user me-2"></i> Profile</a></li>
              <li><a className="dropdown-item" href="#"><i className="fas fa-cog me-2"></i> Settings</a></li>
              <li><hr className="dropdown-divider" /></li>
              <li><a className="dropdown-item" href="#"><i className="fas fa-sign-out-alt me-2"></i> Logout</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header;