from flask import Flask, request
from task2 import *

# Raw keys stored
house_key = 3
phone_key = "51634782"

app = Flask(__name__)

@app.route("/")
def hello():
    cipher = ""
    try: 
        # Takes the argument from the url and uses the Caesar cipher once, before it uses the column 
        # transposition cipher twice to get the plain text and return it to the page
        cipher = request.args.get("cipher")
        cipher_text = caesar(cipher, house_key)
        text = decrypt_transposition(cipher_text, phone_key)
        clear_text = decrypt_transposition(text, phone_key)
    except:
        clear_text = "Hello World"
    return clear_text

if __name__ == "__main__": 
    app.run(debug=True)