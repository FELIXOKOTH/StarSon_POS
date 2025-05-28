from flask import Blueprint, send_from_directory, abort, request
import os

serve_pdf_bp = Blueprint("serve_pdf", __name__)

PDF_STORAGE_DIR = os.path.abspath("pdf_storage")  # Adjust as needed

@serve_pdf_bp.route("/api/pdf/<filename>", methods=["GET"])
def serve_pdf(filename):
    token = request.args.get("token")
    if token != "TECH123":  # Replace with real token validation
        abort(403, description="Access denied.")
    
    try:
        return send_from_directory(PDF_STORAGE_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404, description="File not found.")
