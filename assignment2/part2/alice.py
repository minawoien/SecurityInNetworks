from crypt import methods
from flask import Flask, request, Response, jsonify
import requests, json

from servers import AliceServer
from secure_communication import *

dh = DiffieHellman()
private_key = dh.generate_private_key()
public_key = dh.generate_public_key(private_key)
alice = AliceServer(private_key, public_key)

def checkConnection():
    if AliceServer.PU_b is not -1:
        print("Communication Established")
        shared_key = dh.generate_shared_key(private_key, AliceServer.PU_b)
        bbs = BBS(shared_key)
        secret_key = bbs.generate_key(16*8)
        message = input("Write message:")
        print(message)


app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_communication():
    data = requests.get("http://192.168.10.102:5001/").content
    data = json.loads(data)["Public_key"]
    AliceServer.PU_b = data
    print("Data pk:", AliceServer.PU_b)
    checkConnection()
    return "Hihi"

@app.route("/", methods=["GET"])
def send_communication():
    requests.post("http://192.168.10.102:5001/")
    return {"Public_key": alice.get_public_key()}

@app.route("/", methods=["GET"])
def index():
    return "Hello"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')