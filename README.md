# Site Checker 🔍

A simple Python monitoring tool that checks website availability, response time, open ports, and sends Telegram notifications when a site goes down.

---

## Features

- Website availability monitoring
- Response time measurement
- Port scanning
- Logging to file
- Concurrent checks using threads
- Telegram alerts when a site is DOWN

---

## Project Structure

site_checker/
│
├── main.py # Main monitoring loop
├── checker.py # URL availability checker
├── ports.py # Port scanner
├── logger.py # Logging module
├── notifier.py # Telegram notifications
├── config.json # Configuration file
├── logs.txt # Log output
└── README.md


---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/bravoxx6/site_checker.git
cd site_checker
```
### 1. Clone the repository
```
pip install requests python-dotenv
```
3. Create .env file

Create a file named .env in the project root:
```
TG_TOKEN=your_telegram_bot_token
TG_CHAT_ID=your_chat_id
```
4. Configure sites

Edit config.json

Usage

Run the monitor:
```
python main.py
```
The program will:

1. Check each site
2. Log results to logs.txt
3. Send Telegram alert if a site fails 3 times in a row

How Alerts Work
A Telegram notification is sent ONLY when:

A site returns DOWN status
It fails 3 consecutive checks
This prevents false alarms.

Logs
Logs are saved in: logs.txt


Built for practice in:

Python
Networking
Monitoring systems
Logging architecture
Alerting systems
