import sqlite3
import os
import datetime
from typing import List, Dict, Any, Optional, Union
from database.models import Policy, RiskAssessment, ComplianceMonitor, Report, Activity

# Create database directory if it doesn't exist
os.makedirs('database/data', exist_ok=True)
DB_PATH = 'database/data/aigovernance.db'

def dict_factory(cursor, row):
    """Convert SQLite row objects to dictionaries."""
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    return conn

# Policy functions
def get_all_policies() -> List[Dict[str, Any]]:
    """Retrieve all policies from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM policies ORDER BY created_at DESC')
    policies = cursor.fetchall()
    cursor.close()
    conn.close()
    return policies or []

def get_policy(policy_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a specific policy by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM policies WHERE id = ?', (policy_id,))
    policy = cursor.fetchone()
    cursor.close()
    conn.close()
    return policy

def create_policy(policy: Policy) -> int:
    """Create a new policy and return its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    cursor.execute(
        'INSERT INTO policies (title, description, category, status, created_at, updated_at, content) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (policy.title, policy.description, policy.category, policy.status, now, now, policy.content)
    )
    policy_id = cursor.lastrowid
    
    # Log the activity
    cursor.execute(
        'INSERT INTO activities (activity_type, description, created_at, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?, ?)',
        ('create_policy', f'Created policy: {policy.title}', now, 'Governance Agent', policy_id, 'policy')
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    return policy_id

def update_policy(policy: Policy) -> bool:
    """Update an existing policy."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    cursor.execute(
        'UPDATE policies SET title = ?, description = ?, category = ?, status = ?, updated_at = ?, content = ? WHERE id = ?',
        (policy.title, policy.description, policy.category, policy.status, now, policy.content, policy.id)
    )
    
    # Log the activity
    cursor.execute(
        'INSERT INTO activities (activity_type, description, created_at, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?, ?)',
        ('update_policy', f'Updated policy: {policy.title}', now, 'Governance Agent', policy.id, 'policy')
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    return True

# Risk Assessment functions
def get_all_risk_assessments() -> List[Dict[str, Any]]:
    """Retrieve all risk assessments from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM risk_assessments ORDER BY created_at DESC')
    assessments = cursor.fetchall()
    cursor.close()
    conn.close()
    return assessments or []

def get_risk_assessment(assessment_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a specific risk assessment by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM risk_assessments WHERE id = ?', (assessment_id,))
    assessment = cursor.fetchone()
    cursor.close()
    conn.close()
    return assessment

def create_risk_assessment(assessment: RiskAssessment) -> int:
    """Create a new risk assessment and return its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    cursor.execute(
        'INSERT INTO risk_assessments (title, model_name, risk_score, findings, recommendations, created_at, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (assessment.title, assessment.model_name, assessment.risk_score, assessment.findings, assessment.recommendations, now, assessment.status)
    )
    assessment_id = cursor.lastrowid
    
    # Log the activity
    cursor.execute(
        'INSERT INTO activities (activity_type, description, created_at, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?, ?)',
        ('create_risk_assessment', f'Created risk assessment: {assessment.title}', now, 'Risk Assessment Agent', assessment_id, 'risk_assessment')
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    return assessment_id

# Compliance Monitor functions
def get_all_compliance_monitors() -> List[Dict[str, Any]]:
    """Retrieve all compliance monitors from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM compliance_monitors ORDER BY last_checked DESC')
    monitors = cursor.fetchall()
    cursor.close()
    conn.close()
    return monitors or []

def get_compliance_monitor(monitor_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a specific compliance monitor by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM compliance_monitors WHERE id = ?', (monitor_id,))
    monitor = cursor.fetchone()
    cursor.close()
    conn.close()
    return monitor

def create_compliance_monitor(monitor: ComplianceMonitor) -> int:
    """Create a new compliance monitor and return its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    cursor.execute(
        'INSERT INTO compliance_monitors (name, description, model_or_system, threshold_value, current_value, status, last_checked, alert_level) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (monitor.name, monitor.description, monitor.model_or_system, monitor.threshold_value, monitor.current_value, monitor.status, now, monitor.alert_level)
    )
    monitor_id = cursor.lastrowid
    
    # Log the activity
    cursor.execute(
        'INSERT INTO activities (activity_type, description, created_at, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?, ?)',
        ('create_compliance_monitor', f'Created compliance monitor: {monitor.name}', now, 'Monitoring Agent', monitor_id, 'compliance_monitor')
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    return monitor_id

def update_compliance_monitor(monitor: ComplianceMonitor) -> bool:
    """Update an existing compliance monitor."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    cursor.execute(
        'UPDATE compliance_monitors SET name = ?, description = ?, model_or_system = ?, threshold_value = ?, current_value = ?, status = ?, last_checked = ?, alert_level = ? WHERE id = ?',
        (monitor.name, monitor.description, monitor.model_or_system, monitor.threshold_value, monitor.current_value, monitor.status, now, monitor.alert_level, monitor.id)
    )
    
    # Log the activity
    cursor.execute(
        'INSERT INTO activities (activity_type, description, created_at, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?, ?)',
        ('update_compliance_monitor', f'Updated compliance monitor: {monitor.name}', now, 'Monitoring Agent', monitor.id, 'compliance_monitor')
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    return True

# Report functions
def get_all_reports() -> List[Dict[str, Any]]:
    """Retrieve all reports from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reports ORDER BY created_at DESC')
    reports = cursor.fetchall()
    cursor.close()
    conn.close()
    return reports or []

def get_report(report_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a specific report by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reports WHERE id = ?', (report_id,))
    report = cursor.fetchone()
    cursor.close()
    conn.close()
    return report

def create_report(report: Report) -> int:
    """Create a new report and return its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    cursor.execute(
        'INSERT INTO reports (title, description, report_type, created_at, content, insights, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (report.title, report.description, report.report_type, now, report.content, report.insights, report.status)
    )
    report_id = cursor.lastrowid
    
    # Log the activity
    cursor.execute(
        'INSERT INTO activities (activity_type, description, created_at, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?, ?)',
        ('create_report', f'Created report: {report.title}', now, 'Reporting Agent', report_id, 'report')
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    return report_id

# Activity functions
def get_recent_activities(limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieve the most recent activities from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM activities ORDER BY created_at DESC LIMIT ?', (limit,))
    activities = cursor.fetchall()
    cursor.close()
    conn.close()
    return activities or []

def log_activity(activity: Activity) -> int:
    """Log a new activity and return its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    cursor.execute(
        'INSERT INTO activities (activity_type, description, created_at, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?, ?)',
        (activity.activity_type, activity.description, now, activity.actor, activity.related_entity_id, activity.related_entity_type)
    )
    activity_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return activity_id