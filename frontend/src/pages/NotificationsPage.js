import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, Form, Button, Alert, Tabs, Tab, Spinner, Badge } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const NotificationsPage = () => {
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [secretsStatus, setSecretsStatus] = useState({});
  const [activeTab, setActiveTab] = useState('send');
  const [formData, setFormData] = useState({
    recipient: '',
    subject: '',
    body: '',
    notification_type: 'general',
    urgency: 'normal'
  });
  const [secretFormData, setSecretFormData] = useState({
    name: 'TWILIO_ACCOUNT_SID',
    value: ''
  });
  
  const navigate = useNavigate();

  // Load secrets status on component mount
  useEffect(() => {
    fetchSecretsStatus();
  }, []);

  const fetchSecretsStatus = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/secrets/status');
      if (response.data.success) {
        setSecretsStatus(response.data.data);
      } else {
        setError('Failed to load secrets status: ' + (response.data.error || 'Unknown error'));
      }
    } catch (err) {
      setError('Error fetching secrets status: ' + (err.message || 'Unknown error'));
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSecretChange = (e) => {
    const { name, value } = e.target;
    setSecretFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setSending(true);
      setError(null);
      setSuccess(null);
      
      // Depending on the notification type, we might want to transform the data
      let requestData = { ...formData };
      
      if (formData.notification_type === 'compliance') {
        requestData.current_value = '0.85';  // Example values
        requestData.threshold_value = '0.75';
      } else if (formData.notification_type === 'risk_assessment') {
        requestData.model_name = 'Example Model';  // Example value
        requestData.risk_score = 0.75;  // Example value
      }
      
      const response = await axios.post('/api/notifications/send', requestData);
      
      if (response.data.success) {
        setSuccess('Notification sent successfully!');
        // Clear form
        setFormData({
          recipient: formData.recipient, // Keep the phone number
          subject: '',
          body: '',
          notification_type: 'general',
          urgency: 'normal'
        });
      } else {
        setError('Failed to send notification: ' + (response.data.error || 'Unknown error'));
      }
    } catch (err) {
      setError('Error sending notification: ' + (err.response?.data?.error || err.message || 'Unknown error'));
    } finally {
      setSending(false);
    }
  };

  const handleSecretSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setSending(true);
      setError(null);
      setSuccess(null);
      
      const response = await axios.post('/api/secrets/update', secretFormData);
      
      if (response.data.success) {
        setSuccess(`Secret ${secretFormData.name} updated successfully!`);
        // Clear form
        setSecretFormData({
          name: secretFormData.name,
          value: ''
        });
        // Refresh secrets status
        fetchSecretsStatus();
      } else {
        setError('Failed to update secret: ' + (response.data.error || 'Unknown error'));
      }
    } catch (err) {
      setError('Error updating secret: ' + (err.response?.data?.error || err.message || 'Unknown error'));
    } finally {
      setSending(false);
    }
  };

  const getNotificationTypes = () => [
    { value: 'general', label: 'General Message' },
    { value: 'governance', label: 'Governance Update' },
    { value: 'compliance', label: 'Compliance Alert' },
    { value: 'risk_assessment', label: 'Risk Assessment' }
  ];

  const getUrgencyLevels = () => [
    { value: 'low', label: 'Low' },
    { value: 'normal', label: 'Normal' },
    { value: 'high', label: 'High' },
    { value: 'critical', label: 'Critical' }
  ];
  
  const getSecretOptions = () => 
    Object.keys(secretsStatus).map(key => ({ 
      value: key, 
      label: key,
      description: secretsStatus[key]?.description || 'No description available',
      isSet: secretsStatus[key]?.is_set || false
    }));

  // Check if secrets are configured
  const areTwilioSecretsConfigured = () => {
    return (
      secretsStatus['TWILIO_ACCOUNT_SID']?.is_set &&
      secretsStatus['TWILIO_AUTH_TOKEN']?.is_set &&
      secretsStatus['TWILIO_PHONE_NUMBER']?.is_set
    );
  };

  return (
    <div className="container-fluid py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">Notifications</h2>
        <Button variant="outline-secondary" onClick={() => navigate(-1)}>
          <i className="fas fa-arrow-left me-2"></i>
          Back
        </Button>
      </div>
      
      {(error || success) && (
        <Alert variant={error ? 'danger' : 'success'} dismissible onClose={() => {
          setError(null);
          setSuccess(null);
        }}>
          {error || success}
        </Alert>
      )}
      
      <Tabs
        activeKey={activeTab}
        onSelect={(k) => setActiveTab(k)}
        className="mb-4"
      >
        <Tab eventKey="send" title="Send Notification">
          <Card>
            <Card.Header>
              <h5 className="mb-0">Send SMS Notification</h5>
            </Card.Header>
            <Card.Body>
              {loading ? (
                <div className="text-center py-4">
                  <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </Spinner>
                </div>
              ) : !areTwilioSecretsConfigured() ? (
                <Alert variant="warning">
                  <i className="fas fa-exclamation-triangle me-2"></i>
                  Twilio credentials are not configured. Please set up the required secrets in the Credentials tab.
                </Alert>
              ) : (
                <Form onSubmit={handleSubmit}>
                  <Form.Group className="mb-3">
                    <Form.Label>Recipient Phone Number</Form.Label>
                    <Form.Control
                      type="text"
                      name="recipient"
                      value={formData.recipient}
                      onChange={handleInputChange}
                      placeholder="Enter phone number (e.g., +1234567890)"
                      required
                    />
                    <Form.Text className="text-muted">
                      Phone number in E.164 format (+1234567890) or just the digits (1234567890)
                    </Form.Text>
                  </Form.Group>
                  
                  <Form.Group className="mb-3">
                    <Form.Label>Notification Type</Form.Label>
                    <Form.Select
                      name="notification_type"
                      value={formData.notification_type}
                      onChange={handleInputChange}
                    >
                      {getNotificationTypes().map(type => (
                        <option key={type.value} value={type.value}>{type.label}</option>
                      ))}
                    </Form.Select>
                  </Form.Group>
                  
                  <Form.Group className="mb-3">
                    <Form.Label>Urgency Level</Form.Label>
                    <Form.Select
                      name="urgency"
                      value={formData.urgency}
                      onChange={handleInputChange}
                    >
                      {getUrgencyLevels().map(level => (
                        <option key={level.value} value={level.value}>{level.label}</option>
                      ))}
                    </Form.Select>
                  </Form.Group>
                  
                  <Form.Group className="mb-3">
                    <Form.Label>Subject</Form.Label>
                    <Form.Control
                      type="text"
                      name="subject"
                      value={formData.subject}
                      onChange={handleInputChange}
                      placeholder="Enter notification subject"
                      required
                    />
                  </Form.Group>
                  
                  <Form.Group className="mb-3">
                    <Form.Label>Message Body</Form.Label>
                    <Form.Control
                      as="textarea"
                      rows={4}
                      name="body"
                      value={formData.body}
                      onChange={handleInputChange}
                      placeholder="Enter notification message"
                      required
                    />
                  </Form.Group>
                  
                  <div className="d-grid gap-2">
                    <Button 
                      variant="primary" 
                      type="submit" 
                      disabled={sending}
                    >
                      {sending ? (
                        <>
                          <Spinner
                            as="span"
                            animation="border"
                            size="sm"
                            role="status"
                            aria-hidden="true"
                            className="me-2"
                          />
                          Sending...
                        </>
                      ) : (
                        <>
                          <i className="fas fa-paper-plane me-2"></i>
                          Send Notification
                        </>
                      )}
                    </Button>
                  </div>
                </Form>
              )}
            </Card.Body>
          </Card>
        </Tab>
        
        <Tab eventKey="credentials" title="Credentials">
          <Card>
            <Card.Header>
              <h5 className="mb-0">API Credentials</h5>
            </Card.Header>
            <Card.Body>
              {loading ? (
                <div className="text-center py-4">
                  <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </Spinner>
                </div>
              ) : (
                <>
                  <div className="mb-4">
                    <h6>Current Status</h6>
                    <div className="table-responsive">
                      <table className="table table-bordered">
                        <thead>
                          <tr>
                            <th>Secret Name</th>
                            <th>Description</th>
                            <th>Status</th>
                          </tr>
                        </thead>
                        <tbody>
                          {Object.entries(secretsStatus).map(([key, value]) => (
                            <tr key={key}>
                              <td><code>{key}</code></td>
                              <td>{value.description}</td>
                              <td>
                                {value.is_set ? (
                                  <Badge bg="success">Configured</Badge>
                                ) : (
                                  <Badge bg="danger">Not Configured</Badge>
                                )}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                  
                  <hr />
                  
                  <h6>Update Credentials</h6>
                  <Form onSubmit={handleSecretSubmit}>
                    <Form.Group className="mb-3">
                      <Form.Label>Secret Name</Form.Label>
                      <Form.Select
                        name="name"
                        value={secretFormData.name}
                        onChange={handleSecretChange}
                      >
                        {getSecretOptions().map(option => (
                          <option key={option.value} value={option.value}>
                            {option.label} {option.isSet ? '(Configured)' : '(Not Configured)'}
                          </option>
                        ))}
                      </Form.Select>
                      <Form.Text className="text-muted">
                        {secretsStatus[secretFormData.name]?.description || 'No description available'}
                      </Form.Text>
                    </Form.Group>
                    
                    <Form.Group className="mb-3">
                      <Form.Label>Secret Value</Form.Label>
                      <Form.Control
                        type="password"
                        name="value"
                        value={secretFormData.value}
                        onChange={handleSecretChange}
                        placeholder="Enter secret value"
                        required
                      />
                    </Form.Group>
                    
                    <div className="d-grid gap-2">
                      <Button 
                        variant="primary" 
                        type="submit" 
                        disabled={sending}
                      >
                        {sending ? (
                          <>
                            <Spinner
                              as="span"
                              animation="border"
                              size="sm"
                              role="status"
                              aria-hidden="true"
                              className="me-2"
                            />
                            Updating...
                          </>
                        ) : (
                          <>
                            <i className="fas fa-save me-2"></i>
                            Update Secret
                          </>
                        )}
                      </Button>
                    </div>
                  </Form>
                </>
              )}
            </Card.Body>
          </Card>
        </Tab>
      </Tabs>
    </div>
  );
};

export default NotificationsPage;