# 📦 Shipment Tracking API

A full-stack shipment tracking application built with **FastAPI**, **PostgreSQL** (or SQLite for local dev), and **React**. Features JWT-based authentication and a clean dashboard UI for managing shipments end-to-end.

---

## 🗂️ Project Structure

```
shipment-tracking-api/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # SQLAlchemy engine & session
│   ├── auth/
│   │   └── jwt.py           # JWT creation, hashing, auth dependency
│   ├── models/
│   │   ├── user.py          # User ORM model
│   │   └── shipment.py      # Shipment ORM model + status enum
│   ├── routers/
│   │   ├── auth.py          # /auth/register, /auth/login
│   │   └── shipment.py      # CRUD + status transition endpoints
│   └── schemas/
│       ├── auth.py          # Pydantic schemas for auth
│       └── shipment.py      # Pydantic schemas for shipments
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # React dashboard
│   │   ├── main.jsx
│   │   └── styles.css
│   └── index.html
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## ⚙️ Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | Python 3.11, FastAPI, Uvicorn     |
| ORM       | SQLAlchemy 2.x (mapped columns)   |
| Auth      | JWT (python-jose), bcrypt/passlib |
| Database  | PostgreSQL 16 (Docker) / SQLite   |
| Frontend  | React 18, Vite                    |
| Container | Docker, Docker Compose            |

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- Or: Python 3.11+ and Node.js 20+ for running locally

---

### Option 1 — Docker Compose (Recommended)

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd shipment-tracking-api

# 2. Configure environment
cp .env.example .env
# Edit .env and set a strong SECRET_KEY

# 3. Start all services (backend + PostgreSQL + frontend)
docker compose up --build
```

Services will be available at:
- **API** → http://localhost:8000
- **Frontend** → http://localhost:5173
- **PostgreSQL** → localhost:5432

---

### Option 2 — Local Development

**Backend:**

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env            # Uses SQLite by default

# Run the API server
uvicorn app.main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
cp .env.example .env            # Sets VITE_API_URL=http://localhost:8000
npm install
npm run dev
```

---

## 🔧 Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable                    | Default                    | Description                          |
|-----------------------------|----------------------------|--------------------------------------|
| `DATABASE_URL`              | `sqlite:///./shipment.db`  | Database connection string           |
| `SECRET_KEY`                | `change-me`                | JWT signing secret — **change this** |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60`                     | JWT token lifetime in minutes        |

**Frontend** (`frontend/.env`):

| Variable       | Default                   | Description        |
|----------------|---------------------------|--------------------|
| `VITE_API_URL` | `http://localhost:8000`   | Backend API URL    |

---

## 📡 API Reference

All shipment endpoints require a `Bearer` token in the `Authorization` header.

### Authentication

| Method | Endpoint         | Description              | Auth Required |
|--------|-----------------|--------------------------|---------------|
| POST   | `/auth/register` | Register a new user      | No            |
| POST   | `/auth/login`    | Login and receive a JWT  | No            |

**Register / Login body:**
```json
{
  "username": "yourname",
  "password": "yourpassword"
}
```

**Login response:**
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

---

### Shipments

| Method | Endpoint                      | Description                   |
|--------|-------------------------------|-------------------------------|
| GET    | `/shipments`                  | List shipments (with filters) |
| GET    | `/shipments/{id}`             | Get a single shipment         |
| POST   | `/shipments`                  | Create a new shipment         |
| PUT    | `/shipments/{id}`             | Update shipment details       |
| PATCH  | `/shipments/{id}/status`      | Update shipment status        |
| DELETE | `/shipments/{id}`             | Delete a shipment             |

**Query filters for `GET /shipments`:**

| Parameter    | Type     | Description                          |
|--------------|----------|--------------------------------------|
| `status`     | string   | Filter by status (`Pending`, `In Transit`, `Delivered`) |
| `destination`| string   | Partial match on destination         |
| `start_date` | datetime | Filter shipments created after date  |
| `end_date`   | datetime | Filter shipments created before date |

**Create shipment body:**
```json
{
  "tracking_number": "TRK-001",
  "origin": "Istanbul",
  "destination": "Ankara",
  "expected_delivery": "2026-05-15T12:00:00",
  "status": "Pending"
}
```

---

### Shipment Status

Status transitions follow a strict one-way flow:

```
Pending → In Transit → Delivered
```

Attempting an invalid transition (e.g. `Delivered → Pending`) returns `HTTP 400`.

---

## 🖥️ Frontend Dashboard

The React frontend provides a simple but fully functional dashboard:

- **Auth panel** — Register, login, and logout
- **Create Shipment** — Form with tracking number, origin, destination, expected delivery, and initial status
- **Filters** — Filter the shipment list by status, destination, and date range
- **Shipments table** — View all shipments and update status inline via dropdown

---

## 🔐 Security Notes

- Passwords are hashed with **bcrypt** via passlib.
- JWTs are signed with **HS256** using the `SECRET_KEY` environment variable.
- **Always replace the default `SECRET_KEY`** before deploying to production.
- CORS is configured for `localhost:5173` and `localhost:5174` by default — update `app/main.py` for production origins.

---

## 📄 Interactive API Docs

FastAPI auto-generates interactive documentation:

- **Swagger UI** → http://localhost:8000/docs
- **ReDoc** → http://localhost:8000/redoc

---

## 🩺 Health Check

```
GET /
```

Returns `{"status": "ok"}` — useful for container health checks.
