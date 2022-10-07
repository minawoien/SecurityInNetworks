# Assignment 2

Describe the contents of the directory and any special instructions needed to run your programs (i.e. if it requires and packages, commands to install the package. describe any command line arguments with the required parameters).


`pip install pycryptodomex`


### How to run
Open a terminal for Alice and one for Bob
`export FLASK_APP=alice.py`
`flask run --host 0.0.0.0 --port 5000`

`export FLASK_APP=bob.py`
`flask run --host 0.0.0.0 --port 5001`
