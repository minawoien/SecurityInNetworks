# Assignment 2

Describe the contents of the directory and any special instructions needed to run your programs (i.e. if it requires and packages, commands to install the package. describe any command line arguments with the required parameters).

## Part 1
This task includes the folder "part1" which contains the file "secure_communication" and "RC4.py". The "secure_communication" file is the answer to this task and includes step 1-8. The "RC4.py" file is a class for an attempted solution on the CSPRNG with the use of RC4, but is not used in the final solution of the task.

Install the required package to run the code: `pip install pycryptodomex`

To run the code make sure to be in the part 1 folder and run: `python secure_communication.py`


### Part 2
Open a terminal for Alice and one for Bob

`export FLASK_APP=alice.py`

`flask run --host 0.0.0.0 --port 5000`


`export FLASK_APP=bob.py`

`flask run --host 0.0.0.0 --port 5001`
