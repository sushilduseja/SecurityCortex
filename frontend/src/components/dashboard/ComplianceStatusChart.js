import React, { useEffect, useState } from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { fetchComplianceStatusChart } from '../../services/api';
import LoadingSpinner from '../common/LoadingSpinner';

ChartJS.register(ArcElement, Tooltip, Legend);

const ComplianceStatusChart = () => {
  const [chartData, setChartData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getChartData = async () => {
      try {
        setIsLoading(true);
        const data = await fetchComplianceStatusChart();
        
        setChartData({
          labels: data.labels,
          datasets: [
            {
              data: data.values,
              backgroundColor: [
                'rgba(46, 204, 113, 0.8)',
                'rgba(241, 196, 15, 0.8)',
                'rgba(231, 76, 60, 0.8)',
                'rgba(52, 152, 219, 0.8)',
              ],
              borderColor: [
                'rgba(46, 204, 113, 1)',
                'rgba(241, 196, 15, 1)',
                'rgba(231, 76, 60, 1)',
                'rgba(52, 152, 219, 1)',
              ],
              borderWidth: 1,
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
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 20,
          usePointStyle: true,
          pointStyle: 'circle',
        },
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.formattedValue;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = Math.round((context.raw / total) * 100);
            return `${label}: ${value} (${percentage}%)`;
          }
        }
      }
    },
  };

  return (
    <div className="chart-container" style={{ height: '300px' }}>
      {chartData && <Pie data={chartData} options={options} />}
    </div>
  );
};

export default ComplianceStatusChart;