import os

db_path = "sensor_data.db"  # path to your SQLite DB

if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Deleted {db_path} ")
else:
    print(f"No database found at {db_path}")
