from flask import Flask, render_template, redirect, url_for, request
import requests, json

from servers import BobServer
from secure_communication import *

dh = DiffieHellman()
private_key = dh.generate_private_key()
public_key = dh.generate_public_key(private_key)
bob = BobServer(private_key, public_key)
sym_ciph = SymmetricCipher()

def generate_secret():
    shared_key = dh.generate_shared_key(private_key, BobServer.PU_a)
    print("Shared", shared_key)
    bbs = BBS(shared_key)
    BobServer.secret_key = bbs.generate_key(16*8)
    print(BobServer.secret_key)
    
message = ""
app = Flask(__name__)

@app.route("/getmsg", methods=["POST"])
def get_msg():
    data = request.get_json()
    # Covert back to bytes
    data = eval(data["msg"])
    BobServer.message = sym_ciph.decrypt(data, BobServer.secret_key)
    return redirect(url_for("index"))

@app.route("/sendpua", methods=["GET"])
def send_communication():
    print("Bob", bob.get_public_key())
    return {"Public_key": bob.get_public_key()}

@app.route("/getpua", methods=["POST"])
def get_communication():
    data = requests.get("http://localhost:8080/sendpub").content
    data = json.loads(data)["Public_key"]
    BobServer.PU_a = data
    print("Alice", BobServer.PU_a)
    return redirect(url_for("index"))

@app.route("/")
def index():
    if BobServer.message != "":
        return render_template("indexB.html", msg=BobServer.message)
    elif BobServer.PU_a != -1:
        generate_secret()
        return render_template("indexB.html", msg="established")
    return render_template("indexB.html", msg=None)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')