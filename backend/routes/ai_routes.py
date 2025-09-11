from flask import Blueprint, jsonify, request
from backend.auth.firebase_auth import verify_user_token
from backend.ai.analytics import AnalyticsEngine

ai_bp = Blueprint('ai_bp', __name__)

@ai_bp.route('/api/ai/sales-trends', methods=['GET'])
def get_sales_trends_route():
    """
    API endpoint to get sales trend analysis from the AnalyticsEngine.
    Requires a valid, approved user.
    """
    # 1. Verify the user is authenticated and approved
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization token is missing or invalid'}), 401

    id_token = auth_header.split('Bearer ')[1]
    user = verify_user_token(id_token)

    if not user:
        return jsonify({'error': 'Invalid token'}), 403

    # Check for custom claims
    if user.get('status') != 'approved':
        return jsonify({'error': 'Account not approved'}), 403

    # 2. Proceed with the original logic
    try:
        engine = AnalyticsEngine()
        insight = engine.get_sales_trends()
        return jsonify({'status': 'success', 'insight': insight}), 200
    except Exception as e:
        # In a real app, we would log this error
        print(f"Error in AI analytics route: {e}")
        return jsonify({'status': 'error', 'message': 'Could not process AI analytics request.'}), 500
