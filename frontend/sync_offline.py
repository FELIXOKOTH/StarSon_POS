import requests
import json
import os
import time

LOCAL_STORE = "unsynced_sales.json"
BACKEND_API_URL = "https://your-backend-domain.com/api/sync_sales"  # replace with actual URL

def get_unsynced_data():
    if not os.path.exists(LOCAL_STORE):
        return []
    with open(LOCAL_STORE, "r") as f:
        return json.load(f)

def save_unsynced_data(data):
    with open(LOCAL_STORE, "w") as f:
        json.dump(data, f, indent=4)

def send_to_server(sale):
    response = requests.post(BACKEND_API_URL, json=sale, timeout=5)
    return response.status_code == 200

def mark_as_synced(data, synced_index):
    for index in sorted(synced_index, reverse=True):
        del data[index]
    save_unsynced_data(data)

def sync_local_to_server():
    local_data = get_unsynced_data()
    if not local_data:
        print("No unsynced data found.")
        return

    print("Starting sync...")

    synced_indices = []

    for idx, sale in enumerate(local_data):
        try:
            success = send_to_server(sale)
            if success:
                print(f"Synced sale: {sale}")
                synced_indices.append(idx)
            else:
                print(f"Failed to sync: {sale}")
        except Exception as e:
            print(f"Error syncing sale {sale}: {str(e)}")

    if synced_indices:
        mark_as_synced(local_data, synced_indices)
        print("Synced and updated local store.")
    else:
        print("No data was synced.")

if __name__ == "__main__":
    sync_local_to_server()
