import sqlite3

def get_battery_data(number_of_rows):
    query = """SELECT * FROM battery_data ORDER BY datetime DESC LIMIT ?"""
    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query, (number_of_rows,))
        rows = cur.fetchall()
        datetimes = []
        percentages = []
        for row in reversed(rows):
            datetimes.append(row[0])
            percentages.append(row[1])
        return datetimes, percentages
    except sqlite3.Error as sql_e:
        print(f"SQLite error occurred: {sql_e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()
