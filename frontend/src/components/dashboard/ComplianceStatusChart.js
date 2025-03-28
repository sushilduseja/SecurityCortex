import React, { useEffect, useState, useRef } from 'react';
import { Doughnut } from 'react-chartjs-2';
import { 
  Chart as ChartJS, 
  ArcElement, 
  Tooltip, 
  Legend,
  LinearScale,
  Title
} from 'chart.js';
import { fetchComplianceStatusChart } from '../../services/api';
import LoadingSpinner from '../common/LoadingSpinner';

// Register required components
ChartJS.register(
  ArcElement, 
  Tooltip, 
  Legend, 
  LinearScale,
  Title
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
      ctx.font = 'bold 24px Arial';
      ctx.fillStyle = '#2c3e50';
      ctx.fillText(`${complianceRate}%`, centerX, centerY - 10);
      
      // Draw label
      ctx.font = '14px Arial';
      ctx.fillStyle = '#7f8c8d';
      ctx.fillText('Compliance', centerX, centerY + 15);
      
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
  const chartRef = useRef(null);
  const chartContainerRef = useRef(null);

  useEffect(() => {
    const getChartData = async () => {
      try {
        setIsLoading(true);
        const response = await fetchComplianceStatusChart();
        
        const data = response.data || response;
        
        setChartData({
          labels: data.labels,
          datasets: [
            {
              data: data.values,
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
  }, []);

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
    cutout: '60%',
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
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.formattedValue;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = Math.round((context.raw / total) * 100);
            return `${label}: ${value} (${percentage}%)`;
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
    }
  };

  return (
    <div className="chart-container" style={{ height: '300px', position: 'relative' }}>
      {chartData && (
        <Doughnut 
          ref={chartRef}
          data={chartData} 
          options={options} 
        />
      )}
    </div>
  );
};

export default ComplianceStatusChart;