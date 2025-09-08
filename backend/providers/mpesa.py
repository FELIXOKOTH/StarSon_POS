
from .base import BasePaymentProvider
from backend.integrations.daraja import SafaricomAPI

class SafaricomMpesaProvider(BasePaymentProvider):
    """
    Concrete implementation for Safaricom M-Pesa payments via the Daraja API.
    """

    def __init__(self, api_client: SafaricomAPI):
        self.api_client = api_client

    def get_provider_name(self) -> str:
        return "safaricom_mpesa"

    def initiate_payment(self, txn_id: str, amount: float, phone_number: str, **kwargs) -> dict:
        """Initiates an STK push for M-Pesa."""
        account_ref = kwargs.get("account_ref", "StarSonPOS")
        transaction_desc = kwargs.get("transaction_desc", "POS Payment")
        callback_url_base = kwargs.get("callback_url_base")

        if not callback_url_base:
            raise ValueError("callback_url_base is required for M-Pesa STK push")

        # The callback URL must be unique for the provider to track the transaction
        callback_url = f"{callback_url_base}callback/{self.get_provider_name()}/{txn_id}"
        
        response = self.api_client.initiate_stk_push(
            phone_number=phone_number,
            amount=str(amount),
            account_reference=account_ref,
            transaction_desc=transaction_desc,
            callback_url=callback_url
        )
        return response

    def handle_callback(self, txn_id: str, data: dict) -> tuple:
        """Processes the callback from the Daraja API."""
        status = 'failed'
        processed_data = {'provider_name': self.get_provider_name()}

        stk_callback = data.get('Body', {}).get('stkCallback', {})
        result_code = stk_callback.get('ResultCode', -1)

        if result_code == 0:
            status = 'completed'
            # Extract useful metadata from the successful callback
            callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
            for item in callback_metadata:
                if item['Name'] == 'Amount':
                    processed_data['amount_paid'] = item.get('Value')
                elif item['Name'] == 'MpesaReceiptNumber':
                    processed_data['provider_receipt'] = item.get('Value')
                elif item['Name'] == 'PhoneNumber':
                    processed_data['customer_phone'] = item.get('Value')
        else:
            processed_data['error_message'] = stk_callback.get('ResultDesc', 'Unknown error')

        return status, processed_data
