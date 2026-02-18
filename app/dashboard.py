from fastapi import FastAPI, Request
import sqlite3
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

monitoring_state = {"is_active": False}  # Глобальная переменная для состояния мониторинга

def get_db_connection():
    conn = sqlite3.connect('monitoring.db', timeout=10, check_same_thread=False)
    # Это позволяет обращаться к полям по имени: row['url']
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/dashboard")
def get_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- API Эндпоинты ---

@app.get("/api/data")
def get_api_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = '''
        SELECT * FROM monitoring_results 
        WHERE id IN (SELECT MAX(id) FROM monitoring_results GROUP BY url)
        ORDER BY timestamp DESC
    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    
    # Превращаем Row объекты в обычные словари для JSON
    data = [dict(row) for row in rows]
    return JSONResponse(content=data)

@app.get("/api/status")
def get_status():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT * FROM monitoring_results 
        WHERE id IN (SELECT MAX(id) FROM monitoring_results GROUP BY url)
        ORDER BY timestamp DESC
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    
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

@app.post("/api/toggle")
def toggle_monitoring():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Сначала узнаем текущее состояние
    cursor.execute("SELECT value FROM settings WHERE key = 'monitoring_active'")
    current_value = cursor.fetchone()['value']
    
    # Меняем на противоположное
    new_value = 'True' if current_value == 'False' else 'False'
    cursor.execute("UPDATE settings SET value = ? WHERE key = 'monitoring_active'", (new_value,))
    
    conn.commit()
    conn.close()
    return {"is_active": (new_value == 'True')}