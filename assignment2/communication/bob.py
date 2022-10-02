from this import s
from flask import Flask, redirect, url_for
import requests
import json
app = Flask(__name__)

PU_B = 1

@app.route("/", methods=["GET"])
def send_communication():
    requests.post("http://172.20.10.2:5000/")
    return {"Public key": PU_B}

@app.route("/", methods=["POST"])
def get_communication():
    data = requests.get("http://172.20.10.2:5000/").content
    print(json.loads(data))
    return json.loads(data)

@app.route("/")
def index():
    return "Helloeffv"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')