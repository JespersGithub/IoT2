import sqlite3
from datetime import datetime
import json
import paho.mqtt.subscribe as subscribe

print("Subscribe MQTT script running")

def create_table():
    query = """CREATE TABLE IF NOT EXISTS gps_data (timestamp TEXT NOT NULL, latitude REAL NOT NULL, longitude REAL NOT NULL);"""
    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except sqlite3.Error as sql_e:
        print(f"SQLite error occurred: {sql_e}")
        conn.rollback()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:  
        conn.close()

create_table()

def on_message_print(client, userdata, message):
    now = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    payload = json.loads(message.payload.decode())
            
    if 'latitude' in payload and 'longitude' in payload:
        # GPS data
        query = """INSERT INTO gps_data (timestamp, latitude, longitude) VALUES (?, ?, ?)"""
        data = (now, payload['latitude'], payload['longitude'])

        try:
            conn = sqlite3.connect("database/sensor_data.db")
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()
        except sqlite3.Error as sql_e:
            print(f"SQLite error occurred: {sql_e}")
            conn.rollback()
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            conn.close()

subscribe.callback(on_message_print, "paho/test/topic", hostname="40.67.233.215", userdata={"message_count": 0})
