from fastapi import FastAPI, Request
import sqlite3
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db_connection():
    conn = sqlite3.connect('monitoring.db', timeout=10, check_same_thread=False)
    # Это позволяет обращаться к полям по имени: row['url']
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/dashboard")
def get_dashboard(request: Request):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Запрос берет последнюю запись для каждого уникального URL
    query = '''
        SELECT * FROM monitoring_results 
        WHERE id IN (SELECT MAX(id) FROM monitoring_results GROUP BY url)
        ORDER BY timestamp DESC
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    
    return templates.TemplateResponse("index.html", {"request": request, "results": data})