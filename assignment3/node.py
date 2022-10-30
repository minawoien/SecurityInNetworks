from flask import Flask, request
from argparse import ArgumentParser
from routing import RoutingTable
import requests
import uuid
import json

app = Flask(__name__)

routing = RoutingTable()

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/uploadFile")
def upload():
    print("Hello")
    return app.send_static_file("index.html")

@app.route("/getNodes", methods=["GET"])
def getNodes():
    print("Getting")
    return json.dumps(routing.routing_to_address)

# Receive the address of a node on the network, check if it is in its own routing table and adds it
@app.route("/est", methods=["POST"])
def establish_con():
    data = request.get_json()
    routing.check_address(data["guid"], data["address"])
    for i in routing.routing_to_ID:
        print(i)
    return routing.guid

@app.route("/routingTable", methods=["GET"])
def get_routingTable():
    return routing.routing_to_address

# Connect with the remote host and sends its own address
def connect(address):
    response = requests.post(f"http://{address}/est", json={"address": routing.host, "guid": routing.guid})
    url = response.url
    first = url.find("/") + 2
    end = first + url[first:].find("/")
    routing.check_address(response.text, url[first:end])
    get_all(address)

def get_all(address):
    routing_table = requests.get(f"http://{address}/routingTable").content
    routing_table = json.loads(routing_table)
    for guid in routing_table:
        new_address = routing.check_address(guid, routing_table[guid])
        if new_address:
            requests.post(f"http://{new_address}/est", json={"address": routing.host, "guid": routing.guid})
    for i in routing.routing_to_ID:
        print(i)
   
if __name__ == "__main__":
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
    app.run(host=host[0], port=host[1])


