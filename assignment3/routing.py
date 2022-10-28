class RoutingTable:
    def __init__(self):
        self.host = None
        self.routing_to_address = {}
        self.routing_to_ID = {}
    
    # Set the address to the routing table
    def set_address(self, socket, port):
        self.routing_to_address[socket] = port
    
    # Check if the given address is in the routing table
    def check_address(self, address):
        if address not in self.routing_to_address:
            address_info = address.split(":")
            self.set_address(address, address_info[1])

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