from multiprocessing import Manager

class RoutingTable:
    def __init__(self):
        self.host = None
        self.guid = None
        m = Manager()
        self.routing_to_address = m.dict()
        self.routing_to_ID = m.dict()
    
    # Set the address to the routing table
    def set_address(self, guid, address):
        self.routing_to_address[guid] = address
    
    def set_guid(self, address, guid):
        self.routing_to_ID[address] = guid

    # Check if the given address is in the routing table
    def check_address(self, guid, address):
        if guid not in self.routing_to_address:
            self.set_address(guid, address)
            self.set_guid(address, guid)
            return address
        return False

    # Process a given heartbeat
    # This function controls which nodes have sent a heartbeat
    def process_heartbeat(self, address):
        guid = self.routing_to_ID[address]
        del self.routing_to_ID[address]
        del self.routing_to_address[guid]

    # Return the ID of a node given the address
    def get_ID(self):
        return self.routing_to_ID

    # Return the address of a node given the ID
    def get_address(self):
        return self.routing_to_address