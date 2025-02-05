import sqlite3
import json

def load_crop_database():
    conn = sqlite3.connect("crops.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crops")
    crops = cursor.fetchall()
    conn.close()
    return crops

def find_best_crop(temperature, humidity, soil_moisture, month):
    crops = load_crop_database()
    best_crop = None
    for crop in crops:
        name, min_temp, max_temp, min_humidity, max_humidity, min_soil_moisture, max_soil_moisture, sowing_months, harvesting_months, wholesale_price, retail_price, npk_fertilizer, npk_uptake = crop[1:]
        sowing_months = json.loads(sowing_months)
        if (min_temp <= temperature <= max_temp and
            min_humidity <= humidity <= max_humidity and
            min_soil_moisture <= soil_moisture <= max_soil_moisture and
            month in sowing_months):
            best_crop = name
            break
    return best_crop
