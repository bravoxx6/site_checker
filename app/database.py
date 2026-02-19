import sqlite3

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

def create_settings_table():
    conn = sqlite3.connect('monitoring.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    # По умолчанию мониторинг выключен
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('monitoring_active', 'false')")
    conn.commit()
    conn.close()