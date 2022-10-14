import random
from Cryptodome.Cipher import AES

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
        return {"Safe prime:": self.safe_prime, "Prime: ": self.prime, "Generator: ": self.generator}

    # Generate a random private key that is less than the safe prime
    def generate_private_key(self):
        return random.randint(0, self.safe_prime-1)

    # Generate public keys for Alice and Bob.
    def generate_public_key(self, private_key):
        return pow(self.generator, private_key, self.safe_prime)
    
    # Generate a shared key
    def generate_shared_key(self, private_key, public_key):
        return pow(public_key, private_key, self.safe_prime)


# Class for cryptographically strong pseudo-random number generator (CSPRNG)
# Using the Blum Blum Shub generator to generate a random secret key
# Takes the shared key as an incoming seed
class BBS:
    def __init__(self, seed):
        self.n = 0
        self.seed = seed
        self.generate_primes()

    # Generate two large primes, q and p, that both have a remainder 3 when divided by 4
    # Generate n which is relative prime to the seed and is the product of p and q
    def generate_primes(self):
        p = 71
        q = 139
        self.n = p * q 

    # Generate the secret key with an incoming set length
    # Produces a sequence of bits with type string and convert the string to bytes
    def generate_key(self, length):
        print(self.n)
        B = ""
        x = [self.seed**2 % self.n]
        for i in range(1, length+1):
            x.append(x[i-1]**2 % self.n)
            B += str(x[i] % 2)
        return bytes(int(B[i : i + 8], 2) for i in range(0, len(B), 8))


# Class for symmetric cipher, the AES
class SymmetricCipher:
    # Encrypt the incoming message with the incoming secret key
    # Uses the builtin function AES with EAX mode
    # Adds the nonce to the beginning of the ciphertext
    # Returns the nonce and ciphertext together
    def encrypt(self, message, key):
        cipher = AES.new(key, AES.MODE_CTR)
        ciphertext = cipher.encrypt(message)
        result = cipher.nonce + ciphertext
        return result

    # Set the nonce as the 8 first bytes of the ciphertext and the remaining as the ciphertext
    # Decrypt the incoming ciphertext with the incoming secret key
    # Uses the builtin function AES with EAX mode
    # Return the plaintext
    def decrypt(self, ciphertext, key):
        cipher_nonce = ciphertext[:8]
        ciphertext = ciphertext[8:]
        cipher = AES.new(key, AES.MODE_CTR, nonce=cipher_nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.decode("UTF-8")
