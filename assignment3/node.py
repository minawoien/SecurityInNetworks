from flask import Flask, request
from argparse import ArgumentParser
from routing import RoutingTable
import requests
import uuid

app = Flask(__name__)

routing = RoutingTable()

@app.route("/")
def index():
    return "Hello world"

# Receive the address of a node on the network, check if it is in its own routing table and adds it
@app.route("/est", methods=["POST"])
def establish_con():
    data = request.get_json()
    routing.check_address(data["guid"], data["address"])
    print("table", routing.routing_to_address)
    print("other", routing.routing_to_ID)
    return routing.guid

# Connect with the remote host and sends its own address
def connect(address, guid):
    response = requests.post(f"http://{address}/est", json={"address": routing.host, "guid": guid})
    url = response.url
    first = url.find("/") + 2
    end = first + url[first:].find("/")
    routing.check_address(response.text, url[first:end])
    print("table", routing.routing_to_address)
    print("other", routing.routing_to_ID)
   
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
        connect(args.r, guid)
    host = args.host.split(":")
    app.run(host=host[0], port=host[1])


