import sqlite3
import os

def init_db():
    """Initialize the SQLite database with the required tables if they don't exist."""
    # Create the database directory if it doesn't exist
    os.makedirs('database/data', exist_ok=True)
    
    # Connect to the database (this will create it if it doesn't exist)
    conn = sqlite3.connect('database/data/ai_governance.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS policies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
