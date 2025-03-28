import React from 'react';

const PageHeader = ({ title, subtitle, actions }) => {
  return (
    <div className="page-header mb-4">
      <div className="d-flex flex-wrap justify-content-between align-items-center">
        <div>
          <h2 className="page-title mb-1">{title}</h2>
          {subtitle && <p className="text-muted mb-0">{subtitle}</p>}
        </div>
        {actions && (
          <div className="page-actions d-flex flex-wrap gap-2">
            {actions}
          </div>
        )}
      </div>
    </div>
  );
};

export default PageHeader;