import logging
import json
from datetime import datetime

logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format='%(message)s',
)

def log_result(result: dict):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "url": result.get("url"),
        "response_time": result.get("response_time"),
        "status": result.get("status"),
        "error": result.get("error"),
        "port_info": result.get("port_info")
    }
    logging.info(json.dumps(log_entry, ensure_ascii=False))

