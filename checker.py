import requests, time
from urllib.parse import urlparse
from ports import check_port

def check_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        start_time = time.time()
        r = requests.get(url, timeout=20, headers=headers)
        end_time = time.time()
        port_result = check_port(urlparse(url).hostname)
        status_level = "INFO" if r.status_code == 200 else "WARNING" if 400 <= r.status_code < 500 else "ERROR"
        return {
            "url": r.url,
            "response_time": round(end_time - start_time, 2), 
            "status": "UP" if r.ok else f'(HTTP {r.status_code})',
            "error": None,
            "port_info": port_result["open_ports"],
            "status_level": status_level
            }
    except requests.Timeout:
        return {
            "url": url, 
            "response_time": None, 
            "status": "DOWN", 
            "error": "The request timed out",
            "port_info": None,
            "status_level": "ERROR"
            }
    except requests.RequestException as e:
        return {
            "url": url, 
            "response_time": None, 
            "status": "DOWN", 
            "error": str(e),
            "port_info": None,
            "status_level": "ERROR"
            }