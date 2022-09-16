# Assignment 1

## Part 1
### vigenere.py 
This file contains the first try of solving the cipher text with the Vigenere cipher. This file can be run from the directory part1, by runing `python vigenere.py` in the terminal.

### autokey.py 
This file contains the algorithm that decipher the key with a known key and the algorithm that replaces low frequency words with high frequency words. This file can be run from the directory part1, by runing `python auto.py` in the terminal. The user will be asked wether the key is know or not. If the key is known, enter `y` and write in the key. If the key is not known, enter `n` and the algorithm will print the cipher text with replaced letters.  

### auto.py 
This file contains the algorithm that checks how many English common words each deciphered text contains and finds the best keys based on that. It uses the file words.txt. This file can be run from the directory part1, by runing `python autokey.py` in the terminal.

### autokey_quad.py 
This file contains the algorithm used to find the correct key to decipher the cipher text. It uses both the file english_quadgrams.txt and the file words.txt. This file can be run from the directory part1, by runing `python autokey_quad.py` in the terminal.

### english_quadgrams.txt
This file is downloaded from James Lyons, "Quadgram Statistics as a Fitness Measure", http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/

### words.txt
This file is contains the 1000 most common words in English from "1000 most common words in English", https://www.ef.com/wwen/english-resources/english-vocabulary/top-1000-words/
  
## Part 2
### task2.py 
This file solves task 2. It decipher the cipher text with a Caesar-cipher algorithm to decrypt the cipher text and a column-transposition-cipher algorithm to decrypt the result of the Caesar-cipher. This file can be run from the directory part2, by runing `python task2.py` in the terminal.

### task4.py 
This file solves task 4. It encrypts the plain text message from task 2 with a column-transposition-cipher algorithm to encrypt the plain text message, and than the result from that encryption with the same algorithm, before that result gets encrypted with the Caesar-cipher algorithm. This file can be run from the directory part2, by runing `python task4.py` in the terminal.

### app.py
This file solves task 5. It takes in an argument in the url, and decipher it with the Caesar-cipher algorithm from task 2 first, and then uses the column-transposition-cipher algorithm from task 2 twice.
This files require pip and flask installed.
- To install pip: `python install pip`
- To install flask: `pip install flask`

This file can be run from the directory part2, by runing `python app.py` in the terminal.

Example file to test in the browser: http://127.0.0.1:5000/?cipher=sphdwdhldsqflwrdkovjhrnqwqyddaxwuwuhvlbl

