from security.rbac_system import has_permission

def secure_action(user_role: str):
    if has_permission(user_role, "access_core"):
        return {"message": "Access granted"}
    else:
        return {"error": "Access denied"}
