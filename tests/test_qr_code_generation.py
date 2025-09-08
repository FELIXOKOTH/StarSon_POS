
import unittest
import os
from backend.receipt.receipt_generator import generate_pdf_receipt
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
from io import BytesIO

class TestQRCodeGeneration(unittest.TestCase):

    def test_qr_code_generation_and_content(self):
        receipt_data = {
            'items': [{'name': 'Test Item', 'qty': 1, 'price': 10.00}],
            'total': 10.00
        }
        customer_name = 'Test Customer'
        reference_url = 'http://example.com/receipt/123'
        
        # Generate the PDF receipt with QR code
        pdf_path = generate_pdf_receipt(receipt_data, customer_name, reference_url=reference_url)

        # For this test, we'll generate a QR code directly and read it
        # This is because extracting the QR from the PDF is complex
        qr = qrcode.make(reference_url)
        
        # Save the QR code to a buffer
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Use Pillow to open the image from the buffer
        img = Image.open(buffer)
        
        # Decode the QR code
        decoded_qr = decode(img)
        
        self.assertTrue(len(decoded_qr) > 0, "QR Code not found or is not readable.")
        
        qr_data = decoded_qr[0].data.decode('utf-8')
        
        self.assertEqual(qr_data, reference_url, "QR Code content does not match the reference URL.")

        # Clean up the generated PDF file
        os.remove(pdf_path)

if __name__ == '__main__':
    unittest.main()
