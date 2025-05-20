import requests
import csv
import os
from datetime import datetime

DATA_PATH = "data/history.csv"
API_URL = "https://hub.spacestation14.com/api/servers"

def fetch_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def ensure_data_folder():
    if not os.path.exists("data"):
        os.makedirs("data")

def append_data(servers):
    now = datetime.utcnow().isoformat()
    fields = [
        "timestamp", "address", "name", "map", "preset", "players", "soft_max_players", "run_level", "round_id",
        "round_start_time", "tags", "inferredTags"
    ]
    file_exists = os.path.isfile(DATA_PATH)
    with open(DATA_PATH, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(fields)
        for s in servers:
            sd = s.get("statusData", {})
            writer.writerow([
                now,
                s.get("address"),
                sd.get("name"),
                sd.get("map"),
                sd.get("preset"),
                sd.get("players"),
                sd.get("soft_max_players"),
                sd.get("run_level"),
                sd.get("round_id"),
                sd.get("round_start_time"),
                ",".join(sd.get("tags", [])),
                ",".join(s.get("inferredTags", [])),
            ])

if __name__ == "__main__":
    ensure_data_folder()
    data = fetch_data()
    append_data(data)
