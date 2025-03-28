import React from 'react';

const LoadingSpinner = ({ size, message }) => {
  return (
    <div className="spinner-container">
      <div className="d-flex flex-column align-items-center">
        <div className="spinner" style={{ 
          width: size || '40px', 
          height: size || '40px' 
        }}></div>
        {message && <p className="mt-3 text-muted">{message}</p>}
      </div>
    </div>
  );
};

export default LoadingSpinner;