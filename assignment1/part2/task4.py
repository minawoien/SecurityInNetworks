# Expresses letters numerically
def numerically(text):
    numeric = []
    for letter in text:
        numeric.append(ord(letter)-97)
    return numeric

# Translate numbers back to letters
def letters(numbers):
    text = []
    for numb in numbers:
        text.append(chr(numb+97))
    return text

def transposition_cipher(text, key):
    # Finds the number of rows in the transposition cipher matrix
    rows_numb = int(len(text)/len(key))

    # Add 8 (the length of the key) letters to a list of rows as one element
    rows = []
    for i in range(1,rows_numb+1):
        rows.append(text[len(key)*(i-1):len(key)*i])

    # creates the columns of the transposition cipher matrix with five letters
    matrix = []
    for j in range(len(key)): # Endre?
        column = []
        for i in range(len(rows)): #Endre?
            column.append(rows[i][j])
        matrix.append(column)

    # Adding each number in the key to a list after subtracting with one. 
    # This becomes the list of indexes for the columns order in cipher
    key_list = []
    for i in key:   
        key_list.append(int(i)-1)  

    # Sorts the matrix based on the columns indexes from the key
    sorted_matrix = [x for _, x in sorted(zip(key_list, matrix))]

    # Add column by column to a string which becomes the cipher text
    cipher_text = ""
    for i in range(len(sorted_matrix)):
        for j in range(len(column)):
            cipher_text += sorted_matrix[i][j]

    return cipher_text

def caesar_cipher(text, key):
    # Expresses the letters numerically to subtract the value of the key from each number 
    # before they are translated back to letters
    numbers = numerically(text)
    caesar_numb = []
    for i in numbers:
        number = i + key
        if number > 25:
            number -= 26
        caesar_numb.append(number)
    cipher_list = letters(caesar_numb)
    cipher_text = ""
    for i in cipher_list:
        cipher_text += i
    return cipher_text

if __name__ == "__main__":
    # Uses the transposition cipher algorithm one time with the clear text
    clear_text = "Leave your package in the train station at six pm"
    clear_text = clear_text.replace(" ", "").lower()
    tran_key = "51634782"
    cipher_text = transposition_cipher(clear_text, tran_key)
    print(cipher_text)

    # Uses the transposition cipher algorithm a second time with the cipher text
    cipher_text_second = transposition_cipher(cipher_text, tran_key)
    print(cipher_text_second)

    # Uses the caesar cipher algorithm 
    caesar_key = 3
    caesar_text = caesar_cipher(cipher_text_second, caesar_key)
    print(caesar_text)
