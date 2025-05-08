# integrations/miti_pesa_api.py

import requests
import json
from config.settings import MITI_PESA_API_KEY, MITI_PESA_ENDPOINT

def send_carbon_data_to_miti_pesa(store_id, receipts_saved):
    from core.carbon_calculator import calculate_carbon_savings
    
    carbon_data = calculate_carbon_savings(receipts_saved)

    payload = {
        "store_id": store_id,
        "receipts_saved": carbon_data["receipts_saved"],
        "co2_saved_kg": carbon_data["co2_saved_kg"]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MITI_PESA_API_KEY}"
    }

    try:
        response = requests.post(MITI_PESA_ENDPOINT, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return {"status": "success", "response": response.json()}
        else:
            return {"status": "error", "code": response.status_code, "detail": response.text}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
