from secure_communication import DiffieHellman, Convert

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
    
    def generate_key(self, S, length):
        i = 0
        j = 0
        for i in range(length):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            save = S[i]
            S[i] = S[j]
            S[j] = save
            t = (S[i] + S[j]) % 256
            k = S[t]
        print(k)


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

    # Generate the secret key with the use of RC4
    csprng = CSPRNG(dh.generate_shared_key(pr_a))
    csprng.convert_to_bytes()
    S = csprng.generate_state_vector()
    state_vector = csprng.convert_to_int(S)
    print("State vector: ", state_vector)
    print("Secret key: ", csprng.generate_key(state_vector, 10))