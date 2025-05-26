def setup_token_valid(token):
    return token == "TECH123"

def allow_frontend_setup():
    print("Frontend setup allowed.")

def deny_access():
    print("Access denied.")

user = {'role': 'Technician'}
token = "TECH123"

if user['role'] == 'Technician' and setup_token_valid(token):
    allow_frontend_setup()
else:
    deny_access()
