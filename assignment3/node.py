import time
from flask import Flask, request
from argparse import ArgumentParser
from routing import RoutingTable
from hashTable import HashTable
import requests
import uuid
import json
from multiprocessing import Process
from secure_communication import DiffieHellman, BBS, SymmetricCipher
import os

app = Flask(__name__)

@app.route("/")
def index():
    return app.send_static_file("index.html")

# Route to upload file, and save it
# Add it to the hash table and share it with the nodes in the routing table
@app.route("/uploadFile", methods=["POST"])
def upload():
    file = request.files['file']
    # Endre til guid
    os.mkdir(routing.host)
    content = file.read()
    open(f"files/{routing.host}/{file.filename}", 'wb').write(content)
    hash = dht.create_hash(file)
    dht.add(routing.guid, routing.host, hash, file.filename)
    updated_dht()
    return app.send_static_file("index.html")

# Route to request file from the node containing the hash
# Use the guid of the node to get the address, and requests the file from it's filename
@app.route("/requestFile", methods=["POST"])
def request_file():
    data = request.get_json()
    address = routing.get_address(data['guid'])
    response = requests.post(f"http://{address}/getFile", json={"filename": data['filename']})
    return app.send_static_file("index.html")

# Route to send file to the requesting node
@app.route("/getFile", methods=["POST"])
def getFile():
    filename = request.get_json()['filename']
    dht.find_file(filename, routing.guid)
    return "Hello"

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
    routing.check_address(data["guid"], data["address"])
    return routing.guid

# Route to heartbeat
@app.route("/heartbeat", methods=["GET"])
def receive_heartbeat():
    return "ok"

# Connect with the remote host and sends its own address
# Add the remote host to the routing table
def connect(address):
    response = requests.post(f"http://{address}/est", json={"address": routing.host, "guid": routing.guid})
    url = response.url
    first = url.find("/") + 2
    end = first + url[first:].find("/")
    routing.check_address(response.text, url[first:end])
    share_table(address)
    request_hash_table(address)

# Get the routing table of the remote host and share it with every node in the host's routing table
def share_table(address):
    table = requests.get(f"http://{address}/getNodes").content
    table = json.loads(table)
    for guid in table:
        new_address = routing.check_address(guid, table[guid])
        if new_address:
            requests.post(f"http://{new_address}/est", json={"address": routing.host, "guid": routing.guid})

# Request the hash table from the remote host nodes
def request_hash_table(address):
    table = requests.get(f"http://{address}/getHashTable").content
    table = json.loads(table)
    dht.update_table(table)       

def updated_dht():
    for address in routing.routing_to_ID.keys():
        if address != routing.host:
            requests.post(f"http://{address}/getdht", json={"file": dht.hashTable.copy()})


# Send a heartbeat to each node in the host's routing table at a set time interval
def send_heartbeat(routing, dht):
    while True:
        for address in routing.routing_to_ID.keys():
            if address != routing.host:
                try:
                    response = requests.get(f"http://{address}/heartbeat").content
                except:
                    dht.remove_node(routing.routing_to_ID[address])
                    routing.process_heartbeat(address)
        time.sleep(10)

if __name__ == "__main__":
    routing = RoutingTable()
    dht = HashTable()

    # Insert the host and a remote host
    parser = ArgumentParser()
    parser.add_argument('-host')
    parser.add_argument('-r')
    args = parser.parse_args()

    # Create a random UUID and add it with the address to the routing table
    guid = str(uuid.uuid4())
    routing.guid = guid
    routing.host = args.host
    routing.set_address(guid, args.host)
    routing.set_guid(args.host, guid)

    # If a remote host is added as parameter, the host will try to connect with the remote host
    if args.r is not None:
        connect(args.r)
    host = args.host.split(":")

    # Start a process that runs in the background
    # This process runs the function send_heartbeat to send heartbeats to each node in a given time interval
    # It takes in the routing class to know when the routing table has changed
    p = Process(target=send_heartbeat, args=(routing, dht, ))
    p.start()
    app.run(host=host[0], port=host[1])
    p.terminate()

