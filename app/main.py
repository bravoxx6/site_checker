import time
from checker import check_url
from logger import log_result
import json
from notifier import send_notification
file_path = 'config.json'
from concurrent.futures import ThreadPoolExecutor
import sqlite3
import threading

# SQLite connection pool with mutex to prevent concurrent access
_db_lock = threading.Lock()
DB_PATH = 'monitoring.db'

def get_db_connection():
    """Get a database connection with proper settings for concurrent access."""
    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
    conn.execute('PRAGMA journal_mode=WAL;')
    conn.execute('PRAGMA synchronous=NORMAL;')
    conn.execute('PRAGMA busy_timeout=30000;')
    return conn

try:
    with open(file_path, 'r') as f:
        config = json.load(f)
        urls_to_check = config.get("urls", [])
        ports_to_check = config.get("ports", [])
        
except FileNotFoundError:
    print(f"Configuration file '{file_path}' not found. Please create it with the necessary URLs and ports.")
    urls_to_check = []
    ports_to_check = [80, 20, 443, 21, 22, 3306]
    

def analyse_url(url):
    down_count = 0
    last_result = None
    for _ in range(3):
        result = check_url(url, ports_to_check)
        last_result = result

        # Use lock to prevent concurrent database writes
        with _db_lock:
            conn = get_db_connection()
            try:
                log_result(result, conn)
            finally:
                conn.close()
        
        if result['status'] == "DOWN":
            down_count += 1
    print(f"URL: {last_result['url']}, "
            f"Response Time: {last_result['response_time']}s, "
            f"Status: {last_result['status']}, "
            f"Error: {last_result['error']}, "
            f"Open Ports: {last_result['port_info']}, "
            f"Status Level: {last_result['status_level']}"
            )
    
    if down_count == 3:
        message = (
            f"🚨 SITE DOWN\n\n"
            f"🌐 URL: {last_result['url']}\n"
            f"🚫 Status: {last_result['status']}\n"
            f"⚠️ Error: {last_result['error']}\n"
            f"🔌 Ports: {last_result['port_info']}\n"
            f"📊 Status Level: {last_result['status_level']}\n"
        )

        send_notification(message)

def is_monitoring_enabled():
    try:
        with _db_lock:
            conn = get_db_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM settings WHERE key = 'monitoring_active'")
                row = cursor.fetchone()
                return row and row[0] == 'True'
            finally:
                conn.close()
    except Exception as e:
        print(f"Error checking settings: {e}")
        return False

# В основном блоке программы:
if __name__ == "__main__":
    while True:
        if is_monitoring_enabled():
            print("Мониторинг активен, начинаю проверку...")
            with ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(analyse_url, urls_to_check)
        else:
            print("Мониторинг на паузе. Жду...") # При остановленном мониторинге просто ждем и не выполняем проверки. Коду немного нужно времени для обработки команды остановки
        
        time.sleep(10) # Проверяем статус и крутим цикл каждые 10 сек
