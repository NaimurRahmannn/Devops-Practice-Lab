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
