import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { fetchRiskDistributionChart } from '../../services/api';
import LoadingSpinner from '../common/LoadingSpinner';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const RiskDistributionChart = () => {
  const [chartData, setChartData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getChartData = async () => {
      try {
        setIsLoading(true);
        const data = await fetchRiskDistributionChart();
        
        setChartData({
          labels: data.labels,
          datasets: [
            {
              label: 'Risk Count',
              data: data.values,
              backgroundColor: [
                'rgba(231, 76, 60, 0.8)',
                'rgba(241, 196, 15, 0.8)',
                'rgba(46, 204, 113, 0.8)',
              ],
              borderColor: [
                'rgba(231, 76, 60, 1)',
                'rgba(241, 196, 15, 1)',
                'rgba(46, 204, 113, 1)',
              ],
              borderWidth: 1,
            },
          ],
        });
        setError(null);
      } catch (err) {
        console.error('Error fetching risk distribution chart data:', err);
        setError('Failed to load risk distribution data');
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
        position: 'top',
        display: false,
      },
      title: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          display: true,
          drawBorder: false,
        },
        ticks: {
          precision: 0,
        },
      },
      x: {
        grid: {
          display: false,
          drawBorder: false,
        },
      },
    },
  };

  return (
    <div className="chart-container" style={{ height: '300px' }}>
      {chartData && <Bar data={chartData} options={options} />}
    </div>
  );
};

export default RiskDistributionChart;