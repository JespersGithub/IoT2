import sqlite3
from datetime import datetime
import json
import paho.mqtt.subscribe as subscribe

print("Subscribe MQTT script running")

# Create table for distance data
def create_distance_table():
    query = """CREATE TABLE IF NOT EXISTS distance_data (
                   datetime TEXT NOT NULL,
                   distance REAL NOT NULL
               );"""
    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except sqlite3.Error as sql_e:
        print(f"sqlite error occurred: {sql_e}")
        conn.rollback()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()

create_distance_table()

# Callback function for MQTT message reception
def on_message_insert(client, userdata, message):
    query = """INSERT INTO distance_data (datetime, distance) VALUES (?, ?)"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hcr04_data = json.loads(message.payload.decode())

    if "distance" in hcr04_data:
        data = (now, hcr04_data["distance"])

        try:
            conn = sqlite3.connect("database/sensor_data.db")
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()
            print("Distance data inserted into database.")
        except sqlite3.Error as sql_e:
            print(f"sqlite error occurred: {sql_e}")
            conn.rollback()
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            conn.close()
    else:
        print("Received message does not contain 'distance' key.")


# Subscribe to MQTT topic and register callback function
subscribe.callback(on_message_insert, "paho/test/topic", hostname="40.67.233.215", userdata={"message_count": 0})
