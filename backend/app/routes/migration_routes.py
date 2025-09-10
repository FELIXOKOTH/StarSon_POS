
from flask import Blueprint, render_template, request, jsonify
import os
import json
from werkzeug.utils import secure_filename
from ai.gemini_vision_analyzer import GeminiVisionAnalyzer

# Blueprint setup
migration_bp = Blueprint('migration_bp', __name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'csv'}
INVENTORY_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'inventory.json')

# Ensure necessary folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(INVENTORY_FILE), exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@migration_bp.route('/migrate', methods=['GET'])
def migration_page():
    """Renders the main migration assistant page."""
    return render_template('migration_assistant.html')

@migration_bp.route('/migrate/analyze', methods=['POST'])
def analyze_inventory_document():
    """Handles document upload, analysis via Gemini, and returns structured JSON."""
    if 'inventory_file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['inventory_file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid or no file selected"}), 400

    gemini_api_key = os.environ.get('GEMINI_API_KEY')
    if not gemini_api_key:
        return jsonify({"error": "Server configuration error: GEMINI_API_KEY not set."}), 500

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        analyzer = GeminiVisionAnalyzer(api_key=gemini_api_key)
        prompt = (
            "You are an inventory scanning assistant. Analyze the document to extract product details. "
            "Return a single JSON object with a key 'inventory_items', containing a list of items. "
            "Each item should be an object with keys: 'name', 'quantity', 'sku', and 'price'."
        )
        result_text = analyzer.analyze_document(filepath, prompt)
        clean_json_str = result_text.strip().replace('```json', '').replace('```', '')
        result_json = json.loads(clean_json_str)
        return jsonify(result_json)
    except Exception as e:
        print(f"Analysis Error: {e}")
        return jsonify({"error": "Failed to analyze the document."}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

@migration_bp.route('/migrate/import', methods=['POST'])
def import_inventory_data():
    """Receives confirmed data, updates the inventory file, and returns the status."""
    new_data = request.get_json()
    if not new_data or 'inventory_items' not in new_data:
        return jsonify({"status": "error", "message": "No data provided."}), 400

    items_to_import = new_data['inventory_items']

    try:
        # Load existing inventory
        try:
            with open(INVENTORY_FILE, 'r') as f:
                inventory_list = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            inventory_list = []

        # Use a dictionary for efficient SKU lookups
        inventory_map = {item['sku']: item for item in inventory_list}
        
        added_count = 0
        updated_count = 0

        for item in items_to_import:
            sku = item.get('sku')
            if not sku:
                continue # Skip items without a SKU

            # Convert quantity and price to the correct type
            try:
                quantity = int(item.get('quantity', 0))
                price = float(item.get('price', 0.0))
            except (ValueError, TypeError):
                quantity = 0
                price = 0.0

            if sku in inventory_map:
                # Update existing item
                existing_item = inventory_map[sku]
                existing_item['quantity'] = int(existing_item.get('quantity', 0)) + quantity
                existing_item['price'] = price # Update price to the latest value
                existing_item['name'] = item.get('name', existing_item['name'])
                updated_count += 1
            else:
                # Add new item
                inventory_map[sku] = {
                    'name': item.get('name'),
                    'quantity': quantity,
                    'sku': sku,
                    'price': price
                }
                added_count += 1

        # Save the updated inventory
        with open(INVENTORY_FILE, 'w') as f:
            json.dump(list(inventory_map.values()), f, indent=4)

        return jsonify({
            "status": "success",
            "message": f"Import complete! {added_count} items added, {updated_count} items updated."
        })

    except Exception as e:
        print(f"Import Error: {e}")
        return jsonify({"status": "error", "message": "An internal error occurred during import."}), 500
