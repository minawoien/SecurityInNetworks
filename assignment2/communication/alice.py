from crypt import methods
from flask import Flask, request, Response, jsonify
import requests, json

app = Flask(__name__)

PU_A = 0

@app.route("/", methods=["POST"])
def get_communication():
    data = requests.get("http://172.20.10.2:5001/").content
    print(json.loads(data))
    return "Hihi"

@app.route("/", methods=["GET"])
def send_communication():
    requests.post("http://172.20.10.2:5001/")
    return {"Public key": PU_A}

@app.route("/", methods=["GET"])
def index():
    return "Hello"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')