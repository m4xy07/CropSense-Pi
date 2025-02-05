import sqlite3
import json

# Load crop data from JSON file
with open("cropsdb.json", "r") as file:
    crops_data = json.load(file)["crops"]

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("crops.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS crops (
    id INTEGER PRIMARY KEY,
    name TEXT,
    min_temp REAL,
    max_temp REAL,
    min_humidity REAL,
    max_humidity REAL,
    min_soil_moisture REAL,
    max_soil_moisture REAL,
    sowing_months TEXT,
    harvesting_months TEXT,
    wholesale_price TEXT,
    retail_price TEXT,
    npk_fertilizer TEXT,
    npk_uptake TEXT
)
""")

# Insert crop data into table
for crop in crops_data:
    cursor.execute("""
    INSERT INTO crops (name, min_temp, max_temp, min_humidity, max_humidity, min_soil_moisture, max_soil_moisture, sowing_months, harvesting_months, wholesale_price, retail_price, npk_fertilizer, npk_uptake)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        crop["name"],
        crop["temperature"]["min"],
        crop["temperature"]["max"],
        crop["humidity"]["min"],
        crop["humidity"]["max"],
        crop["soil_moisture"]["min"],
        crop["soil_moisture"]["max"],
        json.dumps(crop["sowing_months"]),
        json.dumps(crop["harvesting_months"]),
        json.dumps(crop["wholesale_price"]),
        json.dumps(crop["retail_price"]),
        crop["NPK_fertilizer"],
        json.dumps(crop["NPK_uptake_(kg/ha)"])
    ))

# Commit changes and close connection
conn.commit()
conn.close()
