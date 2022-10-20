from flask import Flask
from argparse import ArgumentParser

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world"


if __name__ == "__main__":
    # Insert the addresses
    parser = ArgumentParser()
    parser.add_argument('-a')
    args = parser.parse_args()
    arg = args.a
    app.run(debug=True, host='127.0.0.1')