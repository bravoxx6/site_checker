import sqlite3
from sys import monitoring


def create_database():
    conn = sqlite3.connect('monitoring.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA journal_mode=WAL;')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monitoring_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            response_time REAL,
            status VARCHAR(50),
            error VARCHAR(555),
            port_info VARCHAR(255),
            status_level VARCHAR(200),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database IS READY")