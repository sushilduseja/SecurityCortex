import React, { useEffect, useRef } from 'react';
import { gsap } from 'gsap';

// Function to get card color theme based on icon
const getCardTheme = (icon) => {
  switch (icon) {
    case 'sitemap': // Governance Policies
      return {
        gradient: 'linear-gradient(135deg, #4158D0 0%, #C850C0 100%)',
        iconColor: '#b388ff',
        shadow: '0 4px 20px rgba(79, 64, 201, 0.15)'
      };
    case 'exclamation-triangle': // Risk Score
      return {
        gradient: 'linear-gradient(135deg, #ff9966 0%, #ff5e62 100%)',
        iconColor: '#ff7043',
        shadow: '0 4px 20px rgba(255, 94, 98, 0.15)'
      };
    case 'check-square': // Compliance Rate
      return {
        gradient: 'linear-gradient(135deg, #43cea2 0%, #185a9d 100%)',
        iconColor: '#26a69a',
        shadow: '0 4px 20px rgba(67, 206, 162, 0.15)'
      };
    case 'eye': // Active Monitors
      return {
        gradient: 'linear-gradient(135deg, #5b86e5 0%, #36d1dc 100%)',
        iconColor: '#42a5f5',
        shadow: '0 4px 20px rgba(91, 134, 229, 0.15)'
      };
    default:
      return {
        gradient: 'linear-gradient(135deg, #3b4371 0%, #f3904f 100%)',
        iconColor: '#7986cb',
        shadow: '0 4px 20px rgba(59, 67, 113, 0.15)'
      };
  }
};

const MetricCard = ({ title, value, delta, icon, bgGradient }) => {
  const cardRef = useRef(null);
  const valueRef = useRef(null);
  const prevValue = useRef(value);
  const theme = getCardTheme(icon);

  // Animate value changes
  useEffect(() => {
    if (valueRef.current && prevValue.current !== value) {
      gsap.fromTo(
        valueRef.current,
        { opacity: 0.6, y: -10 },
        { 
          opacity: 1, 
          y: 0,
          duration: 0.5,
          ease: 'power2.out'
        }
      );
      
      prevValue.current = value;
    }
  }, [value]);

  // Add hover animation
  useEffect(() => {
    if (cardRef.current) {
      cardRef.current.addEventListener('mouseenter', handleMouseEnter);
      cardRef.current.addEventListener('mouseleave', handleMouseLeave);
    }
    
    return () => {
      if (cardRef.current) {
        cardRef.current.removeEventListener('mouseenter', handleMouseEnter);
        cardRef.current.removeEventListener('mouseleave', handleMouseLeave);
      }
    };
  }, []);

  const handleMouseEnter = () => {
    gsap.to(cardRef.current, {
      y: -5,
      scale: 1.02,
      boxShadow: theme.shadow.replace('0.15', '0.25'),
      duration: 0.3,
      ease: 'power2.out'
    });
  };

  const handleMouseLeave = () => {
    gsap.to(cardRef.current, {
      y: 0,
      scale: 1,
      boxShadow: theme.shadow,
      duration: 0.3,
      ease: 'power2.out'
    });
  };

  const deltaDisplay = delta !== 0 ? (
    <span className={`widget-delta ${delta > 0 ? 'positive' : delta < 0 ? 'negative' : ''}`}>
      <i className={`fas fa-${delta > 0 ? 'arrow-up' : delta < 0 ? 'arrow-down' : 'minus'}`}></i>
      {Math.abs(delta).toFixed(delta % 1 === 0 ? 0 : 1)}%
    </span>
  ) : null;

  return (
    <div 
      ref={cardRef}
      className="card border-0 h-100" 
      style={{ 
        boxShadow: theme.shadow,
        transition: 'all 0.3s ease'
      }}
    >
      <div className="card-body">
        <div className="d-flex align-items-center mb-3">
          <div 
            className="icon-circle me-3" 
            style={{ 
              backgroundColor: 'rgba(255, 255, 255, 0.9)',
              width: '45px',
              height: '45px',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <i 
              className={`fas fa-${icon}`} 
              style={{ 
                fontSize: '1.5rem', 
                color: theme.iconColor
              }}
            ></i>
          </div>
          <h6 className="mb-0 text-muted">{title}</h6>
        </div>
        
        <div className="d-flex align-items-baseline">
          <h2 
            ref={valueRef} 
            className="display-6 mb-0 fw-bold" 
            style={{ color: '#333' }}
          >
            {typeof value === 'number' && value % 1 !== 0 ? value.toFixed(1) : value}
          </h2>
          {deltaDisplay && (
            <div 
              className="ms-2" 
              style={{ 
                color: delta > 0 ? '#2ecc71' : delta < 0 ? '#e74c3c' : '#7f8c8d',
                fontSize: '0.9rem',
                fontWeight: 'bold'
              }}
            >
              <i className={`fas fa-${delta > 0 ? 'arrow-up' : delta < 0 ? 'arrow-down' : 'minus'} me-1`}></i>
              {Math.abs(delta).toFixed(delta % 1 === 0 ? 0 : 1)}%
            </div>
          )}
        </div>
        
        <div 
          className="progress mt-3" 
          style={{ height: '3px', backgroundColor: 'rgba(0,0,0,0.05)' }}
        >
          <div 
            className="progress-bar" 
            role="progressbar" 
            style={{ 
              width: `${typeof value === 'number' ? Math.min(100, value) : 50}%`,
              background: theme.gradient
            }} 
            aria-valuenow={typeof value === 'number' ? value : 50} 
            aria-valuemin="0" 
            aria-valuemax="100"
          ></div>
        </div>
      </div>
    </div>
  );
};

export default MetricCard;