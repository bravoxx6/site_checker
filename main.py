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
        down_count = 0
        last_result = None

        for _ in range(3):
            result = check_url(url)
            last_result = result

            log_result(result)
            if result['status'] == "DOWN":
                down_count += 1

        print(f"URL: {last_result['url']}, "
              f"Response Time: {last_result['response_time']}s, "
              f"Status: {last_result['status']}, "
              f"Error: {last_result['error']}, "
              f"Open Ports: {last_result['port_info']}")
        
        if down_count == 3:
            message = (
                f"🚨 SITE DOWN\n\n"
                f"URL: {last_result['url']}\n"
                f"Status: {last_result['status']}\n"
                f"Error: {last_result['error']}\n"
                f"Ports: {last_result['port_info']}"
            )

            send_notification(message)


try:
    print("Starting URL analysis...")
    while True:
        analyse_urls(urls_to_check)
        time.sleep(5)
except KeyboardInterrupt:
    print("URL analysis stopped by user.")