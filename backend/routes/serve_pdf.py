from flask import Blueprint, send_from_directory, abort, request, jsonify
from backend.auth.firebase_auth import verify_user_token
import os

serve_pdf_bp = Blueprint("serve_pdf", __name__)

PDF_STORAGE_DIR = os.path.abspath("pdf_storage")  # Adjust as needed

@serve_pdf_bp.route("/api/pdf/<filename>", methods=["GET"])
def serve_pdf(filename):
    # 1. Verify the user is authenticated and approved via Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        # Using jsonify for a consistent error response format
        return jsonify({'error': 'Authorization token is missing or invalid'}), 401

    id_token = auth_header.split('Bearer ')[1]
    user = verify_user_token(id_token)

    if not user:
        return jsonify({'error': 'Invalid token'}), 403

    # Check for custom claims
    if user.get('status') != 'approved':
        return jsonify({'error': 'Account not approved'}), 403
    
    # 2. Proceed with serving the file
    try:
        return send_from_directory(PDF_STORAGE_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404, description="File not found.")
