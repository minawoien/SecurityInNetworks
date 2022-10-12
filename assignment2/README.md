# Assignment 2
Install the required package to run the code: 

`pip install pycryptodomex`

`pip install flask`

## Part 1
This task includes the folder "part1" which contains the file "secure_communication.py" and "RC4.py". The "secure_communication.py" file is the answer to this task and includes step 1-8. The "RC4.py" file is a class for an attempted solution on the CSPRNG with the use of RC4, but is not used in the final solution of the task.

### To run the program
To run the code make sure to be in the "part1" folder and run: `python secure_communication.py`


## Part 2
This task includes the folder "part2" which contains the files "alice.py", "bob.py", "secure_communication.py", and "servers.py", and the folder "templates" with "indexA.html" and "indexB.html".

The files "alice.py" and "bob.py" is the files for running the programs. This files creates one server each, one for Alice and one for Bob. The logic and content are approximately the same in this files. 

The file "servers.py" contains a class for Alice and one for Bob, where they can store variables.

The file "secure_communications.py" is almost equal to the one i the folder "part1". Some changes have been made as the servers creates the classes in the file separately.

The folder "templates" contains two html-files for view the data in the web-browser.

### To run the program
Make sure to be in the "part2" folder and open one terminal for Alice and one for Bob

In one terminal:

`export FLASK_APP=alice.py`

`flask run --host 0.0.0.0 --port 8080`

In the other terminal:

`export FLASK_APP=bob.py`

`flask run --host 0.0.0.0 --port 5000`

