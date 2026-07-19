import pytest

from app import create_app
from app.extensions import db


@pytest.fixture
def client():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Employee API is running"


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_list_employees_initially_empty(client):
    response = client.get("/employees")
    data = response.get_json()

    assert response.status_code == 200
    assert data["count"] == 0
    assert data["employees"] == []


def test_create_employee(client):
    response = client.post(
        "/employees",
        json={
            "name": "Naimur",
            "department": "Engineering",
            "salary": 30000,
        },
    )

    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "Employee created successfully"
    assert data["employee"]["name"] == "Naimur"
    assert data["employee"]["department"] == "Engineering"
    assert data["employee"]["salary"] == 30000


def test_list_employees_after_create(client):
    client.post(
        "/employees",
        json={
            "name": "Rahim",
            "department": "QA",
            "salary": 25000,
        },
    )

    response = client.get("/employees")
    data = response.get_json()

    assert response.status_code == 200
    assert data["count"] == 1
    assert data["employees"][0]["department"] == "QA"


def test_create_employee_without_name(client):
    response = client.post(
        "/employees",
        json={
            "department": "Engineering",
            "salary": 30000,
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Name is required"


def test_create_employee_with_invalid_salary(client):
    response = client.post(
        "/employees",
        json={
            "name": "Naimur",
            "department": "Engineering",
            "salary": "abc",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Salary must be a number"


def test_get_employee(client):
    create_response = client.post(
        "/employees",
        json={
            "name": "Karim",
            "department": "Support",
            "salary": 20000,
        },
    )

    employee_id = create_response.get_json()["employee"]["id"]

    response = client.get(f"/employees/{employee_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["name"] == "Karim"


def test_get_employee_not_found(client):
    response = client.get("/employees/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Employee not found"


def test_update_employee(client):
    create_response = client.post(
        "/employees",
        json={
            "name": "Sakib",
            "department": "HR",
            "salary": 22000,
        },
    )

    employee_id = create_response.get_json()["employee"]["id"]

    response = client.put(
        f"/employees/{employee_id}",
        json={
            "department": "DevOps",
            "salary": 40000,
        },
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["employee"]["department"] == "DevOps"
    assert data["employee"]["salary"] == 40000


def test_delete_employee(client):
    create_response = client.post(
        "/employees",
        json={
            "name": "Sakib",
            "department": "HR",
            "salary": 22000,
        },
    )

    employee_id = create_response.get_json()["employee"]["id"]

    delete_response = client.delete(f"/employees/{employee_id}")

    assert delete_response.status_code == 200
    assert delete_response.get_json()["message"] == "Employee deleted successfully"

    get_response = client.get(f"/employees/{employee_id}")
    assert get_response.status_code == 404
