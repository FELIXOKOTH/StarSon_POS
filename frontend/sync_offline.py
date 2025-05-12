# Offline sync simulation
def get_unsynced_data():
    return ['sale1', 'sale2']

def send_to_server(data):
    print(f"Syncing {data} to server...")

def mark_as_synced(data):
    print(f"{data} marked as synced.")

def sync_local_to_server():
    local_data = get_unsynced_data()
    for data in local_data:
        try:
            send_to_server(data)
            mark_as_synced(data)
        except:
            continue

sync_local_to_server()