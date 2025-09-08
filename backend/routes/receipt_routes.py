
from flask import Blueprint, request, jsonify
from receipt.receipt_generator import generate_pdf_receipt
import os

receipt_routes = Blueprint('receipt_routes', __name__)

@receipt_routes.route("/api/receipt", methods=['POST'])
def create_receipt_route():
    data = request.get_json()
    receipt_data = data.get('receipt_data')
    customer_name = data.get('customer_name')
    reference_url = data.get('reference_url')

    if not receipt_data or not customer_name:
        return jsonify({"error": "Missing receipt_data or customer_name"}), 400

    try:
        receipt_path = generate_pdf_receipt(receipt_data, customer_name, reference_url)
        return jsonify({"receipt_path": receipt_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
