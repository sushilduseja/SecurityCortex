/**
 * AI Governance Dashboard
 * Charts and Visualizations JavaScript
 */

// Store chart instances for updating later
let complianceChart = null;
let riskDistributionChart = null;
let policyDistributionChart = null;
let complianceTrendChart = null;
let riskHeatmapChart = null;
let governanceRadarChart = null;

// Initialize charts when the document is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize main dashboard charts
    initializeCharts();
});

/**
 * Initialize all charts
 */
function initializeCharts() {
    // Initialize charts for the dashboard
    initComplianceStatusChart();
    initRiskDistributionChart();
    
    // Other charts will be initialized when their sections are loaded
    console.log('Charts initialized');
}

/**
 * Update charts with new data
 */
function updateCharts() {
    // Update all initialized charts with new data
    updateComplianceStatusChart();
    updateRiskDistributionChart();
}

/**
 * Initialize Compliance Status Chart
 */
function initComplianceStatusChart() {
    const ctx = document.getElementById('complianceStatusChart');
    
    if (ctx) {
        complianceChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Compliant', 'Partially Compliant', 'Non-Compliant', 'Under Review'],
                datasets: [{
                    data: [70, 15, 8, 7],
                    backgroundColor: [
                        '#1cc88a', // Green - Compliant
                        '#f6c23e', // Yellow - Partially Compliant
                        '#e74a3b', // Red - Non-Compliant
                        '#4e73df'  // Blue - Under Review
                    ],
                    hoverBackgroundColor: [
                        '#17a673',
                        '#dda20a',
                        '#be2617',
                        '#2e59d9'
                    ],
                    hoverBorderColor: "rgba(234, 236, 244, 1)",
                }]
            },
            options: {
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.parsed}%`;
                            }
                        }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeOutCubic'
                }
            }
        });
    }
}

/**
 * Update Compliance Status Chart with new data
 */
function updateComplianceStatusChart(data) {
    // If real data is provided, use it
    // Otherwise use sample data for demonstration
    const chartData = data || {
        compliant: 70,
        partiallyCompliant: 15,
        nonCompliant: 8,
        underReview: 7
    };
    
    if (complianceChart) {
        complianceChart.data.datasets[0].data = [
            chartData.compliant,
            chartData.partiallyCompliant,
            chartData.nonCompliant,
            chartData.underReview
        ];
        
        complianceChart.update();
    }
}

/**
 * Initialize Risk Distribution Chart
 */
function initRiskDistributionChart() {
    const ctx = document.getElementById('riskDistributionChart');
    
    if (ctx) {
        riskDistributionChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['High', 'Medium-High', 'Medium', 'Medium-Low', 'Low'],
                datasets: [{
                    label: 'Risk Distribution',
                    data: [5, 12, 20, 15, 8],
                    backgroundColor: [
                        '#e74a3b', // Red - High
                        '#f6c23e', // Yellow - Medium-High
                        '#4e73df', // Blue - Medium
                        '#36b9cc', // Cyan - Medium-Low
                        '#1cc88a'  // Green - Low
                    ],
                    maxBarThickness: 50,
                }]
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            drawBorder: false,
                            color: "rgba(0, 0, 0, 0.05)",
                        },
                        ticks: {
                            font: {
                                size: 12
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false,
                            drawBorder: false
                        },
                        ticks: {
                            font: {
                                size: 12
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Models: ${context.parsed.y}`;
                            }
                        }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeOutQuart'
                }
            }
        });
    }
}

/**
 * Update Risk Distribution Chart with new data
 */
function updateRiskDistributionChart(data) {
    // If real data is provided, use it
    // Otherwise use sample data for demonstration
    const chartData = data || {
        high: 5,
        mediumHigh: 12,
        medium: 20,
        mediumLow: 15,
        low: 8
    };
    
    if (riskDistributionChart) {
        riskDistributionChart.data.datasets[0].data = [
            chartData.high,
            chartData.mediumHigh,
            chartData.medium,
            chartData.mediumLow,
            chartData.low
        ];
        
        riskDistributionChart.update();
    }
}

/**
 * Initialize Policy Category Distribution Chart
 */
function initPolicyCategoryChart() {
    const ctx = document.getElementById('policyCategoryChart');
    
    if (ctx) {
        policyDistributionChart = new Chart(ctx, {
            type: 'polarArea',
            data: {
                labels: ['Privacy', 'Security', 'Fairness', 'Transparency', 'Accountability'],
                datasets: [{
                    data: [4, 3, 2, 2, 1],
                    backgroundColor: [
                        '#4e73df', // Blue - Privacy
                        '#1cc88a', // Green - Security
                        '#36b9cc', // Cyan - Fairness
                        '#f6c23e', // Yellow - Transparency
                        '#e74a3b'  // Red - Accountability
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    }
                },
                scales: {
                    r: {
                        ticks: {
                            display: false
                        }
                    }
                },
                animation: {
                    duration: 1200,
                    easing: 'easeOutQuint'
                }
            }
        });
    }
}

/**
 * Initialize Compliance Trend Line Chart
 */
function initComplianceTrendChart() {
    const ctx = document.getElementById('complianceTrendChart');
    
    if (ctx) {
        complianceTrendChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Compliance Rate',
                    data: [78, 80, 85, 82, 90, 94],
                    borderColor: '#1cc88a',
                    backgroundColor: 'rgba(28, 200, 138, 0.1)',
                    borderWidth: 3,
                    pointBackgroundColor: '#1cc88a',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: false,
                        min: 50,
                        max: 100,
                        grid: {
                            color: "rgba(0, 0, 0, 0.05)",
                        },
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Compliance: ${context.parsed.y}%`;
                            }
                        }
                    }
                },
                animation: {
                    duration: 1500,
                    easing: 'easeOutQuad'
                }
            }
        });
    }
}

/**
 * Initialize Governance Maturity Radar Chart
 */
function initGovernanceMaturityChart() {
    const ctx = document.getElementById('governanceMaturityChart');
    
    if (ctx) {
        governanceRadarChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: [
                    'Risk Management',
                    'Compliance',
                    'Transparency',
                    'Fairness',
                    'Accountability',
                    'Ethics'
                ],
                datasets: [
                    {
                        label: 'Current Maturity',
                        data: [75, 65, 80, 70, 60, 55],
                        backgroundColor: 'rgba(78, 115, 223, 0.2)',
                        borderColor: 'rgba(78, 115, 223, 1)',
                        pointBackgroundColor: '#4e73df',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: '#4e73df'
                    },
                    {
                        label: 'Industry Benchmark',
                        data: [65, 70, 60, 80, 65, 70],
                        backgroundColor: 'rgba(28, 200, 138, 0.2)',
                        borderColor: 'rgba(28, 200, 138, 1)',
                        pointBackgroundColor: '#1cc88a',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: '#1cc88a'
                    }
                ]
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        pointLabels: {
                            font: {
                                size: 12
                            }
                        },
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.parsed.r + '%';
                            }
                        }
                    }
                },
                animation: {
                    duration: 1200,
                    easing: 'easeOutCubic'
                }
            }
        });
    }
}

/**
 * Initialize specific charts for a section
 */
function initSectionCharts(sectionName) {
    switch(sectionName) {
        case 'governance':
            initPolicyCategoryChart();
            break;
        case 'monitoring':
            initComplianceTrendChart();
            break;
        case 'risk':
            // Risk-specific charts
            break;
        case 'reports':
            initGovernanceMaturityChart();
            break;
    }
}