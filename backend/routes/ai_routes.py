from flask import Blueprint, jsonify
from ..ai.analytics import AnalyticsEngine

ai_bp = Blueprint('ai_bp', __name__)

@ai_bp.route('/api/ai/sales-trends', methods=['GET'])
def get_sales_trends_route():
    """
    API endpoint to get sales trend analysis from the AnalyticsEngine.
    """
    try:
        engine = AnalyticsEngine()
        insight = engine.get_sales_trends()
        return jsonify({'status': 'success', 'insight': insight}), 200
    except Exception as e:
        # In a real app, we would log this error
        print(f"Error in AI analytics route: {e}")
        return jsonify({'status': 'error', 'message': 'Could not process AI analytics request.'}), 500
