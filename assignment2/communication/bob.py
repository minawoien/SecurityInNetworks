from this import s
from flask import Flask, redirect, url_for
import requests
import json

from secure_communication import *

dh = DiffieHellman()
private_key = dh.generate_private_key()
public_key = dh.generate_public_key(private_key)
bob = BobServer(private_key, public_key)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def send_communication():
    requests.post("http://192.168.10.101:5000/")
    return {"Public_key": bob.get_public_key()}

@app.route("/", methods=["POST"])
def get_communication():
    data = requests.get("http://192.168.10.101:5000/").content
    data = json.loads(data)["Public_key"]
    BobServer.PU_a = data
    return "Hei"

@app.route("/")
def index():
    return "Helloeffv"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')