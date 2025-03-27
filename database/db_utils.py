import sqlite3
import datetime
from typing import List, Dict, Any, Optional, Union
from database.models import Policy, RiskAssessment, ComplianceMonitor, Report, Activity

def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect('database/data/ai_governance.db')
    conn.row_factory = sqlite3.Row
    return conn

# Policy functions
def get_all_policies() -> List[Dict[str, Any]]:
    """Retrieve all policies from the database."""
    conn = get_db_connection()
    policies = conn.execute('SELECT * FROM policies ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(policy) for policy in policies]

def get_policy(policy_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a specific policy by ID."""
    conn = get_db_connection()
    policy = conn.execute('SELECT * FROM policies WHERE id = ?', (policy_id,)).fetchone()
    conn.close()
    return dict(policy) if policy else None

def create_policy(policy: Policy) -> int:
    """Create a new policy and return its ID."""
    conn = get_db_connection()
    now = datetime.datetime.now().isoformat()
    cursor = conn.execute(
        'INSERT INTO policies (title, description, category, status, created_at, updated_at, content) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (policy.title, policy.description, policy.category, policy.status, now, now, policy.content)
    )
    policy_id = cursor.lastrowid
    
    # Log the activity
    conn.execute(
        'INSERT INTO activities (activity_type, description, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?)',
        ('create_policy', f'Created policy: {policy.title}', 'Governance Agent', policy_id, 'policy')
    )
    
    conn.commit()
    conn.close()
    return policy_id

def update_policy(policy: Policy) -> bool:
    """Update an existing policy."""
    conn = get_db_connection()
    now = datetime.datetime.now().isoformat()
    conn.execute(
        'UPDATE policies SET title = ?, description = ?, category = ?, status = ?, updated_at = ?, content = ? WHERE id = ?',
        (policy.title, policy.description, policy.category, policy.status, now, policy.content, policy.id)
    )
    
    # Log the activity
    conn.execute(
        'INSERT INTO activities (activity_type, description, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?)',
        ('update_policy', f'Updated policy: {policy.title}', 'Governance Agent', policy.id, 'policy')
    )
    
    conn.commit()
    conn.close()
    return True

# Risk Assessment functions
def get_all_risk_assessments() -> List[Dict[str, Any]]:
    """Retrieve all risk assessments from the database."""
    conn = get_db_connection()
    assessments = conn.execute('SELECT * FROM risk_assessments ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(assessment) for assessment in assessments]

def get_risk_assessment(assessment_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a specific risk assessment by ID."""
    conn = get_db_connection()
    assessment = conn.execute('SELECT * FROM risk_assessments WHERE id = ?', (assessment_id,)).fetchone()
    conn.close()
    return dict(assessment) if assessment else None

def create_risk_assessment(assessment: RiskAssessment) -> int:
    """Create a new risk assessment and return its ID."""
    conn = get_db_connection()
    now = datetime.datetime.now().isoformat()
    cursor = conn.execute(
        'INSERT INTO risk_assessments (title, model_name, risk_score, findings, recommendations, created_at, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (assessment.title, assessment.model_name, assessment.risk_score, assessment.findings, assessment.recommendations, now, assessment.status)
    )
    assessment_id = cursor.lastrowid
    
    # Log the activity
    conn.execute(
        'INSERT INTO activities (activity_type, description, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?)',
        ('create_risk_assessment', f'Created risk assessment: {assessment.title}', 'Risk Assessment Agent', assessment_id, 'risk_assessment')
    )
    
    conn.commit()
    conn.close()
    return assessment_id

# Compliance Monitor functions
def get_all_compliance_monitors() -> List[Dict[str, Any]]:
    """Retrieve all compliance monitors from the database."""
    conn = get_db_connection()
    monitors = conn.execute('SELECT * FROM compliance_monitors ORDER BY last_checked DESC').fetchall()
    conn.close()
    return [dict(monitor) for monitor in monitors]

def get_compliance_monitor(monitor_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a specific compliance monitor by ID."""
    conn = get_db_connection()
    monitor = conn.execute('SELECT * FROM compliance_monitors WHERE id = ?', (monitor_id,)).fetchone()
    conn.close()
    return dict(monitor) if monitor else None

def create_compliance_monitor(monitor: ComplianceMonitor) -> int:
    """Create a new compliance monitor and return its ID."""
    conn = get_db_connection()
    now = datetime.datetime.now().isoformat()
    cursor = conn.execute(
        'INSERT INTO compliance_monitors (name, description, model_or_system, threshold_value, current_value, status, last_checked, alert_level) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (monitor.name, monitor.description, monitor.model_or_system, monitor.threshold_value, monitor.current_value, monitor.status, now, monitor.alert_level)
    )
    monitor_id = cursor.lastrowid
    
    # Log the activity
    conn.execute(
        'INSERT INTO activities (activity_type, description, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?)',
        ('create_compliance_monitor', f'Created compliance monitor: {monitor.name}', 'Monitoring Agent', monitor_id, 'compliance_monitor')
    )
    
    conn.commit()
    conn.close()
    return monitor_id

def update_compliance_monitor(monitor: ComplianceMonitor) -> bool:
    """Update an existing compliance monitor."""
    conn = get_db_connection()
    now = datetime.datetime.now().isoformat()
    conn.execute(
        'UPDATE compliance_monitors SET name = ?, description = ?, model_or_system = ?, threshold_value = ?, current_value = ?, status = ?, last_checked = ?, alert_level = ? WHERE id = ?',
        (monitor.name, monitor.description, monitor.model_or_system, monitor.threshold_value, monitor.current_value, monitor.status, now, monitor.alert_level, monitor.id)
    )
    
    # Log the activity
    conn.execute(
        'INSERT INTO activities (activity_type, description, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?)',
        ('update_compliance_monitor', f'Updated compliance monitor: {monitor.name}', 'Monitoring Agent', monitor.id, 'compliance_monitor')
    )
    
    conn.commit()
    conn.close()
    return True

# Report functions
def get_all_reports() -> List[Dict[str, Any]]:
    """Retrieve all reports from the database."""
    conn = get_db_connection()
    reports = conn.execute('SELECT * FROM reports ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(report) for report in reports]

def get_report(report_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a specific report by ID."""
    conn = get_db_connection()
    report = conn.execute('SELECT * FROM reports WHERE id = ?', (report_id,)).fetchone()
    conn.close()
    return dict(report) if report else None

def create_report(report: Report) -> int:
    """Create a new report and return its ID."""
    conn = get_db_connection()
    now = datetime.datetime.now().isoformat()
    cursor = conn.execute(
        'INSERT INTO reports (title, description, report_type, created_at, content, insights, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (report.title, report.description, report.report_type, now, report.content, report.insights, report.status)
    )
    report_id = cursor.lastrowid
    
    # Log the activity
    conn.execute(
        'INSERT INTO activities (activity_type, description, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?)',
        ('create_report', f'Created report: {report.title}', 'Reporting Agent', report_id, 'report')
    )
    
    conn.commit()
    conn.close()
    return report_id

# Activity functions
def get_recent_activities(limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieve the most recent activities from the database."""
    conn = get_db_connection()
    activities = conn.execute('SELECT * FROM activities ORDER BY created_at DESC LIMIT ?', (limit,)).fetchall()
    conn.close()
    return [dict(activity) for activity in activities]

def log_activity(activity: Activity) -> int:
    """Log a new activity and return its ID."""
    conn = get_db_connection()
    now = datetime.datetime.now().isoformat()
    cursor = conn.execute(
        'INSERT INTO activities (activity_type, description, created_at, actor, related_entity_id, related_entity_type) VALUES (?, ?, ?, ?, ?, ?)',
        (activity.activity_type, activity.description, now, activity.actor, activity.related_entity_id, activity.related_entity_type)
    )
    activity_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return activity_id
