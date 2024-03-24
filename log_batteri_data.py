import sqlite3
from datetime import datetime  # Add import statement for datetime
import json
import paho.mqtt.subscribe as subscribe

print("Subscribe MQTT script running")

# Create table for battery data
def create_battery_table():
    query = """CREATE TABLE IF NOT EXISTS battery_data (
                   datetime TEXT NOT NULL,
                   percentage REAL NOT NULL
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

create_battery_table()

# Callback function for MQTT message reception
def on_message_store_battery(client, userdata, message):
    query = """INSERT INTO battery_data (datetime, percentage) VALUES (?, ?)"""
    now = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    battery_data = float(message.payload.decode())
    rounded_percentage = round(battery_data, 2)  # Round the percentage to two decimal places
    data = (now, rounded_percentage)

    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
    except sqlite3.Error as sql_e:
        print(f"sqlite error occurred: {sql_e}")
        conn.rollback()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()


# Subscribe to MQTT topic and register callback function
subscribe.callback(on_message_store_battery, "battery/percentage", hostname="40.67.233.215", userdata={"message_count": 0})
