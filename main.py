import time
from checker import check_url
from logger import log_result
import json
from notifier import send_notification
file_path = 'config.json'
from concurrent.futures import ThreadPoolExecutor
import sqlite3

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
    conn = sqlite3.connect('monitoring.db')
    conn.execute('PRAGMA journal_mode=WAL;')
    for _ in range(3):
        result = check_url(url, ports_to_check)
        last_result = result

        log_result(result, conn)
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

def analyse_urls_concurrently(urls):
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(analyse_url, urls)

try:
    print("Starting URL analysis...")
    while True:
        analyse_urls_concurrently(urls_to_check)
        time.sleep(5)
except KeyboardInterrupt:
    print("URL analysis stopped by user.")
    