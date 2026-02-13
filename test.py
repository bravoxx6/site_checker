import requests, time, logging, socket, asyncio
from urllib.parse import urlparse

async def check_port(host):
    COMMON_PORTS = [80, 20, 443, 21, 22, 3306]
    open_ports = []
    try:
        for port in COMMON_PORTS:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                if result == 0:
                    open_ports.append(port)
        return {
            "host": host,
            "open_ports": open_ports,
            "error": None
        }
    except socket.error as e:
        return {
            "host": host,
            "open_ports": None,
            "error": f"Socket error: {e}",
        }



async def check_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        start_time = time.time()
        r = requests.get(url, timeout=20, headers=headers)
        end_time = time.time()
        port_result = check_port(urlparse(url).hostname)
        return {
            "url": r.url,
            "response_time": round(end_time - start_time, 2), 
            "status": "UP" if r.ok else f'DOWN (HTTP {r.status_code})',
            "error": None,
            "port_info": port_result["open_ports"]
            }
    except requests.Timeout:
        return {
            "url": url, 
            "response_time": None, 
            "status": "DOWN", 
            "error": "The request timed out",
            "port_info": None
            }
    except requests.RequestException as e:
        return {
            "url": url, 
            "response_time": None, 
            "status": "DOWN", 
            "error": f"An error occurred: {e}",
            "port_info": None
            }



logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

async def analyse_urls(urls):
    for url in urls:
        result = await check_url(url)
        print(f"URL: {result['url']}, Response Time: {result['response_time']} seconds, Status: {result['status']}, Error: {result['error']}, Open Ports: {result['port_info']}")
        logging.info(f"URL: {result['url']} | Response Time: {result['response_time']} seconds | Status: {result['status']} | Open ports: {result['port_info']} | Error: {result['error']}")

try:
    while True:
        print("Starting URL analysis...")
        asyncio.run(analyse_urls(["https://www.facebook.com/", "https://www.youtube.com/", "https://dattebae.com/","https://www.wikipedia.org/", "https://play.google.com/store/apps/", "https://commons.wikimedia.org/wiki/Main_Page", "https://www.britannica.com/topic/wiki"]))
        time.sleep(5)
except KeyboardInterrupt:
    print("URL analysis stopped by user.")