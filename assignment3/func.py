from secure_communication import BBS
import requests, json, time
ALLOWED_EXTENSIONS = {'txt'}

# Connect with the remote host and sends its own address
# Add the remote host to the routing table
def connect(address, routing, dht):
    response = requests.post(f"http://{address}/est", json={"address": routing.host, "uuid": routing.uuid})
    routing.check_address(response.text, address)
    share_table(address, routing)
    request_hash_table(address, dht)

# Get the routing table of the remote host and share it with every node in the host's routing table
def share_table(address, routing):
    table = requests.get(f"http://{address}/getNodes").content
    table = json.loads(table)
    for uuid in table:
        new_address = routing.check_address(uuid, table[uuid])
        if new_address:
            requests.post(f"http://{new_address}/est", json={"address": routing.host, "uuid": routing.uuid})

# Request the hash table from the remote host nodes
def request_hash_table(address, dht):
    table = requests.get(f"http://{address}/getHashTable").content
    table = json.loads(table)
    dht.update_table(table)       

def updated_dht(routing, dht):
    for address in routing.routing_to_ID.keys():
        if address != routing.host:
            requests.post(f"http://{address}/getdht", json={"file": dht.hashTable.copy()})

def generate_secret_key(pu_k, private_key, dh):
    shared_key = dh.generate_shared_key(private_key, pu_k)
    bbs = BBS(shared_key)
    return bbs.generate_key(16*8)


# Send a heartbeat to each node in the host's routing table at a set time interval
def send_heartbeat(routing, dht):
    while True:
        for address in routing.routing_to_ID.keys():
            if address != routing.host:
                try:
                    requests.get(f"http://{address}/heartbeat").content
                except:
                    dht.remove_node(routing.routing_to_ID[address])
                    routing.process_heartbeat(address)
        time.sleep(5)

# Function that checks if the uploaded file is a txt
# From Uploading files. https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/. (accessed: Nov 6, 2022)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS