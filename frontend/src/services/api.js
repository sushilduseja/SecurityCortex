import axios from 'axios';

const API_BASE_URL = '/api';

// Configure axios defaults
axios.defaults.baseURL = API_BASE_URL;
axios.defaults.headers.common['Content-Type'] = 'application/json';

// Dashboard endpoints
export const fetchDashboardMetrics = async () => {
  try {
    const response = await axios.get('/dashboard/metrics');
    return response.data.data; // Extract the data field from the response
  } catch (error) {
    console.error('Error fetching dashboard metrics:', error);
    return {
      policy_count: 0,
      avg_risk_score: 0,
      compliance_rate: 0,
      active_monitors: 0,
      deltas: {
        policy_count: 0,
        avg_risk_score: 0,
        compliance_rate: 0,
        active_monitors: 0
      }
    };
  }
};

export const fetchComplianceStatusChart = async () => {
  try {
    const response = await axios.get('/charts/compliance-status');
    return response.data.data; // Extract the data field from the response
  } catch (error) {
    console.error('Error fetching compliance status chart:', error);
    return { labels: [], values: [] };
  }
};

export const fetchRiskDistributionChart = async () => {
  try {
    const response = await axios.get('/charts/risk-distribution');
    return response.data.data; // Extract the data field from the response
  } catch (error) {
    console.error('Error fetching risk distribution chart:', error);
    return { labels: [], values: [] };
  }
};

export const fetchRecentActivities = async () => {
  try {
    const response = await axios.get('/activities/recent');
    return response.data.data; // Extract the data field from the response
  } catch (error) {
    console.error('Error fetching recent activities:', error);
    return [];
  }
};

// Governance endpoints
export const fetchPolicies = async () => {
  const response = await axios.get('/policies');
  return response.data;
};

export const fetchPolicy = async (id) => {
  const response = await axios.get(`/policies/${id}`);
  return response.data;
};

export const createPolicy = async (policyData) => {
  const response = await axios.post('/policies', policyData);
  return response.data;
};

export const updatePolicy = async (id, policyData) => {
  const response = await axios.put(`/policies/${id}`, policyData);
  return response.data;
};

// Risk Assessment endpoints
export const fetchRiskAssessments = async () => {
  const response = await axios.get('/risk-assessments');
  return response.data;
};

export const fetchRiskAssessment = async (id) => {
  const response = await axios.get(`/risk-assessments/${id}`);
  return response.data;
};

export const createRiskAssessment = async (assessmentData) => {
  const response = await axios.post('/risk-assessments', assessmentData);
  return response.data;
};

// Compliance Monitoring endpoints
export const fetchComplianceMonitors = async () => {
  const response = await axios.get('/compliance-monitors');
  return response.data;
};

export const fetchComplianceMonitor = async (id) => {
  const response = await axios.get(`/compliance-monitors/${id}`);
  return response.data;
};

export const createComplianceMonitor = async (monitorData) => {
  const response = await axios.post('/compliance-monitors', monitorData);
  return response.data;
};

export const updateComplianceMonitor = async (id, monitorData) => {
  const response = await axios.put(`/compliance-monitors/${id}`, monitorData);
  return response.data;
};

// Reporting endpoints
export const fetchReports = async () => {
  const response = await axios.get('/reports');
  return response.data;
};

export const fetchReport = async (id) => {
  const response = await axios.get(`/reports/${id}`);
  return response.data;
};

export const createReport = async (reportData) => {
  const response = await axios.post('/reports', reportData);
  return response.data;
};

// Notification endpoints
export const sendSmsNotification = async (data) => {
  try {
    const response = await axios.post('/notifications/sms', data);
    return response.data;
  } catch (error) {
    console.error('Error sending SMS notification:', error);
    return handleApiError(error);
  }
};

// Error handler for API calls
export const handleApiError = (error) => {
  const errorMsg = 
    error.response?.data?.message || 
    error.message || 
    'An unexpected error occurred';
  
  // Log error details for debugging
  console.error('API Error:', error);
  
  return {
    error: true,
    message: errorMsg,
    status: error.response?.status || 500
  };
};