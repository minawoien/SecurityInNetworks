from flask import Flask, request
from argparse import ArgumentParser
from routing import RoutingTable
from hashTable import HashTable
import requests, uuid, json, os
from multiprocessing import Process
from secure_communication import DiffieHellman, SymmetricCipher
from func import connect, updated_dht, generate_secret_key, send_heartbeat
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/")
def index():
    return app.send_static_file("index.html")

# Route to upload file, and save it
# Add it to the hash table and share it with the nodes in the routing table
@app.route("/uploadFile", methods=["POST"])
def upload():
    file = request.files['file']
    try:
        os.mkdir(f"files/{routing.host}")
    except FileExistsError:
        pass
    content = file.read()
    filename = secure_filename(file.filename)
    open(f"files/{routing.host}/{filename}", 'wb').write(content)
    hash = dht.create_hash(file)
    dht.add(routing.uuid, public_key, hash, filename)
    updated_dht(routing, dht)
    return app.send_static_file("index.html")

# Route to request file from the node containing the hash
# Use the uuid of the node to get the address, and requests the file from it's filename
@app.route("/requestFile", methods=["POST"])
def request_file():
    data = request.get_json()
    address = routing.get_address(data['uuid'])
    response = requests.post(f"http://{address}/getFile", json={"filename": data['filename'], "public_key":public_key}).content
    pu_k = dht.get_pu_k(data['uuid'])
    secret_key = generate_secret_key(pu_k, private_key, dh)
    received_file = cipher.decrypt(response, secret_key)
    try:
        os.mkdir(f"files/{routing.host}")
    except FileExistsError:
        pass
    with open(f'files/{routing.host}/{data["filename"]}', "wb") as file:
        file.write(received_file)
    with open(f'files/{routing.host}/{data["filename"]}', "rb") as file:
        hash = dht.create_hash(file)
    dht.add(routing.uuid, public_key, hash, data["filename"])
    updated_dht(routing, dht)
    return app.send_static_file("index.html")

# Route to send file to the requesting node, receive public key from requesting node
@app.route("/getFile", methods=["POST"])
def getFile():
    filename = request.get_json()['filename']
    received_pu_k = request.get_json()['public_key']
    secret_key = generate_secret_key(received_pu_k, private_key, dh)
    with open(f'files/{routing.host}/{filename}', "rb") as file:
        text = file.read()
    encrypted_file = cipher.encrypt(text, secret_key)
    return encrypted_file

# Route to update the DHT
@app.route("/getdht", methods=["POST"])
def get_dht():
    data = request.get_json()['file']
    dht.update_table(data)
    return routing.host

# Route to routing table 
@app.route("/getNodes", methods=["GET"])
def getNodes():
    return json.dumps(routing.routing_to_address.copy())

# Route to hash table
@app.route("/getHashTable", methods=["GET"])
def getHashTable():
    return json.dumps(dht.hashTable.copy())

# Receive the address of a node on the network, check if it is in its own routing table and adds it
@app.route("/est", methods=["POST"])
def establish_con():
    data = request.get_json()
    routing.check_address(data["uuid"], data["address"])
    return routing.uuid

# Route to heartbeat
@app.route("/heartbeat", methods=["GET"])
def receive_heartbeat():
    return "ok"

if __name__ == "__main__":
    routing = RoutingTable()
    dht = HashTable()
    cipher = SymmetricCipher()

    # Insert the host and a remote host
    # from Stackoverflow, "How to pass an arbitrary argument to flask through app.run()?",
    # https://stackoverflow.com/questions/48346025/how-to-pass-an-arbitrary-argument-to-flask-through-app-run, 
    # Mar 27, 2019. (accessed: Okt 20, 2022).
    parser = ArgumentParser()
    parser.add_argument('-host')
    parser.add_argument('-r')
    args = parser.parse_args()

    # Create a random UUID and add it with the address to the routing table
    uuid = str(uuid.uuid4())
    routing.uuid = uuid
    routing.host = args.host
    routing.set_address(uuid, args.host)
    routing.set_uuid(args.host, uuid)

    # If a remote host is added as parameter, the host will try to connect with the remote host
    if args.r is not None:
        connect(args.r, routing, dht)
    host = args.host.split(":")

    # Create private and public key for file sharing with the use of Diffie Hellman
    dh = DiffieHellman()
    private_key = dh.generate_private_key()
    public_key = dh.generate_public_key(private_key)

    # Start a process that runs in the background
    # This process runs the function send_heartbeat to send heartbeats to each node in a given time interval
    # It takes in the routing and DHT class to know when the tables have changed
    p = Process(target=send_heartbeat, args=(routing, dht, ))
    p.start()
    app.run(host=host[0], port=host[1])
    p.terminate()

