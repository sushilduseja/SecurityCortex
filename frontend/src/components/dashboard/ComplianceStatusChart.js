import React, { useEffect, useState, useRef } from 'react';
import { Doughnut } from 'react-chartjs-2';
import { 
  Chart as ChartJS, 
  ArcElement, 
  Tooltip, 
  Legend,
  LinearScale,
  Title,
  SubTitle
} from 'chart.js';
import { fetchComplianceStatusChart, fetchComplianceMonitors } from '../../services/api';
import LoadingSpinner from '../common/LoadingSpinner';

// Register required components
ChartJS.register(
  ArcElement, 
  Tooltip, 
  Legend, 
  LinearScale,
  Title,
  SubTitle
);

// Create the center text plugin
const centerTextPlugin = {
  id: 'centerText',
  beforeDraw: function(chart) {
    if (chart.config.type === 'doughnut') {
      // Get ctx and data
      const ctx = chart.ctx;
      const data = chart.data.datasets[0].data;
      const total = data.reduce((a, b) => a + b, 0);
      
      // Calculate compliance rate
      const compliantIndex = chart.data.labels.findIndex(label => 
        label.toLowerCase().includes('compliant') && !label.toLowerCase().includes('non') && !label.toLowerCase().includes('partially')
      );
      
      const complianceRate = compliantIndex >= 0 
        ? Math.round((data[compliantIndex] / total) * 100) 
        : 0;
        
      // Draw center text
      const centerX = chart.getDatasetMeta(0).data[0] ? chart.getDatasetMeta(0).data[0].x : chart.width / 2;
      const centerY = chart.getDatasetMeta(0).data[0] ? chart.getDatasetMeta(0).data[0].y : chart.height / 2;
      
      ctx.save();
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      
      // Draw main percentage
      ctx.font = 'bold 28px Arial';
      ctx.fillStyle = '#2c3e50';
      ctx.fillText(`${complianceRate}%`, centerX, centerY - 15);
      
      // Draw label
      ctx.font = 'bold 14px Arial';
      ctx.fillStyle = '#7f8c8d';
      ctx.fillText('Compliance', centerX, centerY + 10);
      
      // Draw subtitle
      ctx.font = '12px Arial';
      ctx.fillStyle = '#95a5a6';
      ctx.fillText('Rate', centerX, centerY + 30);
      
      ctx.restore();
    }
  }
};

// Register the plugin globally
ChartJS.register(centerTextPlugin);

const ComplianceStatusChart = () => {
  const [chartData, setChartData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedModel, setSelectedModel] = useState('All');
  const [models, setModels] = useState([]);
  const [detailView, setDetailView] = useState(false);
  const [detailData, setDetailData] = useState(null);
  const chartRef = useRef(null);
  const chartContainerRef = useRef(null);

  // Fetch compliance monitors to get model list
  useEffect(() => {
    const getModelsList = async () => {
      try {
        const monitorsData = await fetchComplianceMonitors();
        
        // Extract unique model/system names
        const uniqueModels = ['All', ...new Set(monitorsData.map(m => m.model_or_system))];
        setModels(uniqueModels);
      } catch (err) {
        console.error('Error fetching compliance monitors:', err);
      }
    };
    
    getModelsList();
  }, []);

  // Fetch chart data
  useEffect(() => {
    const getChartData = async () => {
      try {
        setIsLoading(true);
        const response = await fetchComplianceStatusChart();
        const data = response.data || response;
        
        // Get compliance monitors for detail view
        const monitorsData = await fetchComplianceMonitors();
        
        // Filter monitors based on selected model if not 'All'
        const filteredMonitors = selectedModel === 'All' 
          ? monitorsData 
          : monitorsData.filter(m => m.model_or_system === selectedModel);
        
        // Prepare detail data
        const complianceDetails = prepareDetailData(filteredMonitors);
        setDetailData(complianceDetails);
        
        // Count statuses for the selected model
        const statusCounts = countStatusesByModel(monitorsData, selectedModel);
        
        setChartData({
          labels: Object.keys(statusCounts),
          datasets: [
            {
              data: Object.values(statusCounts),
              backgroundColor: [
                'rgba(46, 204, 113, 0.85)',  // Green - Compliant
                'rgba(241, 196, 15, 0.85)',  // Yellow - Partially Compliant
                'rgba(231, 76, 60, 0.85)',   // Red - Non-compliant
                'rgba(52, 152, 219, 0.85)',  // Blue - Under Review
              ],
              borderColor: [
                'rgba(46, 204, 113, 1)',
                'rgba(241, 196, 15, 1)',
                'rgba(231, 76, 60, 1)',
                'rgba(52, 152, 219, 1)',
              ],
              borderWidth: 2,
              hoverBorderWidth: 4,
              hoverOffset: 10,
            },
          ],
        });
        setError(null);
      } catch (err) {
        console.error('Error fetching compliance status chart data:', err);
        setError('Failed to load compliance status data');
      } finally {
        setIsLoading(false);
      }
    };

    getChartData();
  }, [selectedModel]);

  // Helper function to count statuses by model
  const countStatusesByModel = (monitors, modelFilter) => {
    // Filter monitors by selected model if not 'All'
    const filteredMonitors = modelFilter === 'All' 
      ? monitors 
      : monitors.filter(m => m.model_or_system === modelFilter);
    
    // Count by alert level
    const counts = {
      'Compliant': 0,
      'Partially Compliant': 0,
      'Non-Compliant': 0,
      'Under Review': 0
    };
    
    filteredMonitors.forEach(monitor => {
      const alertLevel = monitor.alert_level;
      if (alertLevel === 'Normal') {
        counts['Compliant']++;
      } else if (alertLevel === 'Warning') {
        counts['Partially Compliant']++;
      } else if (alertLevel === 'Critical') {
        counts['Non-Compliant']++;
      } else {
        counts['Under Review']++;
      }
    });
    
    return counts;
  };
  
  // Helper function to prepare detailed compliance data
  const prepareDetailData = (monitors) => {
    return monitors.map(monitor => ({
      name: monitor.name,
      description: monitor.description,
      status: getStatusFromAlertLevel(monitor.alert_level),
      currentValue: monitor.current_value,
      thresholdValue: monitor.threshold_value,
      lastChecked: new Date(monitor.last_checked).toLocaleString(),
      color: getColorFromAlertLevel(monitor.alert_level)
    }));
  };
  
  // Helper function to map alert level to status
  const getStatusFromAlertLevel = (alertLevel) => {
    switch (alertLevel) {
      case 'Normal': return 'Compliant';
      case 'Warning': return 'Partially Compliant';
      case 'Critical': return 'Non-Compliant';
      default: return 'Under Review';
    }
  };
  
  // Helper function to get color from alert level
  const getColorFromAlertLevel = (alertLevel) => {
    switch (alertLevel) {
      case 'Normal': return 'rgba(46, 204, 113, 1)'; 
      case 'Warning': return 'rgba(241, 196, 15, 1)';
      case 'Critical': return 'rgba(231, 76, 60, 1)';
      default: return 'rgba(52, 152, 219, 1)';
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

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '65%',
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 20,
          usePointStyle: true,
          pointStyle: 'circle',
          font: {
            size: 12,
            weight: 'bold'
          }
        },
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.85)',
        padding: 12,
        bodyFont: {
          size: 14
        },
        titleFont: {
          size: 16
        },
        usePointStyle: true,
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.formattedValue;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = Math.round((context.raw / total) * 100);
            return `${label}: ${value} monitors (${percentage}%)`;
          }
        }
      },
      // Enable centerText plugin
      centerText: {}
    },
    animation: {
      animateRotate: true,
      animateScale: true,
      duration: 800,
      easing: 'easeOutCubic'
    },
    onClick: (event, elements) => {
      if (elements.length > 0) {
        setDetailView(true);
      }
    }
  };

  return (
    <div className="compliance-chart-container">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div className="chart-controls">
          <div className="form-group d-inline-block me-3">
            <label htmlFor="modelSelect" className="me-2 fw-bold">Filter by:</label>
            <select 
              id="modelSelect" 
              className="form-select form-select-sm d-inline-block" 
              style={{ width: 'auto', minWidth: '150px' }}
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
            >
              {models.map(model => (
                <option key={model} value={model}>{model}</option>
              ))}
            </select>
          </div>
        </div>
        <div>
          <button 
            className="btn btn-sm btn-outline-primary" 
            onClick={() => setDetailView(!detailView)}
          >
            <i className={`fas fa-${detailView ? 'chart-pie' : 'list'} me-1`}></i>
            {detailView ? 'Show Chart' : 'Show Details'}
          </button>
        </div>
      </div>
      
      {!detailView ? (
        <div className="chart-container position-relative" style={{ height: '280px', width: '100%' }}>
          {chartData && (
            <Doughnut 
              ref={chartRef}
              data={chartData} 
              options={options} 
            />
          )}
        </div>
      ) : (
        <div className="detail-view-container" style={{ maxHeight: '280px', overflowY: 'auto' }}>
          <table className="table table-hover table-sm">
            <thead className="table-light sticky-top">
              <tr>
                <th>Monitor</th>
                <th>Status</th>
                <th>Current</th>
                <th>Threshold</th>
                <th>Last Checked</th>
              </tr>
            </thead>
            <tbody>
              {detailData && detailData.map((item, idx) => (
                <tr key={idx}>
                  <td>
                    <span className="fw-bold">{item.name}</span>
                    <br/>
                    <small className="text-muted">{item.description}</small>
                  </td>
                  <td>
                    <span className="badge" style={{ 
                      backgroundColor: item.color,
                      padding: '5px 8px'
                    }}>
                      {item.status}
                    </span>
                  </td>
                  <td className="text-center">{(item.currentValue * 100).toFixed(1)}%</td>
                  <td className="text-center">{(item.thresholdValue * 100).toFixed(1)}%</td>
                  <td><small>{item.lastChecked}</small></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      
      <div className="compliance-insights mt-3 pt-2 border-top">
        <small className="text-muted">
          <i className="fas fa-lightbulb me-1"></i>
          <strong>Insight:</strong> {selectedModel === 'All' 
            ? 'Overall compliance rate is affected by 2 critical and 1 warning alerts across systems.'
            : `${selectedModel} has ${detailData ? detailData.filter(d => d.status === 'Non-Compliant').length : 0} critical compliance issues requiring attention.`}
        </small>
      </div>
    </div>
  );
};

export default ComplianceStatusChart;