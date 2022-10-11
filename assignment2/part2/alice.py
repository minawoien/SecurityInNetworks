from crypt import methods
from urllib import request
from flask import Flask, redirect, url_for, render_template, request
import requests, json

from servers import AliceServer
from secure_communication import *

dh = DiffieHellman()
private_key = dh.generate_private_key()
public_key = dh.generate_public_key(private_key)
alice = AliceServer(private_key, public_key)

def checkConnection(message):
    print("Communication Established")
    shared_key = dh.generate_shared_key(private_key, AliceServer.PU_b)
    bbs = BBS(shared_key)
    secret_key = bbs.generate_key(16*8)
    sym_ciph = SymmetricCipher()
    message = bytes(message, "UTF-8")
    return sym_ciph.encrypt(message, secret_key)


app = Flask(__name__)

@app.route("/send", methods=["POST"])
def send():
    if request.method == "POST":
        message = (request.form.get("message"))
        cipher_message = checkConnection(message)
        print(cipher_message)
    return render_template('message.html', title="sent")


@app.route("/getpub", methods=["POST"])
def get_communication():
    data = requests.get("http://localhost:5000/sendpua").content
    data = json.loads(data)["Public_key"]
    AliceServer.PU_b = data
    print("Data pk:", AliceServer.PU_b)
    return redirect(url_for("index"))

@app.route("/sendpub", methods=["GET"])
def send_communication():
    return {"Public_key": alice.get_public_key()}

@app.route("/", methods=["GET"])
def index():
    var = "Welcome"
    if AliceServer.PU_b != -1:
        var = "Connection established"
        return render_template('message.html', title=var)
    return render_template('base_alice.html', title=var)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')