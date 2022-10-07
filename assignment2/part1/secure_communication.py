from distutils.command.upload import upload
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

class BobServer:
    def __init__(self):
        self.PU_a = -1
        self.PU_b = -1

class AliceServer:
    def __init__(self):
        self.PU_a = -1
        self.PU_b = -1

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
    
    def convert_prime(self):
        self.prime = self.prime.replace(" ", "").replace("\n", "")
        self.prime = self.converter.hexa_to_decimal(self.prime)
        self.safe_prime = 2*self.prime + 1
    
    def get_parameters(self):
        return {"Safe prime:": self.safe_prime, "Prime: ": self.prime, "Generator: ": self.generator}

    # Generate a random private key that is less than the safe prime
    def generate_private_key(self):
        #return random.randint(0, self.safe_prime-1)
        return random.randint(0, 100)

    # Generate public keys for Alice and Bob. If Alice's key is not set, we set it, otherwise Bob's private
    # key is set.
    def generate_public_key(self, private_key):
        pu = (self.generator ** private_key)% self.safe_prime
        if self.PU_a == -1:
            self.PU_a = pu
        else:
            self.PU_b = pu
        return pu
    
    # Generate a shared key
    # To chose which public key to use, we generate the public key with the use of the incoming private key
    # to check if it is equal to Alice's key, and then we use Bob's key
    def generate_shared_key(self, private_key):
        if self.PU_a == (self.generator ** private_key)% self.safe_prime:
            return (self.PU_b**private_key) % self.safe_prime
        else:
            return (self.PU_a**private_key) % self.safe_prime


class CSPRNG:
    def __init__(self, shared_key):
        self.seed = shared_key
        self.bytes = []
    
    def convert_to_bytes(self):
        print("\n")
        print(self.seed)
        bits = "{0:08b}".format(self.seed)
        print(bits)
        for i in range(0,len(bits), 8):
            print(bits[i:i+8])
            self.bytes.append(int(bits[i:i+8], 2))
            print(int(bits[i:i+8], 2))
    
    def convert_to_int(self, S):
        key = ""
        for i in range(len(S)):
            key += "{0:08b}".format(S[i])
        return int(key,2)

    def generate_state_vector(self):
        # Create the state vector S and a temporary vector T
        # If the length of the key K is 256 bytes, then K is transferred to T
        # Otherwise, for a key of length keylen bytes, the first keylen elements of T are copied from K, 
        # and then K is repeated as many times as necessary to fill out T
        S = []
        T = []
        for i in range(256):
            S.append((i))
            T.append(self.bytes[i % len(self.bytes)])

        # Initial permutation
        j = 0
        for i in range(256):
            j = (j + S[i] + T[i]) % 256
            save = S[i]
            S[i] = S[j]
            S[j] = save
        return S


if __name__ == "__main__":
    dh = DiffieHellman()
    # Display the cyclic group and public parameters
    parameters = dh.get_parameters()
    for i in parameters:
        print(f"{i}\n{parameters[i]}")
    
    # Display public key for Alice and Bob
    # Generate private keys for Alice and Bob which they will use to generate public keys
    pr_a = dh.generate_private_key()
    pr_b = dh.generate_private_key()

    # Use their private key to generate public keys
    print("Alice public key: ", dh.generate_public_key(pr_a))
    print("Bob public key: ", dh.generate_public_key(pr_b))

    # Display the shared key 
    print("Shared key Alice: \n", dh.generate_shared_key(pr_a))
    print("Shared key Bob: \n", dh.generate_shared_key(pr_b))

    # Generate the secret key with the use of RC4
    csprng = CSPRNG(dh.generate_shared_key(pr_a))
    csprng.convert_to_bytes()
    S = csprng.generate_state_vector()
    secret_key = csprng.convert_to_int(S)
    print("Secret key: \n", secret_key)

    # Take input from Alice for encryption
    file = "text.txt"
    


    print("\ndone")
