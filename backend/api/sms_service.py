# backend/api/sms_service.py

import requests

class SMSService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://smsapi.example.com/send"  # Replace with actual SMS service URL

    def send_sms(self, phone_number, message):
        payload = {
            'api_key': self.api_key,
            'phone_number': phone_number,
            'message': message
        }
        response = requests.post(self.api_url, data=payload)
        if response.status_code == 200:
            return "SMS sent successfully"
        else:
            return f"Failed to send SMS: {response.text}"
