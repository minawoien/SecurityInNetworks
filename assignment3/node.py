from crypt import methods
import time
from flask import Flask, request
from argparse import ArgumentParser
from routing import RoutingTable
from hashTable import HashTable
import requests
import uuid
import json
from multiprocessing import Process

app = Flask(__name__)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/uploadFile", methods=["POST"])
def upload():
    file = request.files['file']
    hash = dht.create_hash(file)
    dht.add(routing.guid, routing.host, hash, file.filename)
    updated_dht()
    return app.send_static_file("index.html")

@app.route("/getdht", methods=["POST"])
def get_dht():
    data = request.get_json()
    print(data)
    return routing.host

@app.route("/getNodes", methods=["GET"])
def getNodes():
    return json.dumps(routing.routing_to_address.copy())

@app.route("/getHashTable", methods=["GET"])
def getHashTable():
    return json.dumps(dht.hashTable)

# Receive the address of a node on the network, check if it is in its own routing table and adds it
@app.route("/est", methods=["POST"])
def establish_con():
    data = request.get_json()
    routing.check_address(data["guid"], data["address"])
    for i in routing.routing_to_ID.keys():
        print(i)
    return routing.guid

@app.route("/heartbeat", methods=["GET"])
def receive_heartbeat():
    return "ok"

# Connect with the remote host and sends its own address
def connect(address):
    response = requests.post(f"http://{address}/est", json={"address": routing.host, "guid": routing.guid})
    url = response.url
    first = url.find("/") + 2
    end = first + url[first:].find("/")
    routing.check_address(response.text, url[first:end])
    share_tables(address)

def share_tables(address):
    routing_table = requests.get(f"http://{address}/getNodes").content
    routing_table = json.loads(routing_table)
    for guid in routing_table:
        new_address = routing.check_address(guid, routing_table[guid])
        if new_address:
            requests.post(f"http://{new_address}/est", json={"address": routing.host, "guid": routing.guid})
    for i in routing.routing_to_ID.keys():
        print(i)

def updated_dht():
    for address in routing.routing_to_ID.keys():
        if address != routing.host:
            requests.post(f"http://{address}/getdht", json={"file": dht.hashTable})

# Send a heartbeat at a set time interval
def send_heartbeat(routing):
    while True:
        for address in routing.routing_to_ID.keys():
            if address != routing.host:
                try:
                    response = requests.get(f"http://{address}/heartbeat").content
                    print(response)
                except:
                    print("connection failed")
                    routing.process_heartbeat(address)
        time.sleep(10)

if __name__ == "__main__":
    routing = RoutingTable()
    dht = HashTable()

    # Insert the sockets
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

    p = Process(target=send_heartbeat, args=(routing, ))
    p.start()
    app.run(host=host[0], port=host[1])
    p.terminate()

