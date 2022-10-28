class RoutingTable:
    def __init__(self):
        self.host = None
        self.routing_to_address = {}
        self.routing_to_ID = {}
    
    def set_address(self, socket, port):
        self.routing_to_address[socket] = port
    
    def check_address(self, address):
        if address not in self.routing_to_address:
            address_info = address.split(":")
            self.set_address(address, address_info[1])


