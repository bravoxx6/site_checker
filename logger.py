import logging
import json

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
        log_file = config.get("log_file", "")
except FileNotFoundError:
    print("Configuration file 'config.json' not found. Please create it with the necessary log file name.")
    log_file = "logs.txt"

logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')