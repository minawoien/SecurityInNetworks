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
    bbs = BBS(shared_key)
    BobServer.secret_key = bbs.generate_key(16*8)
    
message = ""
app = Flask(__name__)

@app.route("/getmsg", methods=["POST"])
def get_msg():
    data = request.get_json()
    # Covert back to bytes
    data = eval(data["msg"])
    BobServer.message = sym_ciph.decrypt(data, BobServer.secret_key)
    return redirect(url_for("index"))

@app.route("/sendmsga", methods=["POST", "GET"])
def send_message():
    message = (request.form.get("message"))
    encrypted_msg = sym_ciph.encrypt(bytes(message, "UTF-8"), BobServer.secret_key)
    requests.post("http://localhost:8080/getmsga", json={"msg": str(encrypted_msg)})
    return render_template('indexB.html', msg=None, established="True")

@app.route("/sendpua", methods=["GET"])
def send_communication():
    return {"Public_key": bob.get_public_key()}

@app.route("/getpua", methods=["POST"])
def get_communication():
    data = requests.get("http://localhost:8080/sendpub").content
    data = json.loads(data)["Public_key"]
    BobServer.PU_a = data
    return redirect(url_for("index"))

@app.route("/")
def index():
    if BobServer.message != "":
        return render_template("indexB.html", msg=BobServer.message, established="True")
    elif BobServer.PU_a != -1:
        generate_secret()
        return render_template("indexB.html", msg=None, established="True")
    return render_template("indexB.html", msg=None, established=None)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')