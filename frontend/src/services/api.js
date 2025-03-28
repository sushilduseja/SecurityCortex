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
  try {
    const response = await axios.get('/policies');
    if (response.data && response.data.success) {
      // Ensure we always return an array even if the API returns null or undefined
      return Array.isArray(response.data.data) ? response.data.data : [];
    }
    throw new Error('Invalid response format');
  } catch (error) {
    console.error('Error fetching policies:', error);
    return [];
  }
};

export const fetchPolicy = async (id) => {
  try {
    const response = await axios.get(`/policies/${id}`);
    if (response.data && response.data.success && response.data.data) {
      return response.data.data;
    }
    throw new Error('Policy not found');
  } catch (error) {
    console.error(`Error fetching policy ${id}:`, error);
    throw error;
  }
};

export const createPolicy = async (policyData) => {
  try {
    const response = await axios.post('/policies', policyData);
    if (response.data && response.data.success) {
      return response.data.data;
    }
    throw new Error('Failed to create policy');
  } catch (error) {
    console.error('Error creating policy:', error);
    throw error;
  }
};

export const updatePolicy = async (id, policyData) => {
  try {
    const response = await axios.put(`/policies/${id}`, policyData);
    if (response.data && response.data.success) {
      return true;
    }
    throw new Error('Failed to update policy');
  } catch (error) {
    console.error(`Error updating policy ${id}:`, error);
    throw error;
  }
};

// Risk Assessment endpoints
export const fetchRiskAssessments = async () => {
  try {
    const response = await axios.get('/risk-assessments');
    if (response.data && response.data.success) {
      // Ensure we always return an array even if the API returns null or undefined
      return Array.isArray(response.data.data) ? response.data.data : [];
    }
    throw new Error('Invalid response format');
  } catch (error) {
    console.error('Error fetching risk assessments:', error);
    return [];
  }
};

export const fetchRiskAssessment = async (id) => {
  try {
    const response = await axios.get(`/risk-assessments/${id}`);
    if (response.data && response.data.success && response.data.data) {
      return response.data.data;
    }
    throw new Error('Risk assessment not found');
  } catch (error) {
    console.error(`Error fetching risk assessment ${id}:`, error);
    throw error;
  }
};

export const createRiskAssessment = async (assessmentData) => {
  try {
    const response = await axios.post('/risk-assessments', assessmentData);
    if (response.data && response.data.success) {
      return response.data.data;
    }
    throw new Error('Failed to create risk assessment');
  } catch (error) {
    console.error('Error creating risk assessment:', error);
    throw error;
  }
};

// Compliance Monitoring endpoints
export const fetchComplianceMonitors = async () => {
  try {
    const response = await axios.get('/compliance-monitors');
    if (response.data && response.data.success) {
      // Ensure we always return an array even if the API returns null or undefined
      return Array.isArray(response.data.data) ? response.data.data : [];
    }
    throw new Error('Invalid response format');
  } catch (error) {
    console.error('Error fetching compliance monitors:', error);
    return [];
  }
};

export const fetchComplianceMonitor = async (id) => {
  try {
    const response = await axios.get(`/compliance-monitors/${id}`);
    if (response.data && response.data.success && response.data.data) {
      return response.data.data;
    }
    throw new Error('Compliance monitor not found');
  } catch (error) {
    console.error(`Error fetching compliance monitor ${id}:`, error);
    throw error;
  }
};

export const createComplianceMonitor = async (monitorData) => {
  try {
    const response = await axios.post('/compliance-monitors', monitorData);
    if (response.data && response.data.success) {
      return response.data.data;
    }
    throw new Error('Failed to create compliance monitor');
  } catch (error) {
    console.error('Error creating compliance monitor:', error);
    throw error;
  }
};

export const updateComplianceMonitor = async (id, monitorData) => {
  try {
    const response = await axios.put(`/compliance-monitors/${id}`, monitorData);
    if (response.data && response.data.success) {
      return true;
    }
    throw new Error('Failed to update compliance monitor');
  } catch (error) {
    console.error(`Error updating compliance monitor ${id}:`, error);
    throw error;
  }
};

// Reporting endpoints
export const fetchReports = async () => {
  try {
    const response = await axios.get('/reports');
    if (response.data && response.data.success) {
      // Ensure we always return an array even if the API returns null or undefined
      return Array.isArray(response.data.data) ? response.data.data : [];
    }
    throw new Error('Invalid response format');
  } catch (error) {
    console.error('Error fetching reports:', error);
    return [];
  }
};

export const fetchReport = async (id) => {
  try {
    const response = await axios.get(`/reports/${id}`);
    if (response.data && response.data.success && response.data.data) {
      return response.data.data;
    }
    throw new Error('Report not found');
  } catch (error) {
    console.error(`Error fetching report ${id}:`, error);
    throw error;
  }
};

export const createReport = async (reportData) => {
  try {
    const response = await axios.post('/reports', reportData);
    if (response.data && response.data.success) {
      return response.data.data;
    }
    throw new Error('Failed to create report');
  } catch (error) {
    console.error('Error creating report:', error);
    throw error;
  }
};

// Notification endpoints
export const sendSmsNotification = async (data) => {
  try {
    const response = await axios.post('/send-sms-notification', data);
    return response.data;
  } catch (error) {
    console.error('Error sending SMS notification:', error);
    return {
      success: false,
      message: error.response?.data?.error || error.message || 'Failed to send SMS notification'
    };
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