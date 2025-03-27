import os
import psycopg2
from sqlalchemy import create_engine, text

def init_db():
    """Initialize the PostgreSQL database with the required tables if they don't exist."""
    # Get PostgreSQL connection string from environment variables
    db_url = os.environ.get('DATABASE_URL')
    
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set")
    
    # Connect to the database
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS policies (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        content TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS risk_assessments (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        model_name TEXT,
        risk_score REAL,
        findings TEXT,
        recommendations TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS compliance_monitors (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        model_or_system TEXT,
        threshold_value REAL,
        current_value REAL,
        status TEXT,
        last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        alert_level TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        report_type TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        content TEXT,
        insights TEXT,
        status TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS activities (
        id SERIAL PRIMARY KEY,
        activity_type TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        actor TEXT,
        related_entity_id INTEGER,
        related_entity_type TEXT
    )
    ''')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    return True

if __name__ == "__main__":
    init_db()
