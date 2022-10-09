from crypt import methods
from flask import Flask, request, Response, jsonify
import requests, json

from secure_communication import *

    #print(dh.generate_shared_key(alice.PR_a, AliceServer.PU_b))

dh = DiffieHellman()
private_key = dh.generate_private_key()
public_key = dh.generate_public_key(private_key)
alice = AliceServer(private_key, public_key)

app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_communication():
    data = requests.get("http://192.168.10.101:5001/").content
    data = json.loads(data)["Public_key"]
    AliceServer.PU_b = data
    print("Data pk:", AliceServer.PU_b)
    return "Hihi"

@app.route("/", methods=["GET"])
def send_communication():
    requests.post("http://192.168.10.101:5001/")
    return {"Public_key": alice.get_public_key()}

@app.route("/", methods=["GET"])
def index():
    return "Hello"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')