import base64
from io import BytesIO
from matplotlib.figure import Figure
from flask import Flask, render_template, jsonify
from get_stue_dht11_data import get_stue_data
from get_hcr04_data import get_distance_data
from get_batteri_data import get_battery_data
import sqlite3

app = Flask(__name__)

def stue_temp():
    timestamps, temp, hum = get_stue_data(10)
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor('#fff')
    ax.plot(timestamps, temp, linestyle = "dashed", c="#11f", linewidth="1.5", marker="o",)
    ax.set_xlabel("Timestamps")
    ax.set_ylabel("temperature celsius")
    fig.patch.set_facecolor("#fff")
    ax.tick_params(axis="x", colors="black")
    ax.tick_params(axis="y", colors="black")
    ax.spines['left'].set_color("blue")
    ax.spines['right'].set_color("blue")
    ax.spines['top'].set_color("blue")
    ax.spines['bottom'].set_color("blue")
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def stue_hum():
    timestamps, temp, hum = get_stue_data(10)
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor('#fff')
    ax.plot(timestamps, hum, linestyle = "dashed", c="#11f", linewidth="1.5", marker="o",)
    ax.set_xlabel("Timestamps")
    ax.set_ylabel("humidity")
    fig.patch.set_facecolor("#fff")
    ax.tick_params(axis="x", colors="black")
    ax.tick_params(axis="y", colors="black")
    ax.spines['left'].set_color("blue")
    ax.spines['right'].set_color("blue")
    ax.spines['top'].set_color("blue")
    ax.spines['bottom'].set_color("blue")
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data


def distance_data():
    timestamps, distances = get_distance_data(10)
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor('#fff')
    ax.plot(timestamps, distances, linestyle="dashed", c="#11f", linewidth="1.5", marker="o")
    ax.set_xlabel("Timestamps")
    ax.set_ylabel("Distance (cm)")
    fig.patch.set_facecolor("#fff")
    ax.tick_params(axis="x", colors="black")
    ax.tick_params(axis="y", colors="black")
    ax.spines['left'].set_color("blue")
    ax.spines['right'].set_color("blue")
    ax.spines['top'].set_color("blue")
    ax.spines['bottom'].set_color("blue")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def battery_data():
    timestamps, percentages = get_battery_data(10)
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor('#fff')
    ax.plot(timestamps, percentages, linestyle="dashed", c="#11f", linewidth="1.5", marker="o")
    ax.set_xlabel("Timestamps")
    ax.set_ylabel("Battery Percentage")
    fig.patch.set_facecolor("#fff")
    ax.tick_params(axis="x", colors="black")
    ax.tick_params(axis="y", colors="black")
    ax.spines['left'].set_color("blue")
    ax.spines['right'].set_color("blue")
    ax.spines['top'].set_color("blue")
    ax.spines['bottom'].set_color("blue")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plot_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    latest_battery_percentage = percentages[-1] if percentages else 0
    return plot_data, latest_battery_percentage


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/kapacitet')
def kapacitet():
    data = distance_data()
    return render_template('kapacitet.html', plot_data=data)

@app.route('/fugtighed')
def stue():
    stue_temperature = stue_temp()
    stue_humidity = stue_hum()
    return render_template('fugtighed.html', stue_temperature = stue_temperature, stue_humidity = stue_humidity)

@app.route('/lokation')
def lokation():
    return render_template('lokation.html')
def get_gps_data():
    koordinater = lokation()
    return jsonify(koordinater)

from flask import jsonify

@app.route('/gps_data')
def get_gps_data():
    # Fetch GPS data from the database
    conn = sqlite3.connect("database/sensor_data.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM gps_data ORDER BY timestamp DESC LIMIT 1")
    gps_data = cur.fetchone()
    conn.close()

    # Return GPS data as JSON
    if gps_data:
        timestamp, latitude, longitude = gps_data
        return jsonify({
            "timestamp": timestamp,
            "latitude": latitude,
            "longitude": longitude
        })
    else:
        return jsonify({})


@app.route('/batteri')
def batteri():
    plot_data, latest_battery_percentage = battery_data()
    return render_template('batteri.html', plot_data=plot_data, battery_percentage=latest_battery_percentage)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)