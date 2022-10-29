class RoutingTable:
    def __init__(self):
        self.host = None
        self.guid = None
        self.routing_to_address = {}
        self.routing_to_ID = {}
    
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

    # Send a heartbeat at a set time interval
    def send_heartbeat(self):
        pass

    # Process a given heartbeat
    # This function controls which nodes have sent a heartbeat
    def process_heartbeat(self):
        pass

    # Remove a node from the network
    def remove_node(self):
        pass

    # Return the ID of a node given the address
    def get_ID(self, address):
        return self.routing_to_ID[address]

    # Return the address of a node given the ID
    def get_address(self, ID):
        return self.routing_to_address[ID]