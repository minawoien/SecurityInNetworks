from flask import Flask, render_template, redirect, url_for, request
import requests, json

from servers import BobServer
from secure_communication import *

# Generate the private key
# Use the private key to generate the public key and store them in the BobServer class
dh = DiffieHellman()
private_key = dh.generate_private_key()
public_key = dh.generate_public_key(private_key)
bob = BobServer(private_key, public_key)
sym_ciph = SymmetricCipher()

# Generate the shared key with the use of Bob's private key and Alice's public key
# Uses the shared key to generate the secret key with a length of 16 bytes as AES cipher require a key
# with the length of 16 bytes.
# Saves the secret key in the BobServer class
def generate_secret():
    shared_key = dh.generate_shared_key(private_key, BobServer.PU_a)
    bbs = BBS(shared_key)
    BobServer.secret_key = bbs.generate_key(16*8)
    
app = Flask(__name__)

# Get called when Bob receives a post request from Alice
# Get the encrypted message from json and convert it back to bytes
# Decrypt the message using the AES cipher and the secret key
# Redirect to index
@app.route("/getmsg", methods=["POST"])
def get_msg():
    data = request.get_json()
    # Covert back to bytes
    data = eval(data["msg"])
    BobServer.message = sym_ciph.decrypt(data, BobServer.secret_key)
    return redirect(url_for("index"))

# Get called when Bob clicks on the send button
# Get the message from the form and encrypt it using the AES cipher and the secret key
# Sends a post request to Alice with the encrypted message as string in json format
# Return to index
@app.route("/sendmsga", methods=["POST", "GET"])
def send_message():
    message = (request.form.get("message"))
    encrypted_msg = sym_ciph.encrypt(bytes(message, "UTF-8"), BobServer.secret_key)
    requests.post("http://localhost:8080/getmsga", json={"msg": str(encrypted_msg)})
    return render_template('indexB.html', msg=None, established="True")

# Get called when Alice request Bob's public key
# Returns Bob's public key
@app.route("/sendpua", methods=["GET"])
def send_communication():
    return {"Public_key": bob.get_public_key()}

# Get called when Bob clicks the establish button
# Request Alice's public key and store it in the BobServer class as a global variable
# Redirect to index
@app.route("/getpua", methods=["POST"])
def get_communication():
    data = requests.get("http://localhost:8080/sendpub").content
    data = json.loads(data)["Public_key"]
    BobServer.PU_a = data
    return redirect(url_for("index"))

# If Bob have received a message, the message will be shown at the index page
# If Bob have received Alice's public key, Bob will be able to send a message to Alice
# Otherwise Bob are able to establish connection with Alice
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