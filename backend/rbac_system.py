
# roles: admin, dept_officer, technician
users_db = {
    "admin_user": {"role": "admin", "password": "admin123"},
    "tech_user": {"role": "technician", "password": "tech123"},
    "dept_user": {"role": "dept_officer", "password": "dept123"},
}

role_permissions = {
    "admin": ["install_frontend", "setup_modules", "access_backend", "modify_core", "create_users"],
    "dept_officer": ["install_frontend", "setup_modules", "access_backend"],
    "technician": ["install_frontend", "setup_modules"],
}

core_access_required = ["modify_core"]

def login(username, password):
    user = users_db.get(username)
    if user and user["password"] == password:
        print(f"Welcome {username}, Role: {user['role']}")
        return user
    else:
        print("Invalid login.")
        return None

def has_permission(user, action):
    return action in role_permissions.get(user["role"], [])

def perform_action(user, action):
    if has_permission(user, action):
        print(f"{user['role']} is performing: {action}")
    else:
        print(f"{user['role']} is not allowed to perform: {action}")

# Example Usage
if __name__ == "__main__":
    current_user = login("dept_user", "dept123")
    if current_user:
        perform_action(current_user, "access_backend")
        perform_action(current_user, "modify_core")  # Requires admin authorization
