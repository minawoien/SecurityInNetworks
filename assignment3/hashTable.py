import hashlib

class HashTable:
    def __init__(self):
        self.hashTable = {}
    
    # Add a node to the hash table with it's public key, the filename and hash
    def add(self, guid, pu_k, hash, filename):
        self.hashTable[guid] = (pu_k, {filename: hash})
        print(self.hashTable)

    # Remove a node from the hash table when it leaves the network
    def remove_node(GUID):
        pass

    # Check if a file already is uploaded
    def find_filename(self, filename):
        pass

    # From Python Program to find hash
    def create_hash(self, file):
        h = hashlib.sha1()
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)
        return h.hexdigest()
