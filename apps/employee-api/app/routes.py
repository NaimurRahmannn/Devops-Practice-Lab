from flask import Blueprint, current_app, jsonify, request

from app.extensions import db
from app.models import Employee

api = Blueprint("api", __name__)


@api.get("/")
def home():
    return jsonify(
        {
            "message": "Employee API is running",
            "app": current_app.config["APP_NAME"],
            "version": current_app.config["VERSION"],
        }
    ), 200


@api.get("/health")
def health_check():
    return jsonify(
        {
            "status": "healthy",
            "service": "employee-api",
        }
    ), 200


@api.get("/employees")
def list_employees():
    employees = Employee.query.order_by(Employee.id).all()

    return jsonify(
        {
            "count": len(employees),
            "employees": [employee.to_dict() for employee in employees],
        }
    ), 200


@api.post("/employees")
def create_employee():
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    department = data.get("department")
    salary = data.get("salary")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    if not department:
        return jsonify({"error": "Department is required"}), 400

    if salary is None:
        return jsonify({"error": "Salary is required"}), 400

    try:
        salary = float(salary)
    except (TypeError, ValueError):
        return jsonify({"error": "Salary must be a number"}), 400

    if salary <= 0:
        return jsonify({"error": "Salary must be greater than 0"}), 400

    employee = Employee(name=name, department=department, salary=salary)

    db.session.add(employee)
    db.session.commit()

    return jsonify(
        {
            "message": "Employee created successfully",
            "employee": employee.to_dict(),
        }
    ), 201


@api.get("/employees/<int:employee_id>")
def get_employee(employee_id):
    employee = db.session.get(Employee, employee_id)

    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify(employee.to_dict()), 200


@api.put("/employees/<int:employee_id>")
def update_employee(employee_id):
    employee = db.session.get(Employee, employee_id)

    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json(silent=True) or {}

    if "name" in data:
        if not data["name"]:
            return jsonify({"error": "Name cannot be empty"}), 400
        employee.name = data["name"]

    if "department" in data:
        if not data["department"]:
            return jsonify({"error": "Department cannot be empty"}), 400
        employee.department = data["department"]

    if "salary" in data:
        try:
            salary = float(data["salary"])
        except (TypeError, ValueError):
            return jsonify({"error": "Salary must be a number"}), 400

        if salary <= 0:
            return jsonify({"error": "Salary must be greater than 0"}), 400

        employee.salary = salary

    db.session.commit()

    return jsonify(
        {
            "message": "Employee updated successfully",
            "employee": employee.to_dict(),
        }
    ), 200


@api.delete("/employees/<int:employee_id>")
def delete_employee(employee_id):
    employee = db.session.get(Employee, employee_id)

    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    db.session.delete(employee)
    db.session.commit()

    return jsonify(
        {
            "message": "Employee deleted successfully",
        }
    ), 200
