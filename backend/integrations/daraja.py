
import base64
import datetime
import requests

class SafaricomAPI:
    """
    A wrapper class for the Safaricom Daraja API.
    Handles token generation and making API requests.
    """

    def __init__(self, consumer_key, consumer_secret, shortcode, passkey, env="sandbox"):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.shortcode = shortcode
        self.passkey = passkey
        self.api_base_url = "https://sandbox.safaricom.co.ke" if env == "sandbox" else "https://api.safaricom.co.ke"
        
        # This is the critical change: handle the error here.
        try:
            self.access_token = self._get_access_token()
        except Exception as e:
            # If we can't get a token, the application is non-functional. Raise the error immediately.
            raise RuntimeError(f"Failed to get Safaricom access token: {e}")

    def _get_access_token(self) -> str:
        """Retrieves an OAuth access token from the Safaricom API."""
        url = f"{self.api_base_url}/oauth/v1/generate?grant_type=client_credentials"
        
        try:
            response = requests.get(url, auth=(self.consumer_key, self.consumer_secret))
            response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)
            return response.json()["access_token"]
        except requests.exceptions.RequestException as e:
            # This wraps the underlying network error in a more specific exception.
            raise Exception(f"Error getting access token: {e}\nResponse: {response.text if 'response' in locals() else 'No response'}")

    def _get_stk_password_and_timestamp(self) -> tuple:
        """Generates the base64 encoded password required for STK Push."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        password_str = self.shortcode + self.passkey + timestamp
        password_bytes = password_str.encode("ascii")
        return base64.b64encode(password_bytes).decode("utf-8"), timestamp

    def initiate_stk_push(self, phone_number: str, amount: str, account_reference: str, transaction_desc: str, callback_url: str) -> dict:
        """Initiates an STK Push request to the Safaricom API."""
        password, timestamp = self._get_stk_password_and_timestamp()
        
        url = f"{self.api_base_url}/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer " + self.access_token}
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc,
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"STK push failed: {e}\nResponse: {response.text}")
