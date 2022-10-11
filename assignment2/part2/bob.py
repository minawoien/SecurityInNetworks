from flask import Flask, render_template
import requests, json

from servers import BobServer
from secure_communication import *

dh = DiffieHellman()
private_key = dh.generate_private_key()
public_key = dh.generate_public_key(private_key)
bob = BobServer(private_key, public_key)


def checkConnection():
    if BobServer.PU_a is not -1:
        print("Communication Established")
        shared_key = dh.generate_shared_key(private_key, BobServer.PU_a)
        bbs = BBS(shared_key)
        secret_key = bbs.generate_key(16*8)
        print(secret_key)
        

app = Flask(__name__)

@app.route("/send", methods=["GET"])
def send():
    print("heieheiei")
    return "Bob's Send page"


@app.route("/sendpua", methods=["GET"])
def send_communication():
    return {"Public_key": bob.get_public_key()}

@app.route("/getpua", methods=["POST"])
def get_communication():
    data = requests.get("http://localhost:8080/sendpub").content
    data = json.loads(data)["Public_key"]
    BobServer.PU_a = data
    checkConnection()
    return "Hei"

@app.route("/")
def index():
    return render_template("base_bob.html")

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')