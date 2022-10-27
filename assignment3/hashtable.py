class HashTable:
    def __init__(self):
        self.host = None
        self.hashTable = {}
    
    def set_address(self, socket, port):
        self.hashTable[socket] = port
    
    def check_address(self, address):
        if address not in self.hashTable:
            address_info = address.split(":")
            self.set_address(address, address_info[1])


