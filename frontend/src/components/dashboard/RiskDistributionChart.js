import React, { useEffect, useState, useRef } from 'react';
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
import { gsap } from 'gsap';
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
  const chartRef = useRef(null);
  const chartContainerRef = useRef(null);

  useEffect(() => {
    const getChartData = async () => {
      try {
        setIsLoading(true);
        const data = await fetchRiskDistributionChart();
        
        // Enhanced color gradient based on risk level
        const colors = data.labels.map(label => {
          if (label.toLowerCase().includes('high')) {
            return 'rgba(231, 76, 60, 0.85)'; // Red for high risk
          } else if (label.toLowerCase().includes('medium')) {
            return 'rgba(241, 196, 15, 0.85)'; // Yellow for medium risk
          } else if (label.toLowerCase().includes('low')) {
            return 'rgba(46, 204, 113, 0.85)'; // Green for low risk
          } else {
            return 'rgba(52, 152, 219, 0.85)'; // Blue for other
          }
        });
        
        const borderColors = colors.map(color => color.replace('0.85', '1'));
        
        setChartData({
          labels: data.labels,
          datasets: [
            {
              label: 'Risk Count',
              data: data.values,
              backgroundColor: colors,
              borderColor: borderColors,
              borderWidth: 2,
              borderRadius: 6,
              borderSkipped: false,
              barPercentage: 0.7,
              categoryPercentage: 0.8,
              hoverBackgroundColor: borderColors,
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

  // Animation effect when chart becomes visible
  useEffect(() => {
    if (chartContainerRef.current && chartData) {
      // Animate the container
      gsap.fromTo(
        chartContainerRef.current,
        { opacity: 0, y: 20 },
        { 
          opacity: 1, 
          y: 0, 
          duration: 0.6, 
          ease: "power2.out"
        }
      );
      
      // Animate each bar individually (done through chart options)
    }
  }, [chartData]);

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
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.85)',
        padding: 12,
        bodyFont: {
          size: 14
        },
        callbacks: {
          label: function(context) {
            const label = context.dataset.label || '';
            const value = context.formattedValue;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = Math.round((context.raw / total) * 100);
            return `${label}: ${value} (${percentage}% of all risks)`;
          },
          title: function(context) {
            return `${context[0].label} Risk`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          display: true,
          drawBorder: false,
          color: 'rgba(200, 200, 200, 0.15)',
        },
        ticks: {
          precision: 0,
          font: {
            size: 12
          },
          callback: function(value) {
            return value + (value === 1 ? ' system' : ' systems');
          }
        },
        title: {
          display: true,
          text: 'Number of Systems',
          font: {
            size: 14,
            weight: 'bold'
          },
          padding: {top: 10, bottom: 10}
        }
      },
      x: {
        grid: {
          display: false,
          drawBorder: false,
        },
        ticks: {
          font: {
            size: 12,
            weight: 'bold'
          }
        }
      },
    },
    animation: {
      delay: (context) => {
        // Stagger the bar animations for better visual effect
        return context.dataIndex * 100;
      },
      duration: 1000,
      easing: 'easeOutQuart',
      from: (ctx) => {
        if (ctx.type === 'data' && ctx.mode === 'default') {
          return { y: ctx.chart.scales.y.getPixelForValue(0) };
        }
      }
    },
    // Add an annotation line for average risk threshold
    annotation: {
      annotations: {
        thresholdLine: {
          type: 'line',
          yMin: 3,
          yMax: 3,
          borderColor: 'rgba(255, 99, 132, 0.7)',
          borderWidth: 2,
          borderDash: [6, 6],
          label: {
            enabled: true,
            content: 'Risk Threshold',
            position: 'end',
            backgroundColor: 'rgba(255, 99, 132, 0.8)',
            font: {
              size: 12
            }
          }
        }
      }
    }
  };

  return (
    <div ref={chartContainerRef} className="chart-container" style={{ height: '300px', position: 'relative' }}>
      <div className="chart-title mb-2" style={{ textAlign: 'center', fontWeight: 'bold', color: '#2c3e50' }}>
        Risk Distribution by Severity Level
      </div>
      {chartData && (
        <Bar 
          ref={chartRef}
          data={chartData} 
          options={options} 
        />
      )}
    </div>
  );
};

export default RiskDistributionChart;