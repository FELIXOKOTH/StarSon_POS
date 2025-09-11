# backend/routes/admin.py

from flask import Blueprint, request, jsonify
from backend.auth.firebase_auth import (
    create_firebase_user,
    generate_account_setup_link,
    approve_user_and_set_subscription,
    verify_user_token # To protect admin routes
)
from backend.services.email_service import send_setup_email

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# --- SECURED Admin Verification ---
def is_admin(user):
    """Checks if the user has admin privileges by checking custom claims."""
    # This now requires the user to have a 'role' of 'admin' in their token
    return user.get('role') == 'admin'

@admin_bp.route('/onboard-user', methods=['POST'])
def onboard_user():
    """
    API endpoint to create a new user and generate their setup link.
    Requires an admin to be authenticated.
    """
    # 1. Verify the request is from an authenticated admin
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization token is missing or invalid'}), 401

    id_token = auth_header.split('Bearer ')[1]
    admin_user = verify_user_token(id_token)

    if not admin_user or not is_admin(admin_user):
        return jsonify({'error': 'Unauthorized: Admin access required'}), 403

    # 2. Get the new user's email from the request
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({'error': 'Email is required'}), 400

    email = data['email']

    # 3. Create the user in Firebase
    new_user = create_firebase_user(email)
    if not new_user:
        return jsonify({'error': 'Failed to create user in Firebase'}), 500

    # 4. Generate the account setup link
    setup_link = generate_account_setup_link(email)
    if not setup_link:
        return jsonify({'error': 'Failed to generate account setup link'}), 500

    # 5. Send the email with the setup link
    send_setup_email(email, setup_link)
    print(f"SETUP LINK for {email} has been sent (simulated).") # For logging

    return jsonify({
        'message': 'User onboarding initiated successfully. Setup link sent.',
        'uid': new_user.uid
    }), 201

@admin_bp.route('/approve-user', methods=['POST'])
def approve_user():
    """
    API endpoint to approve a pending user and set their subscription.
    Requires an admin to be authenticated.
    """
    # 1. Verify the request is from an authenticated admin
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization token is missing or invalid'}), 401

    id_token = auth_header.split('Bearer ')[1]
    admin_user = verify_user_token(id_token)

    if not admin_user or not is_admin(admin_user):
        return jsonify({'error': 'Unauthorized: Admin access required'}), 403

    # 2. Get the UID and expiry date from the request
    data = request.get_json()
    if not data or 'uid' not in data or 'subscription_expiry' not in data:
        return jsonify({'error': 'User UID and subscription_expiry are required'}), 400

    uid_to_approve = data['uid']
    expiry_date = data['subscription_expiry']

    # 3. Approve the user in Firebase
    approve_user_and_set_subscription(uid_to_approve, expiry_date)

    return jsonify({'message': f'User {uid_to_approve} has been approved.'}), 200
