# Smart Task Management System

**Smart Task Management System** is a beginner-friendly but production-quality Flask project featuring authentication, REST APIs, analytics with Pandas/NumPy, real-time updates via Socket.IO, and a responsive HTML/CSS dashboard.

## Features
- User registration, login, logout with session-based authentication
- Task CRUD REST APIs (create, read, update, delete)
- PostgreSQL integration using SQLAlchemy ORM
- Analytics endpoint using Pandas and NumPy
- WebSocket live task updates (`task_updated`)
- Responsive frontend with dashboard, analytics cards, and task table

## Tech Stack
- Python, Flask, Flask-SQLAlchemy, Flask-Migrate
- PostgreSQL, psycopg2-binary
- Pandas, NumPy
- Flask-SocketIO (WebSockets)
- HTML, CSS, JavaScript

## Project Structure
```
project_root/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── task.py
│   │   ├── analytics.py
│   │   └── websocket.py
│   ├── templates/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── dashboard.html
│   ├── static/
│   │   ├── style.css
│   │   └── app.js
│   └── utils/
│       └── analytics_utils.py
├── config.py
├── run.py
├── requirements.txt
├── README.md
├── .env
└── schema.sql
```

## Exact Terminal Commands (Setup)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Create or update .env with your local settings
flask db init
flask db migrate -m "init"
flask db upgrade
python run.py
```

## PostgreSQL Setup Commands
```sql
-- Open psql shell first
CREATE DATABASE task_management_db;
CREATE USER task_user WITH PASSWORD 'task_password';
GRANT ALL PRIVILEGES ON DATABASE task_management_db TO task_user;
```

## Environment Variables
Create a `.env` file with:
```
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=change-me
DATABASE_URL=postgresql://task_user:task_password@localhost:5432/task_management_db
```

## Database Migrations
```bash
flask db init
flask db migrate -m "init"
flask db upgrade
```

## Running the App
```bash
python run.py
```
Open `http://localhost:5000` in your browser.

## API Documentation
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register user |
| POST | `/auth/login` | Login user |
| POST | `/auth/logout` | Logout user |
| GET | `/api/tasks` | Get all tasks |
| POST | `/api/tasks` | Add new task |
| GET | `/api/tasks/<id>` | Get single task |
| PUT | `/api/tasks/<id>` | Update task |
| DELETE | `/api/tasks/<id>` | Delete task |
| GET | `/analytics` | Task analytics |

## API Testing Examples (cURL)
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"pass123"}'

curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"pass123"}'

curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Finish assignment","description":"Create Flask app","priority":"high","status":"pending"}'

curl http://localhost:5000/api/tasks

curl http://localhost:5000/analytics
```

## WebSocket (Socket.IO)
- Event name: `task_updated`
- Triggered whenever a task is created, updated, or deleted.
- Frontend listens to this event and refreshes tasks + analytics automatically.

## Screenshots (Placeholders)
- `docs/screenshots/login.png`
- `docs/screenshots/register.png`
- `docs/screenshots/dashboard.png`

## Demo Video Script (Quick Walkthrough)
1. Introduce the project and mention the tech stack.
2. Show the registration page and create a new user.
3. Log in and open the dashboard.
4. Add a new task and show it appear in the table.
5. Update the task status to completed and show analytics changes.
6. Delete a task and mention real-time updates via Socket.IO.
7. End with project structure and code highlights.
