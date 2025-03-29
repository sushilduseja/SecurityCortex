import sqlite3
import os
import datetime
from typing import List, Dict, Any, Optional, Union

from app.domain.models import Policy, RiskAssessment, ComplianceMonitor, Report, Activity
from app.domain.repositories import (
    PolicyRepository, RiskAssessmentRepository, 
    ComplianceMonitorRepository, ReportRepository, ActivityRepository
)

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

class SQLitePolicyRepository(PolicyRepository):
    def get_all(self) -> List[Dict[str, Any]]:
        """Retrieve all policies from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM policies ORDER BY created_at DESC')
        policies = cursor.fetchall()
        cursor.close()
        conn.close()
        return policies or []
    
    def get_by_id(self, policy_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a specific policy by ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM policies WHERE id = ?', (policy_id,))
        policy = cursor.fetchone()
        cursor.close()
        conn.close()
        return policy
    
    def create(self, policy: Policy) -> int:
        """Create a new policy and return its ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO policies (title, description, category, status, created_at, updated_at, content) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (policy.title, policy.description, policy.category, policy.status, now, now, policy.content)
        )
        policy_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return policy_id
    
    def update(self, policy: Policy) -> bool:
        """Update an existing policy."""
        if not policy.id:
            return False
            
        conn = get_db_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute(
            'UPDATE policies SET title = ?, description = ?, category = ?, status = ?, updated_at = ?, content = ? WHERE id = ?',
            (policy.title, policy.description, policy.category, policy.status, now, policy.content, policy.id)
        )
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return success

class SQLiteRiskAssessmentRepository(RiskAssessmentRepository):
    def get_all(self) -> List[Dict[str, Any]]:
        """Retrieve all risk assessments from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM risk_assessments ORDER BY created_at DESC')
        assessments = cursor.fetchall()
        cursor.close()
        conn.close()
        return assessments or []
    
    def get_by_id(self, assessment_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a specific risk assessment by ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM risk_assessments WHERE id = ?', (assessment_id,))
        assessment = cursor.fetchone()
        cursor.close()
        conn.close()
        return assessment
    
    def create(self, assessment: RiskAssessment) -> int:
        """Create a new risk assessment and return its ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO risk_assessments (title, model_name, risk_score, findings, recommendations, created_at, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (assessment.title, assessment.model_name, assessment.risk_score, assessment.findings, assessment.recommendations, now, assessment.status)
        )
        assessment_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return assessment_id

class SQLiteComplianceMonitorRepository(ComplianceMonitorRepository):
    def get_all(self) -> List[Dict[str, Any]]:
        """Retrieve all compliance monitors from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM compliance_monitors ORDER BY last_checked DESC')
        monitors = cursor.fetchall()
        cursor.close()
        conn.close()
        return monitors or []
    
    def get_by_id(self, monitor_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a specific compliance monitor by ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM compliance_monitors WHERE id = ?', (monitor_id,))
        monitor = cursor.fetchone()
        cursor.close()
        conn.close()
        return monitor
    
    def create(self, monitor: ComplianceMonitor) -> int:
        """Create a new compliance monitor and return its ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO compliance_monitors (name, description, model_or_system, threshold_value, current_value, status, last_checked, alert_level) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (monitor.name, monitor.description, monitor.model_or_system, monitor.threshold_value, monitor.current_value, monitor.status, now, monitor.alert_level)
        )
        monitor_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return monitor_id
    
    def update(self, monitor: ComplianceMonitor) -> bool:
        """Update an existing compliance monitor."""
        if not monitor.id:
            return False
            
        conn = get_db_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute(
            'UPDATE compliance_monitors SET name = ?, description = ?, model_or_system = ?, threshold_value = ?, current_value = ?, status = ?, last_checked = ?, alert_level = ? WHERE id = ?',
            (monitor.name, monitor.description, monitor.model_or_system, monitor.threshold_value, monitor.current_value, monitor.status, now, monitor.alert_level, monitor.id)
        )
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return success

class SQLiteReportRepository(ReportRepository):
    def get_all(self) -> List[Dict[str, Any]]:
        """Retrieve all reports from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reports ORDER BY created_at DESC')
        reports = cursor.fetchall()
        cursor.close()
        conn.close()
        return reports or []
    
    def get_by_id(self, report_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a specific report by ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reports WHERE id = ?', (report_id,))
        report = cursor.fetchone()
        cursor.close()
        conn.close()
        return report
    
    def create(self, report: Report) -> int:
        """Create a new report and return its ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO reports (title, description, report_type, created_at, content, insights, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (report.title, report.description, report.report_type, now, report.content, report.insights, report.status)
        )
        report_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return report_id

class SQLiteActivityRepository(ActivityRepository):
    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve the most recent activities from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM activities ORDER BY created_at DESC LIMIT ?', (limit,))
        activities = cursor.fetchall()
        cursor.close()
        conn.close()
        return activities or []
    
    def log(self, activity: Activity) -> int:
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