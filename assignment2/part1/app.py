from flask import Flask
from secure_communication import *

app = Flask(__name__)

@app.route("/")
def shared_keys():
    name = input("a or b? ")
    # Sophie germian prime
    prime = """FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 29024E08 8A67CC74 020BBEA6 3B139B22 
            514A0879 8E3404DD EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245 E485B576 625E7EC6 
            F44C42E9 A637ED6B 0BFF5CB6 F406B7ED EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D 
            C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F 83655D23 DCA3AD96 1C62F356 208552BB 
            9ED52907 7096966D 670C354E 4ABC9804 F1746C08 CA237327 FFFFFFFF FFFFFFFF"""
    prime = prime.replace(" ", "").replace("\n", "")
  
    # Convert the germian prime to decimal
    converter = Convert()
    prime_decimal = converter.hexa_to_decimal(prime)
    dh = DiffieHellman(prime_decimal)
    private_key = dh.generate_private_key()
    dh.generate_public_key(private_key, name)
    shared_key = dh.generate_shared_key(private_key, name)
    print(shared_key)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')