from time import sleep
from urllib import response
from flask import Flask, request, redirect, url_for
from argparse import ArgumentParser
from routing import RoutingTable
import requests

app = Flask(__name__)

routing = RoutingTable()

@app.route("/")
def index():
    return "Hello world"

# Receive the address of a node on the network, check if it is in its own routing table and adds it
@app.route("/est", methods=["POST"])
def establish_con():
    data = request.get_json()
    address = data['msg']
    print(routing.routing_to_address)
    routing.check_address(address)
    return str(len(routing.routing_to_address))

# Connect with the remote host and sends its own address
def connect(port):
    response = requests.post(f"http://127.0.0.1:{port}/est", json={"msg": routing.host, "count":len(routing.routing_to_address)})
    url = response.url
    first = url.find("/") + 2
    end = first + url[first:].find("/")
    routing.check_address(url[first:end])
    print(routing.routing_to_address)
    print("Response sin count i routing tabellen:", int(response.text))
    print("Min routing tabell:", len(routing.routing_to_address))
    # Videre: hvis ulikt tall, må få bedt om den siste


if __name__ == "__main__":
    # Insert the sockets
    parser = ArgumentParser()
    parser.add_argument('-host')
    parser.add_argument('-r')
    args = parser.parse_args()

    # Split the socket into host and port, and add it to the routing table
    host = args.host.split(":")
    routing.host = args.host
    routing.set_address(args.host, host[1])

    # If an remote socket is added as parameter, the socket is splitted into socket and port and added to the routing table
    # Then the host will connect with the remote host
    if args.r is not None:
        remote = args.r.split(":")
        routing.set_address(args.r, remote[1])
        connect(remote[1])

    app.run(debug=True, host=host[0], port=host[1])


