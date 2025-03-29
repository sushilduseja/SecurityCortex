import React from 'react';

// Function to get report icon based on report type
const getReportTypeIcon = (type) => {
  const lcType = type.toLowerCase();
  
  if (lcType.includes('governance')) {
    return 'sitemap';
  } else if (lcType.includes('risk')) {
    return 'exclamation-triangle';
  } else if (lcType.includes('compliance')) {
    return 'check-square';
  } else if (lcType.includes('comprehensive')) {
    return 'chart-line';
  } else {
    return 'file-alt';
  }
};

// Function to get report color based on report type
const getReportTypeColor = (type) => {
  const lcType = type.toLowerCase();
  
  if (lcType.includes('governance')) {
    return '#4158D0';
  } else if (lcType.includes('risk')) {
    return '#ff5e62';
  } else if (lcType.includes('compliance')) {
    return '#43cea2';
  } else if (lcType.includes('comprehensive')) {
    return '#5b86e5';
  } else {
    return '#3b4371';
  }
};

// Maps report types to their display titles
const reportTypeTitles = {
  "governance_summary": "Governance Summary",
  "risk_assessment_overview": "Risk Assessment Overview",
  "compliance_status": "Compliance Status",
  "comprehensive_report": "Comprehensive Governance Report",
  // For backward compatibility, also handle any old/irregular values
  "Governance Summary": "Governance Summary",
  "Risk Assessment Overview": "Risk Assessment Overview",
  "Compliance Status": "Compliance Status",
  "Comprehensive Governance Report": "Comprehensive Governance Report",
  "comprehensive_governance_report": "Comprehensive Governance Report"
};

// Format the report type to be more readable
const formatReportType = (type) => {
  if (!type) return '';
  
  // First check if we have a direct mapping
  if (reportTypeTitles[type]) {
    return reportTypeTitles[type];
  }
  
  // Otherwise fallback to transform from snake_case or camelCase to Title Case with spaces
  return type
    .replace(/_/g, ' ')  // Replace underscores with spaces
    .replace(/([A-Z])/g, ' $1')  // Add space before capital letters
    .replace(/^\w/, c => c.toUpperCase())  // Capitalize first letter
    .trim();  // Remove any leading/trailing spaces
};

const ReportCard = ({ reportType, count }) => {
  const icon = getReportTypeIcon(reportType);
  const color = getReportTypeColor(reportType);
  const formattedType = formatReportType(reportType);
  
  return (
    <div className="card h-100 border-0 shadow-sm">
      <div className="card-body">
        <h6 className="card-title text-truncate fw-bold">{formattedType}</h6>
        <div className="d-flex align-items-center mt-3">
          <div 
            className="report-icon p-3 rounded me-3 d-flex align-items-center justify-content-center" 
            style={{ 
              backgroundColor: `${color}20`, // 20% opacity of the color
              width: '50px',
              height: '50px'
            }}
          >
            <i 
              className={`fas fa-${icon}`} 
              style={{ 
                color: color,
                fontSize: '1.5rem'
              }}
            ></i>
          </div>
          <div>
            <h3 className="mb-0 fw-bold">{count}</h3>
            <p className="text-muted mb-0">
              {count === 1 ? 'Report' : 'Reports'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReportCard;