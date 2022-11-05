# Assignment 3

Install the required packages to run the code:
`pip install flask`

## Code structure
"node.py" is the main file of the program. This file includes all the routes and is built based on "alice.py" and "bob.py" from assignment 2. This file includes the ArgumentParser class which is from Stackoverflow, "How to pass an arbitrary argument to flask through
app.run()?", https://stackoverflow.com/questions/48346025/how-to-pass-an-arbitrary-argument-to-flask-through-app-run, Mar 27, 2019. (accessed: Okt 20, 2022).

"func.py" contains extra functions for the program.

"hashTable.py" contains the Hash Table class which contains the DHT and all functions needed to add, access and delete files. This file includes the function "create_hash()" which is from 'Python Program to find hash', https://www.programiz.com/python-programming/examples/hash-file, (accessed: 01.11.22).

"routing.py" contains the Routing class which contains the routing table and all functions needed to add, access and delete nodes.

"secure_communication.py" is the file created for assignment 2. This file includes the Diffie Hellman class, the BBS class and the Symmetric Cipher class used for generating keys and encrypt and decrypt files.


## How to run
To start the first node, in the terminal, enter:

`python3 node.py -host` "node's address"

To start nodes when one have entered the network, in another terminal, enter: 

`python3 node.py -host` "address of node at the network" `-r` "node's address"


For example, the first node can start at the address: "127.0.0.1:8080" and the second node at address: "127.0.0.1:5001". To run at these addresses, in one terminal, enter:

`python3 node.py -host 127.0.0.1:8080`

In another terminal enter:
`python3 node.py -host 127.0.0.1:5001 -r 127.0.0.1:8080`
