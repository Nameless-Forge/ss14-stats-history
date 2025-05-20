import requests
import csv
import os
from datetime import datetime

DATA_PATH = "data/history.csv"
API_URL = "https://hub.spacestation14.com/api/servers"

STATUS_FIELDS = [
    "map",
    "name",
    "tags",
    "preset",
    "players",
    "round_id",
    "run_level",
    "panic_bunker",
    "round_start_time",
    "soft_max_players",
    "baby_jail",
    "planet_map",
    "playerlist",
    "characters",
    "short_name",
    "queue",
    "real_ip",
    "real_name"
]

def round_to_nearest_10_minutes(dt: datetime):
    rounded_minute = (dt.minute // 10) * 10
    return dt.replace(minute=rounded_minute, second=0, microsecond=0)

def fetch_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def ensure_data_folder():
    if not os.path.exists("data"):
        os.makedirs("data")

def get_field_value(sd, key):
    v = sd.get(key, '')
    # Если список, склеиваем через запятую
    if isinstance(v, list):
        return ','.join(map(str, v))
    # Для bool возвращаем как 0/1
    if isinstance(v, bool):
        return int(v)
    return v

def append_data(servers):
    dt_now = datetime.utcnow()
    rounded_dt = round_to_nearest_10_minutes(dt_now)
    dt_str = rounded_dt.strftime("%Y-%m-%d %H:%M")
    year = rounded_dt.year
    month = rounded_dt.month
    day = rounded_dt.day
    hour = rounded_dt.hour
    minute = rounded_dt.minute
    weekday = rounded_dt.isoweekday()

    fields = [
        "datetime",
        "year",
        "month",
        "day",
        "hour",
        "minute",
        "weekday",
        "timestamp_iso",
        "address",
    ] + STATUS_FIELDS

    file_exists = os.path.isfile(DATA_PATH)
    with open(DATA_PATH, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(fields)
        for s in servers:
            sd = s.get("statusData", {})
            row = [
                dt_str,
                year,
                month,
                day,
                hour,
                minute,
                weekday,
                rounded_dt.isoformat(),
                s.get("address"),
            ]
            row += [get_field_value(sd, key) for key in STATUS_FIELDS]
            writer.writerow(row)

if __name__ == "__main__":
    ensure_data_folder()
    data = fetch_data()
    append_data(data)
