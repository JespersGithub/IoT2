import sqlite3
from datetime import datetime

def get_gps_data(number_of_rows):
    query = """SELECT * FROM gps_data WHERE latitude IS NOT NULL AND longitude IS NOT NULL ORDER BY datetime DESC;"""
    timestamps = []
    latitudes = []
    longitudes = []
    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchmany(number_of_rows)
        for row in reversed(rows):
            timestamps.append(row[0])
            latitudes.append(row[1])  # Assuming latitude is stored at index 3 in the database
            longitudes.append(row[2])  # Assuming longitude is stored at index 4 in the database
        return timestamps, latitudes, longitudes
    except sqlite3.Error as sql_e:
        print(f"SQLite error occurred: {sql_e}")
        conn.rollback()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()

# Example usage:
timestamps, latitudes, longitudes = get_gps_data(10)
print("Recent GPS data:")
for i in range(len(timestamps)):
    print(f"Datetime: {timestamps[i]}, Latitude: {latitudes[i]}, Longitude: {longitudes[i]}")
