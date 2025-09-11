import firebase_admin
from firebase_admin import credentials, auth
from backend.secure.secure_setup import load_api_key # Assuming you store Firebase credentials securely

# It's recommended to store your Firebase service account key path in a secure way
# For this example, we'll imagine it's handled by your secure_setup module

def initialize_firebase():
    """
    Initializes the Firebase Admin SDK.
    Make sure your Firebase service account key JSON file is secured and its path is correct.
    """
    try:
        # Option 1: From a securely stored file (Best Practice)
        # In a real app, you would securely retrieve the path to this file.
        # For example: cred_path = load_api_key("secure/firebase_service_account.key")
        cred_path = "path/to/your/firebase-service-account-key.json"
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully.")
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")
        print("Please ensure your service account key is correctly configured.")


def verify_user_token(id_token):
    """
    Verifies the ID token sent from the client.

    Args:
        id_token: The Firebase ID token from the request's Authorization header.

    Returns:
        The decoded token containing user info (like UID), or None if invalid.
    """
    if not firebase_admin._apps:
        initialize_firebase()

    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Invalid or expired token: {e}")
        return None

# --- NEW FUNCTIONS FOR SECURE USER ONBOARDING ---

def create_firebase_user(email):
    """
    Creates a new user in Firebase Authentication without a password
    and sets their initial status to 'pending'.

    Args:
        email: The new user's email address.

    Returns:
        The user object from Firebase, or None on failure.
    """
    if not firebase_admin._apps:
        initialize_firebase()

    try:
        # Create user without a password
        user = auth.create_user(email=email)
        print(f"Successfully created new user: {user.uid}")

        # Set initial custom claims for account status
        auth.set_custom_user_claims(user.uid, {'status': 'pending'})
        print(f"Set initial 'pending' status for user: {user.uid}")

        return user
    except Exception as e:
        print(f"Error creating Firebase user: {e}")
        return None

def generate_account_setup_link(email):
    """
    Generates a password reset link that can be used for initial account setup.

    Args:
        email: The user's email address.

    Returns:
        The setup link string, or None on failure.
    """
    if not firebase_admin._apps:
        initialize_firebase()

    try:
        link = auth.generate_password_reset_link(email)
        return link
    except Exception as e:
        print(f"Error generating account setup link: {e}")
        return None

def approve_user_and_set_subscription(uid, expiry_date_str):
    """
    Approves a user by updating their custom claims and sets their subscription expiry.

    Args:
        uid: The Firebase UID of the user to approve.
        expiry_date_str: The subscription expiry date as a string (e.g., "YYYY-MM-DD").
    """
    if not firebase_admin._apps:
        initialize_firebase()

    try:
        # Update claims to 'approved' and set subscription expiry
        auth.set_custom_user_claims(uid, {
            'status': 'approved',
            'subscription_expiry': expiry_date_str
        })
        print(f"Successfully approved user {uid} with expiry {expiry_date_str}")
    except Exception as e:
        print(f"Error approving user: {e}")

# Example of how you would change your Flask route:
#
# from flask import request
# from backend.auth.firebase_auth import verify_user_token
#
# @app.route('/api/some_protected_resource')
# def protected_resource():
#     auth_header = request.headers.get('Authorization')
#     if not auth_header or not auth_header.startswith('Bearer '):
#         return {'error': 'Authorization token is missing or invalid'}, 401
#
#     id_token = auth_header.split('Bearer ')[1]
#     user = verify_user_token(id_token)
#
#     if not user:
#         return {'error': 'Invalid token'}, 403
#     
#     # Check for custom claims
#     if user.get('status') != 'approved':
#          return {'error': 'Account not approved'}, 403
#
#     # Now you have the user's UID and can perform actions on their behalf
#     user_uid = user['uid']
#     return {'message': f'Success! You are user {user_uid}'}

