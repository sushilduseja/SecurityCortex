import axios from 'axios';

/**
 * Service for interacting with the notification API
 */
class NotificationService {
  /**
   * Create a new notification service
   * @param {string} apiUrl - Base API URL
   */
  constructor(apiUrl = '/api/v1') {
    this.apiUrl = apiUrl;
    this.notificationEndpoint = `${apiUrl}/notifications`;
  }

  /**
   * Send a notification
   * @param {string} provider - Notification provider (e.g., 'sms', 'console')
   * @param {string} recipient - Recipient (e.g., phone number)
   * @param {string} message - Notification message
   * @param {Object} metadata - Additional metadata
   * @returns {Promise<Object>} Response data
   */
  async sendNotification(provider, recipient, message, metadata = {}) {
    try {
      const response = await axios.post(`${this.notificationEndpoint}/send`, {
        provider,
        recipient,
        message,
        metadata
      });
      
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error sending notification:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message,
        details: error.response?.data?.details || {}
      };
    }
  }

  /**
   * Send an SMS notification
   * @param {string} phoneNumber - Recipient phone number
   * @param {string} message - Notification message
   * @param {Object} metadata - Additional metadata
   * @returns {Promise<Object>} Response data
   */
  async sendSmsNotification(phoneNumber, message, metadata = {}) {
    return this.sendNotification('sms', phoneNumber, message, metadata);
  }

  /**
   * Send a console notification (for testing)
   * @param {string} recipient - Recipient identifier
   * @param {string} message - Notification message
   * @param {Object} metadata - Additional metadata
   * @returns {Promise<Object>} Response data
   */
  async sendConsoleNotification(recipient, message, metadata = {}) {
    return this.sendNotification('console', recipient, message, metadata);
  }
}

// Create a singleton instance
const notificationService = new NotificationService();

export default notificationService;