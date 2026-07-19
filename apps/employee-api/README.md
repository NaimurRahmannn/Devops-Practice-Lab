# Employee API

This is a simple Flask Employee Management API for local backend practice.

## Features

- Home route
- Health check route
- Create employee
- List employees
- Get employee by ID
- Update employee
- Delete employee
- Pytest test cases

## Project Structure

```text
employee-api/
├── app/
│   ├── __init__.py
│   └── routes.py
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## Run the Project

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start PostgreSQL with Docker Compose:

```bash
docker compose -f ../../docker/docker-compose.yml up -d postgres
```

Run the app:

```bash
python run.py
```

Open this URL in browser:

```text
http://127.0.0.1:5000
```

Health check:

```text
http://127.0.0.1:5000/health
```

## Run Tests

```bash
pytest
```

Tests use an in-memory SQLite database so they can run without PostgreSQL.

## PostgreSQL Configuration

By default, the app connects to:

```text
postgresql+psycopg2://employee_user:employee_password@localhost:5432/employee_db
```

Override it with the `DATABASE_URL` environment variable when needed.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Home route |
| GET | `/health` | Health check |
| GET | `/employees` | List employees |
| POST | `/employees` | Create employee |
| GET | `/employees/<id>` | Get single employee |
| PUT | `/employees/<id>` | Update employee |
| DELETE | `/employees/<id>` | Delete employee |

## Example Create Employee Request

```bash
curl -X POST http://127.0.0.1:5000/employees \
  -H "Content-Type: application/json" \
  -d '{"name": "Naimur", "department": "Engineering", "salary": 30000}'
```
