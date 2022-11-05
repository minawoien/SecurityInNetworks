from multiprocessing import Manager

class RoutingTable:
    def __init__(self):
        self.host = None
        self.uuid = None
        m = Manager()
        self.routing_to_address = m.dict()
        self.routing_to_ID = m.dict()
    
    # Set the uuid and address in the routing table with uuid as key
    def set_address(self, uuid, address):
        self.routing_to_address[uuid] = address
    
    # Set the uuid and address in the routing table with address as key
    def set_uuid(self, address, uuid):
        self.routing_to_ID[address] = uuid

    # Check if the given address is in the routing table
    def check_address(self, uuid, address):
        if uuid not in self.routing_to_address:
            self.set_address(uuid, address)
            self.set_uuid(address, uuid)
            return address
        return False

    # Process a given heartbeat
    # Delete the node from the routing table as the host did not get a response at the heartbeat
    def process_heartbeat(self, address):
        uuid = self.routing_to_ID[address]
        del self.routing_to_ID[address]
        del self.routing_to_address[uuid]

    # Return the address of a node given the ID
    def get_address(self, uuid):
        print(uuid)
        return self.routing_to_address[uuid]