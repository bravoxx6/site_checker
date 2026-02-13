import requests, time, logging, socket, asyncio
from urllib.parse import urlparse
from ports import check_port
from checker import check_url
from logger import logging


def analyse_urls(urls):
    for url in urls:
        result = check_url(url)
        print(f"URL: {result['url']}, Response Time: {result['response_time']} seconds, Status: {result['status']}, Error: {result['error']}, Open Ports: {result['port_info']}")
        logging.info(f"URL: {result['url']} | Response Time: {result['response_time']} seconds | Status: {result['status']} | Open ports: {result['port_info']} | Error: {result['error']}")

try:
    while True:
        print("Starting URL analysis...")
        analyse_urls(["https://www.facebook.com/", "https://www.youtube.com/", "https://dattebae.com/","https://www.wikipedia.org/", "https://play.google.com/store/apps/", "https://commons.wikimedia.org/wiki/Main_Page", "https://www.britannica.com/topic/wiki"])
        time.sleep(5)
except KeyboardInterrupt:
    print("URL analysis stopped by user.")