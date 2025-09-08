
import unittest
from unittest.mock import patch
from backend.receipt.receipt_delivery import generate_and_deliver

class TestReceiptDelivery(unittest.TestCase):

    @patch('backend.receipt.receipt_delivery.send_receipt_email')
    @patch('backend.receipt.receipt_delivery.send_sms_receipt')
    @patch('backend.receipt.receipt_delivery.generate_pdf_receipt')
    @patch('backend.receipt.receipt_delivery.generate_qr')
    def test_generate_and_deliver(self, mock_generate_qr, mock_generate_pdf, mock_send_sms, mock_send_email):
        receipt_data = {'receipt_number': '123'}
        customer_name = 'Test Customer'
        email = 'test@example.com'
        phone = '1234567890'

        mock_generate_pdf.return_value = '/path/to/receipt.pdf'
        mock_generate_qr.return_value = ('/path/to/qr.png', 'http://example.com/receipt.pdf')

        generate_and_deliver(receipt_data, customer_name, email, phone)

        mock_generate_pdf.assert_called_once_with(receipt_data, customer_name)
        mock_generate_qr.assert_called_once_with('/path/to/receipt.pdf')
        mock_send_email.assert_called_once_with(email, customer_name, '123', '/path/to/receipt.pdf')
        mock_send_sms.assert_called_once_with(phone, 'http://example.com/receipt.pdf')

if __name__ == '__main__':
    unittest.main()

