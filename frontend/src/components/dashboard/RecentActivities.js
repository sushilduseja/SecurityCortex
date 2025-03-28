import React, { useEffect, useState } from 'react';
import { fetchRecentActivities } from '../../services/api';
import LoadingSpinner from '../common/LoadingSpinner';

const RecentActivities = () => {
  const [activities, setActivities] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getActivities = async () => {
      try {
        setIsLoading(true);
        const data = await fetchRecentActivities();
        setActivities(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching recent activities:', err);
        setError('Failed to load activity data');
      } finally {
        setIsLoading(false);
      }
    };

    getActivities();
    
    // Poll for updates every minute
    const interval = setInterval(getActivities, 60000);
    return () => clearInterval(interval);
  }, []);

  const getActivityIcon = (type) => {
    const typeLower = type.toLowerCase();
    
    if (typeLower.includes('policy')) {
      return 'sitemap';
    } else if (typeLower.includes('risk') || typeLower.includes('assessment')) {
      return 'exclamation-triangle';
    } else if (typeLower.includes('compliance') || typeLower.includes('monitor')) {
      return 'check-square';
    } else if (typeLower.includes('report')) {
      return 'chart-bar';
    } else {
      return 'bell';
    }
  };
  
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 60) {
      return diffMins === 0 ? 'Just now' : `${diffMins}m ago`;
    } else if (diffHours < 24) {
      return `${diffHours}h ago`;
    } else if (diffDays < 7) {
      return `${diffDays}d ago`;
    } else {
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric',
        year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
      });
    }
  };

  if (isLoading) {
    return <LoadingSpinner size="30px" />;
  }

  if (error) {
    return (
      <div className="alert alert-danger">
        <i className="fas fa-exclamation-circle me-2"></i>
        {error}
      </div>
    );
  }

  if (activities.length === 0) {
    return (
      <div className="alert alert-info">
        <i className="fas fa-info-circle me-2"></i>
        No recent activities found
      </div>
    );
  }

  return (
    <div className="activities-list">
      {activities.map((activity, index) => (
        <div key={activity.id || index} className="activity-item d-flex align-items-start mb-3 pb-3 border-bottom">
          <div className="activity-icon me-3">
            <div className="rounded-circle bg-light d-flex align-items-center justify-content-center" style={{ width: '40px', height: '40px' }}>
              <i className={`fas fa-${getActivityIcon(activity.activity_type)}`}></i>
            </div>
          </div>
          <div className="activity-content flex-grow-1">
            <div className="d-flex justify-content-between align-items-start">
              <div>
                <strong>{activity.activity_type}</strong>
                <p className="mb-0 text-muted">{activity.description}</p>
              </div>
              <div className="activity-time text-muted small">
                {formatDate(activity.created_at)}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default RecentActivities;