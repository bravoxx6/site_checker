import logging
import json
from datetime import datetime
import sqlite3
import database

logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format='%(message)s',
)
conn = sqlite3.connect('monitoring.db')

def log_result(result: dict):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "url": result.get("url"),
        "response_time": result.get("response_time"),
        "status": result.get("status"),
        "error": result.get("error"),
        "port_info": json.dumps(result.get("port_info", [])),
        "status_level": result.get("status_level", "INFO")
    }
    level = result.get("status_level", "INFO")
    if level == "ERROR":
        logging.error(json.dumps(log_entry, ensure_ascii=False))
    elif level == "WARNING":
        logging.warning(json.dumps(log_entry, ensure_ascii=False))
    elif level == "INFO":
        logging.info(json.dumps(log_entry, ensure_ascii=False))

    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO monitoring_results (url, timestamp, response_time, status, error, port_info, status_level)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            log_entry['url'],
            log_entry['timestamp'],
            log_entry['response_time'],
            log_entry['status'],
            str(log_entry['error']) if log_entry['error'] else None,
            log_entry['port_info'],
            log_entry['status_level']
        ))
        print("Logged to database: ", log_entry)
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
            
  
    

