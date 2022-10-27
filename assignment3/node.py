from crypt import methods
from flask import Flask, request
from argparse import ArgumentParser
import requests, json

app = Flask(__name__)

class HashTable:
    def __init__(self):
        self.host = None
        self.hashTable = {}
    
    def set_address(self, socket, port):
        self.hashTable[socket] = port
    
    def check_address(self, address):
        if address not in self.hashTable:
            address_info = address.split(":")
            self.set_address(address, address_info[1])
            return True
        return False
    

hash = HashTable()
# hashTable = {}

# def set_addresses(socket, port):
#     hashTable[socket] = port

@app.route("/")
def index():
    return "Hello world"

# Receive the address of a node on the network, check if it is in its own hash table and adds it
@app.route("/", methods=["POST", "GET"])
def establish_con():
    data = request.get_json()
    address = data['msg']
    if not hash.check_address(address):
        address_info = address.split(":")
        print(address_info[1])
        connect(address_info[1])
    print(data)
    return "Hi"

# Connect with the remote host and sends its own address
def connect(port):
    requests.post("http://localhost:"+port, json={"msg": hash.host})
    print("done")

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