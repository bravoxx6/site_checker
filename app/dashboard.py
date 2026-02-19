from fastapi import FastAPI, Request
import sqlite3
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import threading

app = FastAPI()
templates = Jinja2Templates(directory="templates")

monitoring_state = {"is_active": False}  # Глобальная переменная для состояния мониторинга

# Shared lock for database access
_db_lock = threading.Lock()
DB_PATH = 'monitoring.db'

def get_db_connection():
    """Get a database connection with proper settings for concurrent access."""
    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL;')
    conn.execute('PRAGMA synchronous=NORMAL;')
    conn.execute('PRAGMA busy_timeout=30000;')
    return conn

@app.get("/dashboard")
def get_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- API Эндпоинты ---

@app.get("/api/data")
def get_api_data():
    with _db_lock:
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = '''
                SELECT * FROM monitoring_results 
                WHERE id IN (SELECT MAX(id) FROM monitoring_results GROUP BY url)
                ORDER BY timestamp DESC
            '''
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Превращаем Row объекты в обычные словари для JSON
            data = [dict(row) for row in rows]
            return JSONResponse(content=data)
        finally:
            conn.close()

@app.get("/api/status")
def get_status():
    with _db_lock:
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            
            query = '''
                SELECT * FROM monitoring_results 
                WHERE id IN (SELECT MAX(id) FROM monitoring_results GROUP BY url)
                ORDER BY timestamp DESC
            '''
            cursor.execute(query)
            data = cursor.fetchall()
            
            # Преобразуем данные в список словарей для JSON ответа
            results = []
            for row in data:
                results.append({
                    "url": row["url"],
                    "response_time": row["response_time"],
                    "status": row["status"],
                    "error": row["error"],
                    "port_info": row["port_info"],
                    "status_level": row["status_level"],
                    "timestamp": row["timestamp"]
                })
            
            return JSONResponse(content={"results": results})
        finally:
            conn.close()

@app.post("/api/toggle")
def toggle_monitoring():
    with _db_lock:
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            
            # Сначала узнаем текущее состояние
            cursor.execute("SELECT value FROM settings WHERE key = 'monitoring_active'")
            current_value = cursor.fetchone()['value']
            
            # Меняем на противоположное
            new_value = 'True' if current_value == 'False' else 'False'
            cursor.execute("UPDATE settings SET value = ? WHERE key = 'monitoring_active'", (new_value,))
            
            conn.commit()
            return {"is_active": (new_value == 'True')}
        finally:
            conn.close()
