from flask import Blueprint
from auth.role_base import check_permission

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/setup_frontend', methods=['POST'])
@check_permission("install_frontend")
def setup_frontend():
    return {"status": "Frontend setup complete"}

@admin_routes.route('/admin_only', methods=['POST'])
@check_permission('full_access')
def admin_function():
    return {"status": "Admin access granted."}
                    
