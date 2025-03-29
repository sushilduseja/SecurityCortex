import axios from 'axios';

// No need for a base URL as we're now using absolute paths
// axios.defaults.baseURL = '';
axios.defaults.headers.common['Content-Type'] = 'application/json';

// Dashboard endpoints
export const fetchDashboardMetrics = async () => {
  try {
    const response = await axios.get('/api/dashboard/metrics');
    return response.data; // Backend returns the data directly
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
    const response = await axios.get('/api/dashboard/compliance-status-chart');
    return response.data; // Backend returns the data directly
  } catch (error) {
    console.error('Error fetching compliance status chart:', error);
    return { labels: [], datasets: [{ data: [], backgroundColor: [] }] };
  }
};

export const fetchRiskDistributionChart = async () => {
  try {
    const response = await axios.get('/api/dashboard/risk-distribution-chart');
    return response.data; // Backend returns the data directly
  } catch (error) {
    console.error('Error fetching risk distribution chart:', error);
    return { labels: [], datasets: [] };
  }
};

export const fetchRecentActivities = async () => {
  try {
    const response = await axios.get('/api/dashboard/activities');
    return response.data; // Backend returns the data directly
  } catch (error) {
    console.error('Error fetching recent activities:', error);
    return [];
  }
};

// Governance endpoints
export const fetchPolicies = async () => {
  try {
    const response = await axios.get('/api/policies');
    return response.data; // Backend returns array directly
  } catch (error) {
    console.error('Error fetching policies:', error);
    return [];
  }
};

export const fetchPolicy = async (id) => {
  try {
    const response = await axios.get(`/api/policies/${id}`);
    return response.data; // Backend returns the policy directly
  } catch (error) {
    console.error(`Error fetching policy ${id}:`, error);
    throw error;
  }
};

export const createPolicy = async (policyData) => {
  try {
    const response = await axios.post('/api/policies', policyData);
    return response.data; // Backend returns result directly
  } catch (error) {
    console.error('Error creating policy:', error);
    throw error;
  }
};

export const updatePolicy = async (id, policyData) => {
  try {
    const response = await axios.put(`/api/policies/${id}`, policyData);
    return response.data.success; // Returns success boolean
  } catch (error) {
    console.error(`Error updating policy ${id}:`, error);
    throw error;
  }
};

// Risk Assessment endpoints
export const fetchRiskAssessments = async () => {
  try {
    const response = await axios.get('/api/risk-assessments');
    return response.data; // Backend returns array directly
  } catch (error) {
    console.error('Error fetching risk assessments:', error);
    return [];
  }
};

export const fetchRiskAssessment = async (id) => {
  try {
    const response = await axios.get(`/api/risk-assessments/${id}`);
    return response.data; // Backend returns assessment directly
  } catch (error) {
    console.error(`Error fetching risk assessment ${id}:`, error);
    throw error;
  }
};

export const createRiskAssessment = async (assessmentData) => {
  try {
    const response = await axios.post('/api/risk-assessments', assessmentData);
    return response.data; // Backend returns result directly
  } catch (error) {
    console.error('Error creating risk assessment:', error);
    throw error;
  }
};

// Compliance Monitoring endpoints
export const fetchComplianceMonitors = async () => {
  try {
    const response = await axios.get('/api/compliance-monitors');
    return response.data; // Backend returns array directly
  } catch (error) {
    console.error('Error fetching compliance monitors:', error);
    return [];
  }
};

export const fetchComplianceMonitor = async (id) => {
  try {
    const response = await axios.get(`/api/compliance-monitors/${id}`);
    return response.data; // Backend returns monitor directly
  } catch (error) {
    console.error(`Error fetching compliance monitor ${id}:`, error);
    throw error;
  }
};

export const createComplianceMonitor = async (monitorData) => {
  try {
    const response = await axios.post('/api/compliance-monitors', monitorData);
    return response.data; // Backend returns result directly
  } catch (error) {
    console.error('Error creating compliance monitor:', error);
    throw error;
  }
};

export const updateComplianceMonitor = async (id, monitorData) => {
  try {
    const response = await axios.put(`/api/compliance-monitors/${id}`, monitorData);
    return response.data.success; // Returns success boolean
  } catch (error) {
    console.error(`Error updating compliance monitor ${id}:`, error);
    throw error;
  }
};

// Reporting endpoints
export const fetchReports = async () => {
  try {
    const response = await axios.get('/api/reports');
    return response.data; // Backend returns array directly
  } catch (error) {
    console.error('Error fetching reports:', error);
    return [];
  }
};

export const fetchReport = async (id) => {
  try {
    const response = await axios.get(`/api/reports/${id}`);
    return response.data; // Backend returns report directly
  } catch (error) {
    console.error(`Error fetching report ${id}:`, error);
    throw error;
  }
};

export const createReport = async (reportData) => {
  try {
    const response = await axios.post('/api/reports', reportData);
    return response.data; // Backend returns result directly
  } catch (error) {
    console.error('Error creating report:', error);
    throw error;
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