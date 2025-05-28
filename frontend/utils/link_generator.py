import os
import uuid

# Define base URL where your PDFs are hosted (adjust this to your actual domain)
BASE_PUBLIC_URL = "https://donkaunda.com/receipts"  # Replace with actual domain

# Define the folder where PDFs are stored
RECEIPT_FOLDER = "static/receipts"

def generate_unique_filename(extension="pdf"):
    """
    Generate a unique filename using UUID.
    """
    return f"{uuid.uuid4().hex}.{extension}"

def save_pdf_to_public_dir(file_content: bytes, filename: str = None) -> str:
    """
    Save a PDF file to the public directory and return its public URL.
    """
    if not os.path.exists(RECEIPT_FOLDER):
        os.makedirs(RECEIPT_FOLDER)

    if not filename:
        filename = generate_unique_filename()

    filepath = os.path.join(RECEIPT_FOLDER, filename)

    with open(filepath, "wb") as f:
        f.write(file_content)

    public_url = f"{BASE_PUBLIC_URL}/{filename}"
    return public_url

def get_existing_public_link(filename: str) -> str:
    """
    Construct a public link for an existing file.
    """
    return f"{BASE_PUBLIC_URL}/{filename}"
