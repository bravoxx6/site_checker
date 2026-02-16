import requests, time, logging, socket, asyncio
from urllib.parse import urlparse
from ports import check_port
from checker import check_url
from logger import logging, log_result
import json
from notifier import send_notification
file_path = 'config.json'

try:
    with open(file_path, 'r') as f:
        config = json.load(f)
        urls_to_check = config.get("urls", [])
        ports_to_check = config.get("ports", [])
        
except FileNotFoundError:
    print(f"Configuration file '{file_path}' not found. Please create it with the necessary URLs.")
    urls_to_check = []
    

def analyse_urls(urls):
    for url in urls:
        result = check_url(url)
        print(f"URL: {result['url']}, Response Time: {result['response_time']} seconds, Status: {result['status']}, Error: {result['error']}, Open Ports: {result['port_info']}")
        log_result(result)
        if result['status'] == 'DOWN':
            send_notification(f"Site is down: {result['url']}, Error: {result['error']}")

try:
    while True:
        print("Starting URL analysis...")
        analyse_urls(urls_to_check)
        time.sleep(5)
except KeyboardInterrupt:
    print("URL analysis stopped by user.")