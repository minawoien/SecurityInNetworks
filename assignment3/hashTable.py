import hashlib
from multiprocessing import Manager

class HashTable:
    def __init__(self):
        m = Manager()
        self.hashTable = m.dict()
    
    # Add a node to the hash table with it's public key, the filename and hash
    def add(self, guid, pu_k, hash, filename):
        if guid not in self.hashTable:
            self.hashTable[guid] = (pu_k, {filename: hash})
        else:
            self.hashTable[guid][1][filename] = hash
    
    # Update hash table when the hash table of another node is received
    def update_table(self, table):
        for guid in table:
            pu_k = table[guid][0]
            files = table[guid][1]
            for filename in files:
                self.add(guid, pu_k, files[filename], filename)

    # Remove a node from the hash table when it leaves the network
    def remove_node(self, guid):
        del self.hashTable[guid]

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
