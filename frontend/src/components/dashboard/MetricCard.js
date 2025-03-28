import React, { useEffect, useRef } from 'react';
import { gsap } from 'gsap';

const MetricCard = ({ title, value, delta, icon, bgGradient }) => {
  const valueRef = useRef(null);
  const prevValue = useRef(value);

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

  const deltaDisplay = delta !== 0 ? (
    <span className={`widget-delta ${delta > 0 ? 'positive' : delta < 0 ? 'negative' : ''}`}>
      <i className={`fas fa-${delta > 0 ? 'arrow-up' : delta < 0 ? 'arrow-down' : 'minus'}`}></i>
      {Math.abs(delta).toFixed(delta % 1 === 0 ? 0 : 1)}%
    </span>
  ) : null;

  return (
    <div className="widget-card" style={bgGradient ? { background: bgGradient } : {}}>
      {icon && (
        <div className="widget-icon">
          <i className={`fas fa-${icon}`}></i>
        </div>
      )}
      <div className="widget-title">{title}</div>
      <div className="widget-value" ref={valueRef}>
        {typeof value === 'number' && value % 1 !== 0 ? value.toFixed(1) : value}
      </div>
      {deltaDisplay}
    </div>
  );
};

export default MetricCard;