from flask import Blueprint, jsonify

# Admin-related routes
admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    """
    An example admin route.
    """
    return jsonify({'message': 'Welcome to the admin dashboard!'})
