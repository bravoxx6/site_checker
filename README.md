# 🔍 Site Sentinel: Advanced Monitoring System

A robust Python-based monitoring solution that tracks website availability, response times, and open ports. It features a real-time web dashboard and sends instant Telegram alerts if a service fails.

---

## ✨ Features

* **Dynamic Web Dashboard:** View real-time status without page reloads (AJAX/Fetch).
* **Multi-threaded Worker:** Concurrent website checks for high performance.
* **SQLite with WAL Mode:** Efficient database handling for simultaneous read/write operations.
* **Control Panel:** Activate or deactivate monitoring directly from the dashboard.
* **Triple-Check Logic:** Alerts are sent only after 3 consecutive failures to prevent false alarms.
* **Port Scanning:** Checks critical infrastructure ports (80, 443, 22, etc.).
* **Telegram Integration:** Instant notifications for downtime events.

---

## 📂 Project Structure

```text
site_checker/
│
├── main.py          # Background monitoring worker
├── dashboard.py     # FastAPI server & API endpoints
├── checker.py       # URL availability logic
├── ports.py         # Socket-based port scanner
├── database.py      # SQLite schema and initialization
├── logger.py        # Database and file logging module
├── notifier.py      # Telegram notification service
├── templates/       # Frontend HTML files
├── config.json      # Target URLs and ports configuration
└── monitoring.db    # SQLite database (auto-generated)

```

---

## 🛠 Installation

### 1. Clone the repository

```bash
git clone https://github.com/bravoxx6/site_checker.git
cd site_checker

```

### 2. Install dependencies

```bash
pip install requests python-dotenv fastapi uvicorn jinja2

```

### 3. Setup Environment

Create a `.env` file in the root directory:

```env
TG_TOKEN=your_telegram_bot_token
TG_CHAT_ID=your_chat_id

```

### 4. Configure targets

Edit `config.json` to include the URLs and ports you want to monitor.

---

## 🚀 Usage

### 1. Initialize the system

First, set up the database tables:

```bash
python database.py

```

### 2. Start the Monitor (Worker)

Run the background checker in the first terminal:

```bash
python main.py

```

### 3. Launch the Dashboard

Run the web server in a second terminal:

```bash
uvicorn dashboard:app --reload

```

Open your browser at `http://127.0.0.1:8000/dashboard`.

---

## ⚙️ How it works

1. **State Management:** The Dashboard writes the "Active/Inactive" status to a `settings` table in SQLite.
2. **The Worker:** `main.py` polls this status every 10 seconds. If active, it spawns threads to check your sites.
3. **Observability:** Results are logged into `monitoring.db`. The dashboard's JavaScript fetches the latest results every 5 seconds via a REST API.

---

## 🎓 Learning Objectives

This project was built to master:

* **DevOps:** Implementing Control Plane/Data Plane separation.
* **Backend:** Building REST APIs with FastAPI.
* **Database:** Managing concurrency with SQLite WAL mode.
* **Frontend:** Asynchronous DOM updates with Vanilla JavaScript.
