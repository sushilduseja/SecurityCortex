
/**
 * AI Governance Dashboard
 * Chart Utilities for Advanced Visualizations
 */

// Library of advanced chart utility functions
const ChartUtils = {
  /**
   * Creates a color scale based on a range of values
   * @param {number} min - Minimum value in dataset
   * @param {number} max - Maximum value in dataset
   * @param {string[]} colors - Array of color strings (hex or rgba)
   * @returns {Function} - Function that takes a value and returns a color
   */
  createColorScale: function(min, max, colors = ['#2ecc71', '#f1c40f', '#e74c3c']) {
    return function(value) {
      const range = max - min;
      const normalizedValue = (value - min) / range;
      
      // For 2 colors
      if (colors.length === 2) {
        return d3.interpolate(colors[0], colors[1])(normalizedValue);
      }
      
      // For multiple colors
      const colorScale = d3.scaleLinear()
        .domain(colors.map((_, i) => min + (i * range / (colors.length - 1))))
        .range(colors);
      
      return colorScale(value);
    };
  },
  
  /**
   * Generates a radar chart configuration
   * @param {string} elementId - DOM element ID to render chart
   * @param {object[]} data - Array of data objects with category and value properties
   * @param {object} options - Customization options
   * @returns {object} - Chart configuration object
   */
  createRadarChartConfig: function(elementId, data, options = {}) {
    const defaultOptions = {
      maxValue: 100,
      width: 500,
      height: 500,
      levels: 5,
      roundStrokes: true,
      color: d3.scaleOrdinal().range(["#26AF67", "#762712"]),
      format: '.0f'
    };
    
    const config = { ...defaultOptions, ...options };
    
    // Process data for radar chart format
    const categories = [...new Set(data.map(d => d.category))];
    const series = [...new Set(data.map(d => d.series))];
    
    const formattedData = series.map(s => {
      const seriesData = data.filter(d => d.series === s);
      return {
        name: s,
        axes: categories.map(c => {
          const match = seriesData.find(d => d.category === c);
          return {
            axis: c,
            value: match ? match.value : 0
          };
        })
      };
    });
    
    return {
      element: elementId,
      data: formattedData,
      config: config
    };
  },
  
  /**
   * Creates a network graph configuration for compliance relationships
   * @param {object[]} nodes - Array of node objects
   * @param {object[]} links - Array of link objects connecting nodes
   * @param {object} options - Customization options
   * @returns {object} - Force directed graph configuration
   */
  createNetworkGraph: function(nodes, links, options = {}) {
    const defaultOptions = {
      width: 800,
      height: 600,
      nodeRadius: 10,
      linkDistance: 100,
      charge: -400,
      centerForce: 0.3
    };
    
    const config = { ...defaultOptions, ...options };
    
    // Process nodes to ensure they have required properties
    const processedNodes = nodes.map(node => ({
      id: node.id,
      name: node.name || node.id,
      group: node.group || 1,
      size: node.size || config.nodeRadius,
      color: node.color || null
    }));
    
    // Process links to ensure they have required properties
    const processedLinks = links.map(link => ({
      source: link.source,
      target: link.target,
      value: link.value || 1,
      label: link.label || '',
      color: link.color || '#999'
    }));
    
    return {
      nodes: processedNodes,
      links: processedLinks,
      config: config
    };
  },
  
  /**
   * Creates a sankey diagram configuration for risk flow visualization
   * @param {object[]} nodes - Array of node objects
   * @param {object[]} links - Array of link objects connecting nodes
   * @param {object} options - Customization options
   * @returns {object} - Sankey diagram configuration
   */
  createSankeyConfig: function(nodes, links, options = {}) {
    const defaultOptions = {
      width: 800,
      height: 500,
      nodeWidth: 20,
      nodePadding: 10,
      iterations: 32,
      colors: d3.scaleOrdinal(d3.schemeCategory10)
    };
    
    const config = { ...defaultOptions, ...options };
    
    // Process nodes to ensure they have required properties
    const processedNodes = nodes.map((node, i) => ({
      node: i,
      name: node.name,
      color: node.color || config.colors(i)
    }));
    
    // Process links to ensure they have required properties
    const processedLinks = links.map(link => ({
      source: link.source,
      target: link.target,
      value: link.value,
      color: link.color || null
    }));
    
    return {
      nodes: processedNodes,
      links: processedLinks,
      config: config
    };
  },
  
  /**
   * Creates a tree map configuration for hierarchical risk visualization
   * @param {object} root - Hierarchical data with children
   * @param {object} options - Customization options
   * @returns {object} - Tree map configuration
   */
  createTreeMapConfig: function(root, options = {}) {
    const defaultOptions = {
      width: 800,
      height: 500,
      padding: 1,
      colorScale: d3.scaleOrdinal(d3.schemeBlues[9])
    };
    
    const config = { ...defaultOptions, ...options };
    
    // Process the hierarchical data to ensure it's in the correct format
    const processRoot = (node, depth = 0) => {
      const processed = {
        name: node.name,
        value: node.value || (node.children ? 0 : 1),
        depth: depth,
        color: node.color || null,
        children: node.children ? node.children.map(child => processRoot(child, depth + 1)) : null
      };
      
      // Calculate sum for parent nodes
      if (processed.children) {
        processed.value = processed.children.reduce((sum, child) => sum + child.value, 0);
      }
      
      return processed;
    };
    
    return {
      data: processRoot(root),
      config: config
    };
  },
  
  /**
   * Creates a bubble chart configuration for risk categories
   * @param {object[]} data - Array of data objects with size and category properties
   * @param {object} options - Customization options
   * @returns {object} - Bubble chart configuration
   */
  createBubbleChartConfig: function(data, options = {}) {
    const defaultOptions = {
      width: 800,
      height: 500,
      padding: 1,
      minRadius: 5,
      maxRadius: 50,
      colorScale: d3.scaleOrdinal(d3.schemeSet3)
    };
    
    const config = { ...defaultOptions, ...options };
    
    // Process the data to ensure it's in the correct format
    const processedData = data.map((item, i) => ({
      id: item.id || i,
      name: item.name,
      value: item.value,
      category: item.category,
      color: item.color || config.colorScale(item.category)
    }));
    
    return {
      data: processedData,
      config: config
    };
  },
  
  /**
   * Creates a calendar heatmap configuration for temporal risk visualization
   * @param {object[]} data - Array of data objects with date and value properties
   * @param {object} options - Customization options
   * @returns {object} - Calendar heatmap configuration
   */
  createCalendarHeatmapConfig: function(data, options = {}) {
    const defaultOptions = {
      width: 800,
      height: 200,
      cellSize: 15,
      cellPadding: 2,
      monthLabels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      colorScale: d3.scaleLinear().range(['#ebedf0', '#c6e48b', '#7bc96f', '#239a3b', '#196127'])
    };
    
    const config = { ...defaultOptions, ...options };
    
    // Process the data to ensure it's in the correct format
    const processedData = data.map(item => ({
      date: new Date(item.date),
      value: item.value,
      tooltip: item.tooltip || null
    }));
    
    return {
      data: processedData,
      config: config
    };
  },
  
  /**
   * Creates a chord diagram configuration for inter-category relationships
   * @param {number[][]} matrix - Matrix of connections between categories
   * @param {string[]} names - Names of categories corresponding to matrix indices
   * @param {object} options - Customization options
   * @returns {object} - Chord diagram configuration
   */
  createChordDiagramConfig: function(matrix, names, options = {}) {
    const defaultOptions = {
      width: 600,
      height: 600,
      padding: 0.01,
      colorScale: d3.scaleOrdinal(d3.schemeCategory10)
    };
    
    const config = { ...defaultOptions, ...options };
    
    return {
      matrix: matrix,
      names: names,
      config: config
    };
  },
  
  /**
   * Creates a risk matrix (2D heatmap) configuration
   * @param {object[]} data - Array of data objects with impact and likelihood properties
   * @param {object} options - Customization options
   * @returns {object} - Risk matrix configuration
   */
  createRiskMatrixConfig: function(data, options = {}) {
    const defaultOptions = {
      width: 600,
      height: 600,
      xAxisLabel: 'Impact',
      yAxisLabel: 'Likelihood',
      levels: 5,
      colorScale: d3.scaleLinear()
        .domain([0, 0.25, 0.5, 0.75, 1])
        .range(['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c', '#c0392b'])
    };
    
    const config = { ...defaultOptions, ...options };
    
    // Process the data to ensure it's in the correct format
    const processedData = data.map((item, i) => ({
      id: item.id || i,
      name: item.name || `Risk ${i+1}`,
      impact: item.impact,
      likelihood: item.likelihood,
      severity: item.impact * item.likelihood,
      category: item.category || null,
      description: item.description || null
    }));
    
    return {
      data: processedData,
      config: config
    };
  },
  
  /**
   * Generates a radial progress chart configuration
   * @param {number} value - Current value (0-100)
   * @param {object} options - Customization options
   * @returns {object} - Radial progress chart configuration
   */
  createRadialProgressConfig: function(value, options = {}) {
    const defaultOptions = {
      width: 200,
      height: 200,
      innerRadius: 60,
      outerRadius: 80,
      backgroundColor: '#f0f0f0',
      foregroundColor: value >= 75 ? '#2ecc71' : value >= 50 ? '#f1c40f' : '#e74c3c',
      label: Math.round(value) + '%',
      animationDuration: 1000
    };
    
    const config = { ...defaultOptions, ...options };
    
    return {
      value: Math.min(100, Math.max(0, value)),
      config: config
    };
  }
};

// Export utilities for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ChartUtils;
}

/**
 * Chart Utilities for AI Governance Dashboard
 * Contains functions to create advanced, interactive charts
 */

// Initialize Chart.js with global defaults
if (typeof Chart !== 'undefined') {
  Chart.defaults.font.family = "'Inter', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif";
  Chart.defaults.color = '#6c757d';
  Chart.defaults.responsive = true;
  Chart.defaults.maintainAspectRatio = false;
}

/**
 * Creates an advanced compliance status sunburst chart
 * @param {HTMLCanvasElement} canvasElement - The canvas element
 * @param {Object} data - The chart data
 * @returns {Chart} - The created chart
 */
function createComplianceSunburstChart(canvasElement, data) {
  const ctx = canvasElement.getContext('2d');
  
  // Define color scheme
  const colorMap = {
    'Critical': '#dc3545',
    'Warning': '#fd7e14',
    'Normal': '#0dcaf0',
    'Good': '#20c997'
  };
  
  // Process data for sunburst format
  const labels = Object.keys(data);
  const values = Object.values(data);
  const total = values.reduce((a, b) => a + b, 0);
  
  // Create parent and children data
  const rootData = {
    name: 'Compliance',
    value: total,
    children: labels.map((label, i) => ({
      name: label,
      value: values[i],
      color: colorMap[label] || '#6c757d'
    }))
  };
  
  // Process hierarchical data for sunburst
  function processData(data) {
    const result = {
      labels: ['Compliance'],
      datasets: [{
        data: [data.value],
        backgroundColor: ['#4361ee'],
        hoverBackgroundColor: ['#3a56d4']
      }]
    };
    
    if (data.children && data.children.length) {
      data.children.forEach(child => {
        result.labels.push(child.name);
        result.datasets[0].data.push(child.value);
        result.datasets[0].backgroundColor.push(child.color);
        result.datasets[0].hoverBackgroundColor.push(child.color);
      });
    }
    
    return result;
  }
  
  const chartData = processData(rootData);
  
  // Create the sunburst chart (represented as doughnut with custom options)
  return new Chart(ctx, {
    type: 'doughnut',
    data: chartData,
    options: {
      cutout: '40%',
      plugins: {
        legend: {
          position: 'right',
          labels: {
            generateLabels: function(chart) {
              const data = chart.data;
              if (data.labels.length && data.datasets.length) {
                return data.labels.map((label, i) => {
                  const meta = chart.getDatasetMeta(0);
                  const style = meta.controller.getStyle(i);
                  const value = chart.data.datasets[0].data[i];
                  const percentage = ((value / total) * 100).toFixed(1);
                  
                  return {
                    text: `${label} (${percentage}%)`,
                    fillStyle: data.datasets[0].backgroundColor[i],
                    strokeStyle: '#fff',
                    lineWidth: 2,
                    hidden: isNaN(data.datasets[0].data[i]) || meta.data[i].hidden,
                    index: i
                  };
                });
              }
              return [];
            }
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const label = context.label || '';
              const value = context.raw || 0;
              const percentage = ((value / total) * 100).toFixed(1);
              return `${label}: ${value} (${percentage}%)`;
            }
          }
        }
      },
      animation: {
        animateRotate: true,
        animateScale: true
      }
    }
  });
}

/**
 * Creates an advanced risk distribution chart
 * @param {HTMLCanvasElement} canvasElement - The canvas element
 * @param {Array} riskScores - Array of risk scores
 * @param {Array} labels - Optional array of labels
 * @returns {Chart} - The created chart
 */
function createAdvancedRiskDistributionChart(canvasElement, riskScores, labels = null) {
  const ctx = canvasElement.getContext('2d');
  
  // Calculate frequency distribution
  const bins = [0, 20, 40, 60, 80, 100];
  const binLabels = ['0-20', '21-40', '41-60', '61-80', '81-100'];
  const binCounts = Array(bins.length - 1).fill(0);
  
  riskScores.forEach(score => {
    for (let i = 0; i < bins.length - 1; i++) {
      if (score >= bins[i] && score <= bins[i + 1]) {
        binCounts[i]++;
        break;
      }
    }
  });
  
  // Calculate average risk
  const avgRisk = riskScores.reduce((a, b) => a + b, 0) / riskScores.length;
  
  // Determine risk level
  let riskLevel = 'Low';
  let riskGradient = ctx.createLinearGradient(0, 0, 0, 400);
  
  if (avgRisk >= 80) {
    riskLevel = 'Critical';
    riskGradient.addColorStop(0, 'rgba(220, 53, 69, 0.8)');
    riskGradient.addColorStop(1, 'rgba(220, 53, 69, 0.2)');
  } else if (avgRisk >= 60) {
    riskLevel = 'High';
    riskGradient.addColorStop(0, 'rgba(253, 126, 20, 0.8)');
    riskGradient.addColorStop(1, 'rgba(253, 126, 20, 0.2)');
  } else if (avgRisk >= 40) {
    riskLevel = 'Medium';
    riskGradient.addColorStop(0, 'rgba(255, 193, 7, 0.8)');
    riskGradient.addColorStop(1, 'rgba(255, 193, 7, 0.2)');
  } else if (avgRisk >= 20) {
    riskLevel = 'Low';
    riskGradient.addColorStop(0, 'rgba(32, 201, 151, 0.8)');
    riskGradient.addColorStop(1, 'rgba(32, 201, 151, 0.2)');
  } else {
    riskLevel = 'Minimal';
    riskGradient.addColorStop(0, 'rgba(13, 202, 240, 0.8)');
    riskGradient.addColorStop(1, 'rgba(13, 202, 240, 0.2)');
  }
  
  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: binLabels,
      datasets: [{
        label: 'Risk Distribution',
        data: binCounts,
        backgroundColor: riskGradient,
        borderColor: 'rgba(0, 0, 0, 0.1)',
        borderWidth: 1,
        borderRadius: 5,
        barPercentage: 0.8,
        categoryPercentage: 0.8
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Number of Models/Components'
          },
          ticks: {
            precision: 0
          }
        },
        x: {
          title: {
            display: true,
            text: 'Risk Score Range'
          }
        }
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            title: function(tooltipItems) {
              return `Risk Level: ${tooltipItems[0].label}`;
            },
            label: function(context) {
              return `Count: ${context.raw}`;
            },
            footer: function() {
              return `Average Risk: ${avgRisk.toFixed(1)} (${riskLevel})`;
            }
          }
        },
        annotation: {
          annotations: {
            line1: {
              type: 'line',
              yMin: 0,
              yMax: Math.max(...binCounts) + 1,
              xMin: avgRisk / 20 - 0.5,
              xMax: avgRisk / 20 - 0.5,
              borderColor: 'rgba(220, 53, 69, 0.8)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                display: true,
                content: `Avg: ${avgRisk.toFixed(1)}`,
                position: 'top'
              }
            }
          }
        }
      }
    }
  });
}

/**
 * Creates an interactive compliance trend chart
 * @param {HTMLCanvasElement} canvasElement - The canvas element
 * @param {Array} dates - Array of date strings
 * @param {Array} values - Array of compliance values
 * @returns {Chart} - The created chart
 */
function createComplianceTrendChart(canvasElement, dates, values) {
  const ctx = canvasElement.getContext('2d');
  
  // Create gradient
  const gradient = ctx.createLinearGradient(0, 0, 0, 400);
  gradient.addColorStop(0, 'rgba(67, 97, 238, 0.6)');
  gradient.addColorStop(1, 'rgba(67, 97, 238, 0.1)');
  
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: dates,
      datasets: [{
        label: 'Compliance Rate',
        data: values,
        backgroundColor: gradient,
        borderColor: 'rgba(67, 97, 238, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(67, 97, 238, 1)',
        pointBorderColor: '#fff',
        pointRadius: 4,
        pointHoverRadius: 6,
        fill: true,
        tension: 0.3
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: false,
          min: Math.max(0, Math.min(...values) - 10),
          max: Math.min(100, Math.max(...values) + 10),
          title: {
            display: true,
            text: 'Compliance Rate (%)'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Date'
          }
        }
      },
      plugins: {
        tooltip: {
          mode: 'index',
          intersect: false,
          callbacks: {
            label: function(context) {
              return `Compliance: ${context.raw}%`;
            }
          }
        },
        annotation: {
          annotations: {
            target: {
              type: 'line',
              yMin: 80,
              yMax: 80,
              borderColor: 'rgba(32, 201, 151, 0.8)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                display: true,
                content: 'Target (80%)',
                position: 'end'
              }
            }
          }
        }
      },
      interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false
      }
    }
  });
}

// Export functions for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    createComplianceSunburstChart,
    createAdvancedRiskDistributionChart,
    createComplianceTrendChart
  };
}
