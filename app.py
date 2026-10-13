
import os
from collections import Counter

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "attritioniq-demo-secret")

USERS = {
    "hr@attritioniq.com": {"password": "hr123", "role": "HR"},
    "manager@attritioniq.com": {"password": "manager123", "role": "Manager"},
}

# These are fictional UI records only, not IBM dataset records.
EMPLOYEES = [
    {
        "id": "EMP-1001",
        "name": "Aarav Sharma",
        "department": "Sales",
        "role": "Sales Executive",
        "income": 5200,
        "satisfaction": 3,
        "years": 4,
        "overtime": "Yes",
        "work_life_balance": 2,
        "distance_from_home": 19,
        "years_in_role": 2,
    },
    {
        "id": "EMP-1002",
        "name": "Ananya Reddy",
        "department": "Research & Development",
        "role": "Research Scientist",
        "income": 6800,
        "satisfaction": 4,
        "years": 7,
        "overtime": "No",
        "work_life_balance": 4,
        "distance_from_home": 12,
        "years_in_role": 3,
    },
    {
        "id": "EMP-1003",
        "name": "Rahul Verma",
        "department": "Human Resources",
        "role": "HR Specialist",
        "income": 4700,
        "satisfaction": 3,
        "years": 3,
        "overtime": "Yes",
        "work_life_balance": 3,
        "distance_from_home": 14,
        "years_in_role": 2,
    },
    {
        "id": "EMP-1004",
        "name": "Sneha Patel",
        "department": "Sales",
        "role": "Sales Representative",
        "income": 4300,
        "satisfaction": 2,
        "years": 2,
        "overtime": "Yes",
        "work_life_balance": 2,
        "distance_from_home": 21,
        "years_in_role": 1,
    },
    {
        "id": "EMP-1005",
        "name": "Vikram Rao",
        "department": "Research & Development",
        "role": "Laboratory Technician",
        "income": 3900,
        "satisfaction": 4,
        "years": 5,
        "overtime": "No",
        "work_life_balance": 4,
        "distance_from_home": 8,
        "years_in_role": 4,
    },
    {
        "id": "EMP-1006",
        "name": "Priya Nair",
        "department": "Information Technology",
        "role": "Software Engineer",
        "income": 7400,
        "satisfaction": 4,
        "years": 6,
        "overtime": "No",
        "work_life_balance": 3,
        "distance_from_home": 10,
        "years_in_role": 2,
    },
    {
        "id": "EMP-1007",
        "name": "Karan Mehta",
        "department": "Marketing",
        "role": "Marketing Analyst",
        "income": 5600,
        "satisfaction": 3,
        "years": 3,
        "overtime": "Yes",
        "work_life_balance": 3,
        "distance_from_home": 17,
        "years_in_role": 2,
    },
    {
        "id": "EMP-1008",
        "name": "Meera Joshi",
        "department": "Operations",
        "role": "Operations Manager",
        "income": 8200,
        "satisfaction": 4,
        "years": 8,
        "overtime": "No",
        "work_life_balance": 4,
        "distance_from_home": 15,
        "years_in_role": 4,
    },
    {
        "id": "EMP-1009",
        "name": "Dev Kapoor",
        "department": "Finance",
        "role": "Financial Analyst",
        "income": 6100,
        "satisfaction": 2,
        "years": 4,
        "overtime": "Yes",
        "work_life_balance": 2,
        "distance_from_home": 23,
        "years_in_role": 2,
    },
    {
        "id": "EMP-1010",
        "name": "Simran Khanna",
        "department": "Information Technology",
        "role": "Data Analyst",
        "income": 6900,
        "satisfaction": 4,
        "years": 6,
        "overtime": "No",
        "work_life_balance": 4,
        "distance_from_home": 9,
        "years_in_role": 3,
    },
]


def get_accessible_employees(role):
    if role == "Manager":
        # Team assignments are not in the demo data; this is only a scoped preview.
        return EMPLOYEES[:6]
    return EMPLOYEES


def filter_employees(employees, search_query, department_filter, role_filter):
    filtered = []
    query = (search_query or "").strip().lower()

    for employee in employees:
        matches_query = not query or query in employee["id"].lower() or query in employee["name"].lower()
        matches_department = department_filter == "all" or employee["department"] == department_filter
        matches_role = role_filter == "all" or employee["role"] == role_filter

        if matches_query and matches_department and matches_role:
            filtered.append(employee)

    return filtered


def summarize_employees(employees):
    department_counts = Counter(employee["department"] for employee in employees)
    overtime_counts = Counter(employee["overtime"] for employee in employees)
    max_department_count = max(department_counts.values(), default=0)
    employee_count = len(employees)

    return {
        "employee_count": employee_count,
        "department_count": len(department_counts),
        "average_income": round(sum(employee["income"] for employee in employees) / employee_count) if employee_count else 0,
        "average_satisfaction": round(sum(employee["satisfaction"] for employee in employees) / employee_count, 1) if employee_count else 0,
        "overtime_count": overtime_counts.get("Yes", 0),
        "overtime_percent": round(overtime_counts.get("Yes", 0) / employee_count * 100) if employee_count else 0,
        "departments": [
            {
                "name": department,
                "count": count,
                "percent": round(count / employee_count * 100) if employee_count else 0,
                "bar_width": round(count / max_department_count * 100) if max_department_count else 0,
            }
            for department, count in department_counts.most_common()
        ],
    }

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = USERS.get(email)

        if user and user["password"] == password:
            session["email"] = email
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))

        return render_template("login.html", error="Invalid email or password.")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect(url_for("login"))

    role = session["role"]

    accessible_employees = get_accessible_employees(role)
    stats = {
        "employees": len(accessible_employees),
    }
    scope_note = (
        "HR · Organization-wide sample view"
        if role == "HR"
        else "Manager · Restricted six-record demo scope; real team mapping is not configured."
    )

    return render_template(
        "dashboard.html",
        role=role,
        stats=stats,
        summary=summarize_employees(accessible_employees),
        employees=accessible_employees[:5],
        scope_note=scope_note,
        dashboard_heading="Organization-wide workforce overview" if role == "HR" else "Manager workspace overview",
        dashboard_subtitle=(
            "Explore workforce composition and prepare for evidence-based attrition analysis."
            if role == "HR"
            else "Review the employees available in this restricted manager demo view."
        ),
        dashboard_action="Review model readiness" if role == "HR" else "Review employee context",
    )


@app.route("/predictions")
def predictions():
    if "email" not in session:
        return redirect(url_for("login"))

    accessible_employees = get_accessible_employees(session["role"])
    employee_id = request.args.get("employee_id", "").strip()
    selected_employee = None
    selection_error = None

    if employee_id:
        selected_employee = next(
            (employee for employee in accessible_employees if employee["id"] == employee_id),
            None,
        )
        if selected_employee is None:
            selection_error = "That employee is not available in your current role scope."

    return render_template(
        "predictions.html",
        role=session["role"],
        employees=accessible_employees,
        selected_employee=selected_employee,
        selection_error=selection_error,
        scope_note="HR access: organization-wide predictions when available."
        if session["role"] == "HR"
        else "Manager access: team-scoped predictions when available; team assignments are not configured in this demo.",
    ), 404 if selection_error else 200


@app.route("/analytics")
def analytics():
    if "email" not in session:
        return redirect(url_for("login"))

    role = session["role"]
    accessible_employees = get_accessible_employees(role)
    return render_template(
        "analytics.html",
        role=role,
        summary=summarize_employees(accessible_employees),
        scope_note="Organization-wide sample view"
        if role == "HR"
        else "Manager preview: six sample records; team assignments are not configured.",
    )
@app.route("/employees")
def employees():
    if "email" not in session:
        return redirect(url_for("login"))

    role = session["role"]
    accessible_employees = get_accessible_employees(role)
    search_query = request.args.get("q", "")
    department_filter = request.args.get("department", "all")
    role_filter = request.args.get("role", "all")

    filtered_employees = filter_employees(
        accessible_employees,
        search_query,
        department_filter,
        role_filter,
    )

    department_options = sorted({employee["department"] for employee in accessible_employees})
    role_options = sorted({employee["role"] for employee in accessible_employees})

    return render_template(
        "employees.html",
        role=role,
        employees=filtered_employees,
        departments=department_options,
        job_roles=role_options,
        current_department=department_filter,
        current_role=role_filter,
        search_query=search_query,
        total_count=len(filtered_employees),
        access_note="Organization-wide sample records." if role == "HR" else "Manager demo scope: six sample records only. Team assignments are not configured.",
    )


@app.route("/employees/<employee_id>")
def employee_profile(employee_id):
    if "email" not in session:
        return redirect(url_for("login"))

    role = session["role"]
    accessible_employees = get_accessible_employees(role)
    employee = next((item for item in accessible_employees if item["id"] == employee_id), None)

    if employee is None:
        return render_template("employee_profile.html", role=role, employee=None, access_note="Employee not available in your current scope."), 404

    return render_template(
        "employee_profile.html",
        role=role,
        employee=employee,
        access_note="Demo profile view only — real dataset integration is coming next." if role == "Manager" else "Sample employee record for UI development.",
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
