import axios from 'axios';

/**
 * Check if required secrets are available
 * @param {Array<string>} secretKeys - Array of secret keys to check
 * @returns {Promise<Array<{key: string, available: boolean}>>} Status of each secret
 */
export const checkSecrets = async (secretKeys) => {
  try {
    const response = await axios.post('/api/v1/check-secrets', { secretKeys });
    return response.data.secretsStatus || [];
  } catch (error) {
    console.error('Error checking secrets:', error);
    // Return all secrets as unavailable if the API fails
    return secretKeys.map(key => ({ key, available: false }));
  }
};

/**
 * Request missing secrets
 * @param {Array<string>} secretKeys - Array of secret keys to request
 * @param {string} message - Message explaining why the secrets are needed
 * @returns {Promise<{success: boolean, message: string}>} Result of the request
 */
export const requestSecrets = async (secretKeys, message) => {
  try {
    const response = await axios.post('/api/v1/request-secrets', { 
      secretKeys,
      message
    });
    return {
      success: true,
      message: response.data.message || 'Secrets requested successfully'
    };
  } catch (error) {
    console.error('Error requesting secrets:', error);
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to request secrets'
    };
  }
};