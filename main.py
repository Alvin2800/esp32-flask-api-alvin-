from flask import Flask, request, jsonify

app = Flask(__name__)

temperature = 0
humidity = 0

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

@app.route("/temperature")
def get_temperature():
    return jsonify({"temperature": temperature})

@app.route("/humidity")
def get_humidity():
    return jsonify({"humidity": humidity})
    
@app.route("/emergency")
def get_emergency():
    return jsonify({"Emergency": emergency})
    
@app.route("/logs")
def get_logs():
    return jsonify(logs)
