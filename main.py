from flask import Flask, request, jsonify

app = Flask(__name__)

temperature = 0
humidity = 0

@app.route("/")
def home():
    return "ESP32 IoT Server Running"

@app.route("/data")
def data():
    global temperature, humidity

    temperature = request.args.get("temp", 0)
    humidity = request.args.get("hum", 0)

    print("Température :", temperature, flush=True)
    print("Humidité :", humidity, flush=True)

    return "OK", 200

@app.route("/temperature")
def get_temperature():
    return jsonify({"temperature": temperature})

@app.route("/humidity")
def get_humidity():
    return jsonify({"humidity": humidity})
