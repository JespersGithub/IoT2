import sqlite3
from datetime import datetime

def get_distance_data(number_of_rows):
    query = """SELECT datetime, distance FROM distance_data ORDER BY datetime DESC;"""
    datetimes = []
    distances = []
    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchmany(number_of_rows)
        for row in reversed(rows):
             datetimes.append(row[0])
             distances.append(row[1])
        return datetimes, distances
        
    except sqlite3.Error as sql_e:
        print(f"sqlite error occurred: {sql_e}")
        conn.rollback()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()

# Test the function by fetching the latest 10 records
datetimes, distances = get_distance_data(10)
print("Latest 10 distance records:")
for dt, dist in zip(datetimes, distances):
    print(f"Datetime: {dt}, Distance: {dist}")
