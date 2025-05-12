def detect_provider(phone_number):
    if phone_number.startswith('+2547'):
        return "Safaricom"
    elif phone_number.startswith('+2541'):
        return "Airtel"
    else:
        return "DefaultProvider"

print(detect_provider('+254712345678'))