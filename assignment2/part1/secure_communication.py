import random
from Cryptodome.Cipher import AES
import math

# Class to convert Hexadecimal to decimal
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
    def __init__(self):
        self.converter = Convert()
        # Uses the chosen Sophie Germain prime to calculate a safe prime
        self.prime =  """FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 29024E08 8A67CC74 020BBEA6 3B139B22 
            514A0879 8E3404DD EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245 E485B576 625E7EC6 
            F44C42E9 A637ED6B 0BFF5CB6 F406B7ED EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D 
            C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F 83655D23 DCA3AD96 1C62F356 208552BB 
            9ED52907 7096966D 670C354E 4ABC9804 F1746C08 CA237327 FFFFFFFF FFFFFFFF"""
        self.safe_prime = 0
        self.generator = 2
        self.PU_a = -1
        self.PU_b = -1
        self.convert_prime()
    
    # Convert the Sophie Germain prime from hexadecimal to decimal and uses it to calculate the safe prime
    # Get called at the beginning
    def convert_prime(self):
        self.prime = self.prime.replace(" ", "").replace("\n", "")
        self.prime = self.converter.hexa_to_decimal(self.prime)
        self.safe_prime = 2*self.prime + 1
    
    # Returns the shared parameters including the Sophie Germain prime
    def get_parameters(self):
        return {"Safe prime: ": self.safe_prime, "Prime: ": self.prime, "Generator: ": self.generator}

    # Generate a random private key that is less than the safe prime
    def generate_private_key(self):
        return random.randint(0, self.safe_prime-1)

    # Generate public keys for Alice and Bob. If Alice's key is not set, we set it, otherwise Bob's private
    # key is set.
    def generate_public_key(self, private_key):
        pu = pow(self.generator, private_key, self.safe_prime)
        #pu = (self.generator ** private_key)% self.safe_prime
        if self.PU_a == -1:
            self.PU_a = pu
        else:
            self.PU_b = pu
        return pu
    
    # Generate a shared key
    # To chose which public key to use, we generate the public key with the use of the incoming private key
    # to check if it is equal to Alice's public key, and if it is we use Bob's public key to generate the
    # shared key, otherwise Alice's public key
    def generate_shared_key(self, private_key):
        if self.PU_a == pow(self.generator, private_key, self.safe_prime):
            return pow(self.PU_b, private_key, self.safe_prime)
        return pow(self.PU_a, private_key, self.safe_prime)


# Class for cryptographically strong pseudo-random number generator (CSPRNG)
# Using the Blum Blum Shub generator to generate a random secret key
# Takes the shared key as an incoming seed
class BBS:
    def __init__(self, seed):
        self.n = 0
        self.seed = seed
        self.generate_primes()

    # Generate two large primes, q and p, with random, that both have a remainder 3 when divided by 4
    # Generate n which is relative prime to the seed and is the product of p and q
    # The function runs until these requirements are fulfilled
    def generate_primes(self):
        while math.gcd(self.seed, self.n) != 1:
            q = 4 * random.randint(0,100) + 3
            p = 4 * random.randint(0,100) + 3
            self.n = p * q

    # Generate the secret key with an incoming set length
    # Produces a sequence of bits with type string and convert the string to bytes
    def generate_key(self, length):
        B = ""
        x = [self.seed**2 % self.n]
        for i in range(1, length+1):
            x.append(x[i-1]**2 % self.n)
            B += str(x[i] % 2)
        return bytes(int(B[i : i + 8], 2) for i in range(0, len(B), 8))


# Class for symmetric cipher, the AES
# Create stored values for tag and nonce
class SymmetricCipher:
    def __init__(self):
        self.nonce = b""

    # Encrypt the incoming message with the incoming secret key
    # Uses the builtin function AES with EAX mode
    # Store the nonce and return the encrypted message
    def encrypt(self, message, key):
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext = cipher.encrypt(message)
        self.nonce = cipher.nonce
        return ciphertext

    # Decrypt the incoming ciphertext with the incoming secret key
    # Uses the builtin function AES with EAX mode
    # Uses the stored nonce, and return the plaintext
    def decrypt(self, ciphertext, key):
        cipher = AES.new(key, AES.MODE_EAX, self.nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext


if __name__ == "__main__":
    dh = DiffieHellman()
    # Display the cyclic group and public parameters
    parameters = dh.get_parameters()
    for i in parameters:
        print(f"{i}{parameters[i]}")

    
    # Display public key for Alice and Bob
    # Generate private keys for Alice and Bob which they will use to generate public keys
    pr_a = dh.generate_private_key()
    pr_b = dh.generate_private_key()

    # Use their private key to generate public keys
    print("Alice public key: ", dh.generate_public_key(pr_a))
    print("Bob public key: ", dh.generate_public_key(pr_b))

    # Display the shared key
    shared_key = dh.generate_shared_key(pr_a)
    if shared_key == dh.generate_shared_key(pr_b):
        print("Shared key: ", shared_key)
    else:
        print("Something went wrong")

    # Generate a secret key that will be used for encryption and decryption
    # The secret key has en given length of 16 bytes, as the AES with EAX mode require a length of 16 bytes
    bbs = BBS(shared_key)
    secret_key = bbs.generate_key(16*8)
    print("Secret key: ", secret_key)

    # Take input from Alice for encryption and convert it to bytes
    #message = "Hello, this is a secret text"
    message = input("Write your message to Bob: ")
    print("Alice's message: ", message)

    message = bytes(message, "UTF-8")

    # Uses the symmetric cipher to encrypt the message
    sym_ciph = SymmetricCipher()
    ciphertext = sym_ciph.encrypt(message, secret_key)
    print("Encrypted message: ", ciphertext)

    # Uses the symmetric cipher to decrypt the message and convert it to string
    plaintext = sym_ciph.decrypt(ciphertext, secret_key)
    plaintext = str(plaintext, "UTF-8")
    print("Decrypted message: ", plaintext)

