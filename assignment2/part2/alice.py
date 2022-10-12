from flask import Flask, redirect, url_for, render_template, request
import requests, json

from servers import AliceServer
from secure_communication import *

# Generate the private key
# Use the private key to generate the public key and store them in the AliceServer class
dh = DiffieHellman()
private_key = dh.generate_private_key()
public_key = dh.generate_public_key(private_key)
alice = AliceServer(private_key, public_key)
sym_ciph = SymmetricCipher()

# Generate the shared key with the use of Alice's private key and Bob's public key
# Uses the shared key to generate the secret key with a length of 16 bytes as AES cipher require a key
# with the length of 16 bytes.
# Saves the secret key in the AliceServer class
def generate_secret():
    shared_key = dh.generate_shared_key(private_key, AliceServer.PU_b)
    bbs = BBS(shared_key)
    AliceServer.secret_key = bbs.generate_key(16*8)
    

app = Flask(__name__)

# Get called when Alice clicks on the send button
# Get the message from the form and encrypt it using the AES cipher and the secret key
# Sends a post request to Bob with the encrypted message as string in json format
# Return to index
@app.route("/sendmsg", methods=["POST", "GET"])
def send_message():
    message = (request.form.get("message"))
    if message == "":
        err = "Message can not be empty."
        return render_template('indexA.html', title="Message failed", establish="True", msg=None, error=err)
    encrypted_msg = sym_ciph.encrypt(bytes(message, "UTF-8"), AliceServer.secret_key)
    requests.post("http://localhost:5000/getmsg", json={"msg": str(encrypted_msg)})
    return render_template('indexA.html', title="Message sent", establish="True", msg=None, error=None)

# Get called when Alice receives a post request from Bob
# Get the encrypted message from json and convert it back to bytes
# Decrypt the message using the AES cipher and the secret key
# Redirect to index
@app.route("/getmsga", methods=["POST"])
def get_msg():
    data = request.get_json()
    # Covert back to bytes
    data = eval(data["msg"])
    AliceServer.message = sym_ciph.decrypt(data, AliceServer.secret_key)
    return redirect(url_for("index"))

# Runs when the establish button is clicked
# Requests Bob's public key and store it in the AliceServer class as a global variable
# Redirect to index
@app.route("/getpub", methods=["POST"])
def get_communication():
    data = requests.get("http://localhost:5000/sendpua").content
    data = json.loads(data)["Public_key"]
    AliceServer.PU_b = data
    return redirect(url_for("index"))

# Get called when Bob request Alice's public key
# Returns Alice's public key
@app.route("/sendpub", methods=["GET"])
def send_communication():
    return {"Public_key": alice.get_public_key()}

# If Alice have received a message, the message will be shown at the index page
# If Alice have received Bob's public key, Alice will be able to send a message to Bob
# Otherwise Alice are able to establish connection with Bob
@app.route("/", methods=["GET"])
def index():
    if AliceServer.message != "":
        return render_template("indexA.html", title="Connection established", establish="True", msg=AliceServer.message, error=None)
    elif AliceServer.PU_b != -1:
        generate_secret()
        return render_template('indexA.html', title="Connection established", establish="True", msg=None, error=None)
    return render_template('indexA.html', title="Welcome Alice", establish=None, msg=None, error=None)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')