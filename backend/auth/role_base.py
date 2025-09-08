# role_base.py

from functools import wraps
from flask import request, jsonify

# Define role permissions
ROLE_PERMISSIONS = {
    "technician": {
        "install_frontend": True,
        "add_modules": True,
        "access_backend": False,
        "create_users": False,
        "modify_modules": False,
        "request_core_change": False,
    },
    "department_officer": {
        "install_frontend": True,
        "access_backend": True,
        "create_technicians": True,
        "modify_modules": False,
        "request_core_change": True,
    },
    "admin": {
        "full_access": True,
    }
}

# Dummy user-role mapping for simulation (should be from DB/token)
USER_ROLE_MAP = {
    "tech123": "technician",
    "officer456": "department_officer",
    "admin789": "admin"
}


def get_user_role(api_key):
    """Simulate getting user role by API key (replace with DB/token logic)."""
    return USER_ROLE_MAP.get(api_key)


def check_permission(required_permission):
    """Decorator to check permission before accessing a route."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            api_key = request.headers.get("X-API-KEY")

            if not api_key:
                return jsonify({"error": "Missing API Key"}), 401

            role = get_user_role(api_key)
            if not role:
                return jsonify({"error": "Invalid API Key"}), 403

            if role == "admin":
                return f(*args, **kwargs)

            permissions = ROLE_PERMISSIONS.get(role, {})
            if permissions.get(required_permission) or permissions.get("full_access"):
                return f(*args, **kwargs)

            return jsonify({"error": f"Permission denied for {role}"}), 403
        return wrapper
    return decorator

