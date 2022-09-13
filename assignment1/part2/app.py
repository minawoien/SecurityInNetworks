from flask import Flask, request
from task2 import *

house_key = 3
phone_key = "51634782"

app = Flask(__name__)

@app.route("/")
def hello():
    cipher = ""
    try: 
        cipher = request.args.get("cipher")
        cipher_text = caesar(cipher, house_key)
        clear_text = decrypt_transposition(cipher_text, phone_key)

        print(f"tesing: {clear_text}")
    except:
        clear_text = "Hello World"
    return clear_text

if __name__ == "__main__": 
    app.run(debug=True)