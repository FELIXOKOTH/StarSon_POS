
def setup_token_valid(token: str) -> bool:
    """Check if the provided token matches the allowed technician token."""
    VALID_TOKEN = "TECH123"
    return token == VALID_TOKEN

def allow_frontend_setup():
    """Function triggered when frontend setup is permitted."""
    print("[ACCESS GRANTED] Frontend setup allowed.")

def deny_access():
    """Function triggered when frontend setup is denied."""
    print("[ACCESS DENIED] You do not have the necessary permissions.")

def check_frontend_setup_access(user: dict, token: str):
    """
    Validate user role and token before allowing frontend setup.
    
    Args:
        user (dict): Dictionary containing user information.
        token (str): Technician token to validate.
    """
    if user.get('role') == 'Technician' and setup_token_valid(token):
        allow_frontend_setup()
    else:
        deny_access()

# Example usage
if __name__ == "__main__":
    user = {'role': 'Technician'}
    token = "TECH123"
    check_frontend_setup_access(user, token)
