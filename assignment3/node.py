from time import sleep
from flask import Flask, request, redirect, url_for
from argparse import ArgumentParser
from hashtable import HashTable
import requests

app = Flask(__name__)

hash = HashTable()

@app.route("/")
def index():
    return "Hello world"

# Receive the address of a node on the network, check if it is in its own hash table and adds it
@app.route("/est", methods=["POST"])
def establish_con():
    data = request.get_json()
    print(data)
    address = data['msg']
    print(hash.hashTable)
    hash.check_address(address)
    return str(len(hash.hashTable))

# Connect with the remote host and sends its own address
def connect(port):
    response = requests.post(f"http://127.0.0.1:{port}/est", json={"msg": hash.host, "count":len(hash.hashTable)})
    url = response.url
    first = url.find("/") + 2
    end = first + url[first:].find("/")
    hash.check_address(url[first:end])
    print(hash.hashTable)
    print("Response sin count i hash tabellen:", int(response.text))
    print("Min hash tabell:", len(hash.hashTable))
    # Videre: hvis ulikt tall, må få bedt om den siste

if __name__ == "__main__":
    # Insert the sockets
    parser = ArgumentParser()
    parser.add_argument('-host')
    parser.add_argument('-r')
    args = parser.parse_args()

    # Split the socket into host and port, and add it to the hash table
    host = args.host.split(":")
    hash.host = args.host
    hash.set_address(args.host, host[1])

    # If an remote socket is added as parameter, the socket is splitted into socket and port and added to the hash table
    # Then the host will connect with the remote host
    if args.r is not None:
        remote = args.r.split(":")
        hash.set_address(args.r, remote[1])
        connect(remote[1])
    app.run(debug=True, host=host[0], port=host[1])




