import random

class Convert:
    def __init__(self):
        self.values =  {'0': 0, '1': 1, '2': 2, '3': 3,
                        '4': 4, '5': 5, '6': 6, '7': 7,
                        '8': 8, '9': 9, 'A': 10, 'B': 11,
                        'C': 12, 'D': 13, 'E': 14, 'F': 15}
        
    def hexa_to_decimal(self, hexadecimal):
        decimal = 0
        size = len(hexadecimal) - 1
        for num in hexadecimal:
            decimal = decimal + self.values[num]*16**size
            size = size - 1
        return decimal

class DiffieHellman:
    def __init__(self, prime):
        # Uses the chosen Sophie Germain prime to calculate a safe prime
        self.prime = prime
        self.safe_prime = 2*self.prime + 1
        self.generator = 2
        self.PU_a = -1
        self.PU_b = -1

    # Generate a random private key that is less than the safe prime
    def generate_private_key(self):
        return random.randint(0, self.safe_prime-1)

    # Generate public keys for Alice and Bob. Check their name to check if it is Alice or Bob's public key
    # that are going to be stored public 
    def generate_public_key(self, private_key, name):
        public_key = (self.generator ** private_key) % self.safe_prime
        if name == "a":
            self.PU_a = public_key
        else:
            self.PU_b = public_key
    
    # Generate a shared key, check their names to find which public key to use
    # (Eventually the public key could be returned and use the key that are different, what is better?)
    def generate_shared_key(self, private_key, name):
        if name == "a":
            return (self.PU_b**private_key) % self.safe_prime
        else:
            return (self.PU_a**private_key) % self.safe_prime


if __name__ == "__main__":
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