# Site Checker - Website Monitoring & Alerting System

A real-time website monitoring tool that tracks website availability, response times, and open ports. Includes a web dashboard for visualization and Telegram notifications for alerts.

## Features

- **Real-time URL Monitoring** — Continuously checks website availability and response times
- **Port Scanning** — Monitors open ports (80, 443, 22, 21, 3306) on target hosts
- **Web Dashboard** — FastAPI-based web interface to view monitoring data and control monitoring status
- **Telegram Alerts** — Sends instant notifications when websites go down
- **SQLite Database** — Stores all monitoring results for historical analysis
- **Multi-threaded Processing** — Efficiently handles concurrent URL checks
- **Configurable** — Easy to modify URLs, ports, and check intervals

## Prerequisites

- Docker & Docker Compose
- Python 3.10+ (if running locally without Docker)
- Telegram Bot Token (for notifications)

## Quick Start with Docker

### 1. Clone and Setup

```bash
git clone https://github.com/bravoxx6/site_checker.git
cd first_project
```

### 2. Create .env File

Create a `.env` file in the root directory with your Telegram credentials:

```env
TG_TOKEN=your_telegram_bot_token
TG_CHAT_ID=your_telegram_chat_id
TZ=Europe/Moscow
```

Replace values:
- `TG_TOKEN` — Get from [@BotFather](https://t.me/botfather) on Telegram
- `TG_CHAT_ID` — Your Telegram chat ID (can get from [@userinfobot](https://t.me/userinfobot))
- `TZ` — Your timezone (e.g., `Europe/Moscow`, `America/New_York`, `UTC`)

### 3. Configure Monitoring

Edit `config.json` to specify URLs and ports to monitor:

```json
{
  "interval": 5,
  "http_timeout": 20,
  "log_file": "logs.txt",
  "ports": [80, 443, 22, 21, 3306],
  "urls": [
    "https://www.facebook.com/",
    "https://www.youtube.com/",
    "https://example.com/"
  ]
}
```

- `interval` — Check interval in seconds
- `http_timeout` — HTTP request timeout
- `ports` — Ports to scan for each host
- `urls` — List of URLs to monitor

### 4. Start the Services

```bash
docker compose up -d
```

This starts two services:
- **monitor** — Background monitoring service
- **dashboard** — Web interface (http://127.0.0.1:8000)

### 5. Access the Dashboard

Open your browser and go to:

```
http://127.0.0.1:8000/dashboard
```

## API Endpoints

### GET `/dashboard`
Returns the web dashboard HTML interface.

### GET `/api/data`
Returns the latest monitoring results for all URLs.

**Response:**
```json
[
  {
    "id": 1,
    "url": "https://www.facebook.com/",
    "response_time": 0.45,
    "status": "UP",
    "error": null,
    "port_info": "[80, 443]",
    "status_level": "INFO",
    "timestamp": "2024-02-19 10:30:45"
  }
]
```

### GET `/api/status`
Returns the same data as `/api/data` in a wrapped format.

### POST `/api/toggle`
Toggles monitoring on/off.

**Response:**
```json
{
  "is_active": true
}
```

## Project Structure

```
first_project/
├── app/
│   ├── main.py           # Main monitoring loop
│   ├── dashboard.py      # FastAPI web interface
│   ├── checker.py        # URL checking logic
│   ├── logger.py         # Logging to file and database
│   ├── notifier.py       # Telegram notification sender
│   ├── database.py       # Database initialization
│   └── ports.py          # Port scanning logic
├── templates/
│   └── index.html        # Dashboard UI
├── config.json           # Monitoring configuration
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Container image definition
└── .env                  # Environment variables (create this)
```

## Configuration Details

### How Monitoring Works

1. **Checker** (`checker.py`) — Sends HTTP requests to each URL and checks ports
2. **Logger** (`logger.py`) — Stores results in SQLite database and logs to file
3. **Notifier** (`notifier.py`) — Sends Telegram alerts when a site is DOWN for 3 consecutive checks
4. **Dashboard** (`dashboard.py`) — Provides web interface to view results and control monitoring

### Status Levels

- **INFO** — Website is UP with HTTP 200 status
- **WARNING** — Website returned HTTP 4xx error
- **ERROR** — Website is DOWN or unreachable

### Database Schema

**monitoring_results table:**
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| url | TEXT | Monitored URL |
| response_time | REAL | Response time in seconds |
| status | VARCHAR | UP, DOWN, or HTTP status code |
| error | VARCHAR | Error message if any |
| port_info | VARCHAR | JSON array of open ports |
| status_level | VARCHAR | INFO, WARNING, or ERROR |
| timestamp | DATETIME | Check timestamp |

**settings table:**
| Column | Type | Description |
|--------|------|-------------|
| key | TEXT | Setting key (e.g., 'monitoring_active') |
| value | TEXT | Setting value (e.g., 'True' or 'False') |

## Running Locally (Without Docker)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Database

```bash
python -c "from app.database import create_database, create_settings_table; create_database(); create_settings_table()"
```

### 3. Run Monitoring Service

```bash
python app/main.py
```

### 4. Run Dashboard (in another terminal)

```bash
uvicorn app.dashboard:app --host 0.0.0.0 --port 8000
```

## Common Issues

### Database Corruption Error
If you see `sqlite3.DatabaseError: database disk image is malformed`:

1. Stop containers: `docker compose down`
2. Remove corrupted database: `docker volume rm first_project_db_data`
3. Restart: `docker compose up -d`

### No Telegram Notifications
- Verify `TG_TOKEN` and `TG_CHAT_ID` are correct in `.env`
- Check bot token hasn't expired
- Ensure bot has permission to send messages to the chat

### Timezone Mismatch
The `TZ` environment variable must match your local timezone:

```bash
docker compose down
# Update TZ in .env
docker compose up -d
```

### Monitoring Stopped
Access dashboard at `http://127.0.0.1:8000/dashboard` and click the toggle button to activate monitoring.

## Logs

- **Application logs** — `monitoring.log` (JSON format)
- **Full logs** — `logs.txt`
- **Docker logs** — `docker logs site_checker` or `docker logs site_checker_dashboard`

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| TG_TOKEN | Yes | Telegram Bot API token |
| TG_CHAT_ID | Yes | Telegram chat ID for alerts |
| TZ | No | Timezone (default: UTC) |

## Dependencies

- **requests** — HTTP requests
- **fastapi** — Web framework
- **uvicorn** — ASGI server
- **python-dotenv** — Environment variable loading
- **jinja2** — HTML templating
- **python-telegram-bot** — Telegram API

## Performance

- Monitors up to 7 URLs simultaneously with 5 worker threads
- Database uses WAL mode for concurrent access
- Check interval: 10 seconds (configurable)
- Average response time: < 1 second per URL

## Troubleshooting

### Container won't start
```bash
docker compose logs site_checker
docker compose logs site_checker_dashboard
```

### High memory usage
Check for database locks:
```bash
docker exec site_checker sqlite3 monitoring.db ".tables"
```

## 🎓 Learning Objectives

This project was built to master:

* **DevOps:** Implementing Control Plane/Data Plane separation.
* **Backend:** Building REST APIs with FastAPI.
* **Database:** Managing concurrency with SQLite WAL mode.
* **Frontend:** Asynchronous DOM updates with Vanilla JavaScript.