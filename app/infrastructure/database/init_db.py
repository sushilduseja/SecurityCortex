import sqlite3
import os
import datetime
from app.domain.models import Policy, RiskAssessment, ComplianceMonitor, Report, Activity
from app.infrastructure.database.sqlite_repositories import get_db_connection, DB_PATH

def init_db():
    """Initialize the SQLite database with the required tables if they don't exist."""
    # Ensure database directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS policies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT,
        status TEXT,
        created_at TEXT,
        updated_at TEXT,
        content TEXT
    );
    
    CREATE TABLE IF NOT EXISTS risk_assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        model_name TEXT,
        risk_score REAL,
        findings TEXT,
        recommendations TEXT,
        created_at TEXT,
        status TEXT
    );
    
    CREATE TABLE IF NOT EXISTS compliance_monitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        model_or_system TEXT,
        threshold_value REAL,
        current_value REAL,
        status TEXT,
        last_checked TEXT,
        alert_level TEXT
    );
    
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        report_type TEXT,
        created_at TEXT,
        content TEXT,
        insights TEXT,
        status TEXT
    );
    
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_type TEXT,
        description TEXT,
        created_at TEXT,
        actor TEXT,
        related_entity_id INTEGER,
        related_entity_type TEXT
    );
    ''')
    
    conn.commit()
    
    # Check if we need to preload data (only if tables are empty)
    cursor.execute('SELECT COUNT(*) as count FROM policies')
    policy_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM risk_assessments')
    assessment_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM compliance_monitors')
    monitor_count = cursor.fetchone()['count']
    
    # If tables are empty, preload sample data
    if policy_count == 0 and assessment_count == 0 and monitor_count == 0:
        preload_sample_data(conn)
    
    cursor.close()
    conn.close()
    
    print("Database initialized successfully.")

def preload_sample_data(conn):
    """Preload sample data aligned with NIST AI Risk Management Framework."""
    from database.db_init_sqlite import preload_sample_data as original_preload_sample_data
    original_preload_sample_data(conn)