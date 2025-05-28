import requests
import os

def generate_public_link(file_path):
    """
    Uploads the given file to file.io and returns a temporary public download link.

    Args:
        file_path (str): Path to the local PDF file to upload.

    Returns:
        str: Public link to the uploaded file (valid for one download or limited time).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError("Receipt file does not exist.")

    with open(file_path, 'rb') as f:
        response = requests.post("https://file.io", files={"file": f})

    if response.status_code == 200:
        res_json = response.json()
        return res_json.get("link", "Link not available")
    else:
        raise Exception(f"Upload failed. Status: {response.status_code}, Message: {response.text}")


# Test run
if __name__ == "__main__":
    test_file = "receipts/receipt_Jane_Doe_20250527_123456.pdf"
    try:
        link = generate_public_link(test_file)
        print("Public PDF Link:", link)
    except Exception as e:
        print("Error:", str(e))
