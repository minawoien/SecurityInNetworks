from crypt import methods
from flask import Flask, request
from argparse import ArgumentParser
import requests, json

app = Flask(__name__)

addressList = []

def set_addresses(arg):
    addressList = arg.split(",")
    return addressList

@app.route("/")
def index():
    establish_con()
    return "Hello world"

@app.route("/", methods=["POST", "GET"])
def establish_con():
    if len(addressList) > 1:
        requests.post("http://localhost:"+addressList[1], json={"msg": addressList[0]})
    else:
        data = request.get_json()
        print(data)
    return "Hi"


if __name__ == "__main__":
    # Insert the addresses
    parser = ArgumentParser()
    parser.add_argument('-a')
    args = parser.parse_args()
    arg = args.a
    addressList = set_addresses(arg)
    app.run(debug=True, host='127.0.0.1', port=addressList[0])