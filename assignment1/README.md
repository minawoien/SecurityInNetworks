## Assignment 1

### Part 1
vigenere.py contains the first try of solving the cipher text with the Vigenere cipher. This file can be run from the directory part1, by runing `python vigenere.py` in the terminal.

auto.py contains the algorithm that decipher the key with a known key and the algorithm that replaces low frequency words with high frequency words. This file can be run from the directory part1, by runing `python auto.py` in the terminal.

autokey.py contains the algorithm that checks how many English common words each deciphered text contains and finds the best keys based on that. It uses the file words.txt. This file can be run from the directory part1, by runing `python autokey.py` in the terminal.

autokey_quad.py contains the algorithm used to find the correct key to decipher the cipher text. It uses both the file english_quadgrams.txt and the file words.txt. This file can be run from the directory part1, by runing `python autokey_quad.py` in the terminal.
  
Part 2
- task2.py is the file that solves task 2. It decipher the cipher text with an Caesar-cipher algorithm to decrypt the cipher text and an column-transposition-cipher algorithm to decrypt the result of the Caesar-cipher.
- task4.py is the file that solves task 4. It encrypts the plain text message from task 2 with an an column-transposition-cipher algorithm to encrypt the plain text message, and than the result from that encryption with the same algorithm, before that result gets encrypted with the Caesar-cipher algorithm.
- app.py is the file that solves task 5. It takes in an argument in the url, and decipher it with the Caesar-cipher algorithm from task 2 first, and then uses the column-transposition-cipher algorithm from task 2 twice.
  - This files require pip and flask installed.
    - To install pip: python install pip
    - To install flask: pip install flask
  - Example file to test in the browser:
    - http://127.0.0.1:5000/?cipher=HSQQDXHDRPYFKWVHNHDLOULLQDDWVWBDWWARJULS

To run each file:
python "filename"

