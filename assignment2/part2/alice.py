from crypt import methods
from flask import Flask, redirect, url_for, render_template, request
import requests, json

from servers import AliceServer
from secure_communication import *

dh = DiffieHellman()
private_key = dh.generate_private_key()
public_key = dh.generate_public_key(private_key)
alice = AliceServer(private_key, public_key)
sym_ciph = SymmetricCipher()



def generate_secret():
    shared_key = dh.generate_shared_key(private_key, AliceServer.PU_b)
    print("Shared", shared_key)
    bbs = BBS(shared_key)
    AliceServer.secret_key = bbs.generate_key(16*8)
    print(AliceServer.secret_key)
    

app = Flask(__name__)

@app.route("/sendmsg", methods=["POST", "GET"])
def send_message():
    message = (request.form.get("message"))
    print(message)
    encrypted_msg = sym_ciph.encrypt(bytes(message, "UTF-8"), AliceServer.secret_key)
    requests.post("http://localhost:5000/getmsg", json={"msg": str(encrypted_msg)})
    return render_template('indexA.html', title="Message sent", establish=None, msg=None)

@app.route("/getpub", methods=["POST"])
def get_communication():
    data = requests.get("http://localhost:5000/sendpua").content
    data = json.loads(data)["Public_key"]
    AliceServer.PU_b = data
    print("Bob", AliceServer.PU_b)
    return redirect(url_for("index"))

@app.route("/sendpub", methods=["GET"])
def send_communication():
    print("Alice", alice.get_public_key())
    return {"Public_key": alice.get_public_key()}

@app.route("/", methods=["GET"])
def index():
    if AliceServer.PU_b != -1:
        generate_secret()
        return render_template('indexA.html', title="Connection established", establish="True", msg=None)
    return render_template('indexA.html', title="Welcome", establish=None, msg=None)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')