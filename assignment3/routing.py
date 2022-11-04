from multiprocessing import Manager

class RoutingTable:
    def __init__(self):
        self.host = None
        self.guid = None
        m = Manager()
        self.routing_to_address = m.dict()
        self.routing_to_ID = m.dict()
    
    # Set the guid and address in the routing table with guid as key
    def set_address(self, guid, address):
        self.routing_to_address[guid] = address
    
    # Set the guid and address in the routing table with address as key
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
    # Delete the node from the routing table as the host did not get a response at the heartbeat
    def process_heartbeat(self, address):
        guid = self.routing_to_ID[address]
        del self.routing_to_ID[address]
        del self.routing_to_address[guid]

    # Return the address of a node given the ID
    def get_address(self, guid):
        print(guid)
        return self.routing_to_address[guid]