from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

temperature = 0
humidity = 0
emergency = 0
logs = []

@app.route("/")
def home():
    return "ESP32 IoT Server Running"

@app.route("/data")
def data():
    global temperature, humidity, emergency

    temperature = float(request.args.get("temp", 0))
    humidity = float(request.args.get("hum", 0))
    emergency= int(request.args.get("emergency",0))
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temperature,
        "humidity": humidity,
        "emergency": emergency
    }
    logs.append(log_entry)

    print("Données reçues :", log_entry, flush=True)

    return "OK", 200

@app.route("/status")
def status():
    return jsonify({
        "temperature": temperature,
        "humidity": humidity,
        "emergency": emergency
    })
    
@app.route("/logs")
def get_logs():
    return jsonify(logs)
