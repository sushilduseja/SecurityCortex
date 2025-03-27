"""
Constants and configuration values for the AI Governance Dashboard.
This file centralizes constants used throughout the application.
"""

# API configuration
API_HOST = "localhost"
API_PORT = 8000
API_BASE_URL = f"http://{API_HOST}:{API_PORT}"

# Dashboard configuration
APP_TITLE = "AI Governance Dashboard"
APP_ICON = "🛡️"
APP_DESCRIPTION = "AI-powered governance, risk assessment, and compliance management"

# Database configuration
DB_PATH = "database/data/ai_governance.db"

# Agent configuration
GOVERNANCE_AGENT_CONFIG = {
    "policy_categories": [
        "Data Privacy", 
        "Model Transparency", 
        "Ethical AI", 
        "Bias Mitigation",
        "Security", 
        "Compliance",
        "Accountability",
        "Human Oversight"
    ]
}

RISK_ASSESSMENT_AGENT_CONFIG = {
    "risk_categories": [
        "Privacy Risk",
        "Bias Risk",
        "Security Risk",
        "Transparency Risk",
        "Accountability Risk",
        "Robustness Risk",
        "Safety Risk",
        "Compliance Risk"
    ]
}

MONITORING_AGENT_CONFIG = {
    "alert_levels": ["Critical", "Warning", "Normal", "Good"],
    "monitor_statuses": ["Active", "Inactive", "Paused"]
}

REPORTING_AGENT_CONFIG = {
    "report_types": [
        "Governance Summary",
        "Risk Assessment Overview",
        "Compliance Status",
        "Comprehensive Governance Report"
    ],
    "report_statuses": ["Draft", "Final", "Archived"]
}

# UI Colors
UI_COLORS = {
    # Primary colors
    "primary": "#007bff",
    "secondary": "#6c757d",
    "success": "#28a745",
    "danger": "#dc3545",
    "warning": "#ffc107",
    "info": "#17a2b8",
    
    # Alert levels
    "critical": "#d9534f",
    "warning_alert": "#f0ad4e",
    "normal": "#5bc0de",
    "good": "#5cb85c",
    
    # Chart colors
    "chart_blue": "#4e73df",
    "chart_red": "#e74a3b",
    "chart_green": "#1cc88a",
    "chart_yellow": "#f6c23e",
    "chart_teal": "#36b9cc",
    "chart_gray": "#858796"
}

# Page structure
PAGES = {
    "home": {
        "title": "Dashboard",
        "icon": "🏠",
        "description": "Overview of AI governance status"
    },
    "governance": {
        "title": "Governance",
        "icon": "📜",
        "description": "Manage AI governance policies"
    },
    "risk_assessment": {
        "title": "Risk Assessment",
        "icon": "🔍",
        "description": "Assess and manage AI risks"
    },
    "monitoring": {
        "title": "Monitoring",
        "icon": "📊",
        "description": "Monitor compliance status"
    },
    "reporting": {
        "title": "Reporting",
        "icon": "📋",
        "description": "Generate and view reports"
    }
}

# Risk assessment thresholds
RISK_THRESHOLDS = {
    "high": 75,
    "medium": 50,
    "low": 25
}

# Compliance thresholds
COMPLIANCE_THRESHOLDS = {
    "excellent": 90,
    "good": 80,
    "moderate": 70,
    "poor": 60
}

# Monitoring refresh intervals (in seconds)
REFRESH_INTERVALS = {
    "dashboard": 60,
    "monitors": 30,
    "real_time": 10
}

# Demo data flag (used for testing)
IS_DEMO_MODE = False

# Error messages
ERROR_MESSAGES = {
    "api_connection": "Error connecting to API. Please check that the backend service is running.",
    "data_load": "Error loading data. Please try refreshing the page.",
    "operation_failed": "Operation failed. Please try again later.",
    "invalid_input": "Invalid input provided. Please check your entries."
}

# Help texts
HELP_TEXTS = {
    "governance": {
        "policy_generation": "AI-generated policies are created based on best practices and regulatory requirements. Review and customize them for your specific needs.",
        "policy_categories": "Each policy category addresses different aspects of AI governance, from data privacy to model transparency and ethical considerations."
    },
    "risk_assessment": {
        "documentation": "Provide detailed documentation about your AI model for a more accurate risk assessment.",
        "risk_score": "Risk scores range from 0-100, with higher scores indicating greater risk. Scores above 75 are considered high risk."
    },
    "monitoring": {
        "alerts": "Critical alerts require immediate attention. Warning alerts should be addressed soon to prevent escalation.",
        "thresholds": "Thresholds determine when alerts are triggered. Adjust them based on your organization's risk tolerance."
    },
    "reporting": {
        "insights": "AI-generated insights highlight key findings and recommendations based on your governance data.",
        "report_types": "Different report types focus on specific aspects of AI governance, from policy management to risk assessment and compliance."
    }
}
