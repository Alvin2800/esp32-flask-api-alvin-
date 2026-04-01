from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

DB_PATH = "database.db"


def get_db_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS measurements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        temperature REAL NOT NULL,
        humidity REAL NOT NULL,
        emergency INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()


init_db()


def insert_data(timestamp, temperature, humidity, emergency):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO measurements (timestamp, temperature, humidity, emergency)
        VALUES (?, ?, ?, ?)
    """, (timestamp, temperature, humidity, emergency))

    conn.commit()
    conn.close()


temperature = 0.0
humidity = 0.0
emergency = 0


@app.route("/")
def home():
    return "IoT API Alvin Running", 200


@app.route("/data")
def data():
    global temperature, humidity, emergency

    try:
        temperature = float(request.args.get("temp", 0))
        humidity = float(request.args.get("hum", 0))
        emergency = int(request.args.get("emergency", 0))

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_data(timestamp, temperature, humidity, emergency)

        payload = {
            "timestamp": timestamp,
            "temperature": temperature,
            "humidity": humidity,
            "emergency": emergency
        }

        print("Données reçues :", payload, flush=True)
        return "OK", 200

    except Exception as e:
        print(f"Erreur /data : {e}", flush=True)
        return jsonify({"error": str(e)}), 500


@app.route("/status")
def status():
    try:
        return jsonify({
            "temperature": temperature,
            "humidity": humidity,
            "emergency": emergency
        })
    except Exception as e:
        print(f"Erreur /status : {e}", flush=True)
        return jsonify({"error": str(e)}), 500


@app.route("/logs")
def get_logs():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT timestamp, temperature, humidity, emergency
            FROM measurements
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        logs = []
        for row in rows:
            logs.append({
                "timestamp": row[0],
                "temperature": row[1],
                "humidity": row[2],
                "emergency": row[3]
            })

        return jsonify(logs)

    except Exception as e:
        print(f"Erreur /logs : {e}", flush=True)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
