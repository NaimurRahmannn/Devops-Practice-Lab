from flask import Blueprint, current_app, jsonify, request

api = Blueprint("api", __name__)


def get_employees():
    return current_app.config["EMPLOYEES"]


def get_next_id():
    employees = get_employees()

    if not employees:
        return 1

    return max(employee["id"] for employee in employees) + 1


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
    employees = get_employees()

    return jsonify(
        {
            "count": len(employees),
            "employees": employees,
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

    employee = {
        "id": get_next_id(),
        "name": name,
        "department": department,
        "salary": salary,
    }

    get_employees().append(employee)

    return jsonify(
        {
            "message": "Employee created successfully",
            "employee": employee,
        }
    ), 201


@api.get("/employees/<int:employee_id>")
def get_employee(employee_id):
    employees = get_employees()

    employee = next(
        (employee for employee in employees if employee["id"] == employee_id),
        None,
    )

    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify(employee), 200


@api.put("/employees/<int:employee_id>")
def update_employee(employee_id):
    employees = get_employees()

    employee = next(
        (employee for employee in employees if employee["id"] == employee_id),
        None,
    )

    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json(silent=True) or {}

    if "name" in data:
        if not data["name"]:
            return jsonify({"error": "Name cannot be empty"}), 400
        employee["name"] = data["name"]

    if "department" in data:
        if not data["department"]:
            return jsonify({"error": "Department cannot be empty"}), 400
        employee["department"] = data["department"]

    if "salary" in data:
        try:
            salary = float(data["salary"])
        except (TypeError, ValueError):
            return jsonify({"error": "Salary must be a number"}), 400

        if salary <= 0:
            return jsonify({"error": "Salary must be greater than 0"}), 400

        employee["salary"] = salary

    return jsonify(
        {
            "message": "Employee updated successfully",
            "employee": employee,
        }
    ), 200


@api.delete("/employees/<int:employee_id>")
def delete_employee(employee_id):
    employees = get_employees()

    employee = next(
        (employee for employee in employees if employee["id"] == employee_id),
        None,
    )

    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    employees.remove(employee)

    return jsonify(
        {
            "message": "Employee deleted successfully",
        }
    ), 200
