import hashlib
from multiprocessing import Manager

class HashTable:
    def __init__(self):
        m = Manager()
        self.hashTable = m.dict()
    
    # Add a node to the hash table with it's public key, the filename and hash
    # If the node already have a file in the hash table, the filename and hash will be added to the same row
    def add(self, guid, pu_k, hash, filename):
        if guid not in self.hashTable:
            self.hashTable[guid] = (pu_k, {filename: hash})
        else:
            pk,files = self.hashTable[guid]
            files[filename]= hash
            self.hashTable[guid] = (pk,files)

    
    # Update hash table when the hash table of another node is received
    def update_table(self, table):
        for guid in table:
            pu_k = table[guid][0]
            files = table[guid][1]
            for filename in files:
                self.add(guid, pu_k, files[filename], filename)

    # Remove a node from the hash table when it leaves the network
    def remove_node(self, guid):
        if guid in self.hashTable.keys():
            del self.hashTable[guid]

    # Create the hash of a file with the SHA 1 hashing algorithm.
    # From 'Python Program to find hash', https://www.programiz.com/python-programming/examples/hash-file, (accessed: 01.11.22)
    def create_hash(self, file):
        h = hashlib.sha1()
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)
        return h.hexdigest()
    
    # Get the public key for a node
    def get_pu_k(self, guid):
        return self.hashTable[guid][0]
