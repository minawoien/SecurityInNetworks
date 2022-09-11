
def numerically(cipher):
    numeric = []
    for letter in cipher:
        numeric.append(ord(letter)-97)
    return numeric

def letters(numbers):
    plaintext = ""
    for numb in numbers:
        plaintext += chr(numb+97)
    return plaintext

def caesar(cipher, house_key):
    cipher = cipher.replace(" ", "").lower()
    cipher_numb = numerically(cipher)
    caesar_numb = []
    for i in cipher_numb:
        number = i - house_key
        if number < 0:
            number += 26
        caesar_numb.append(number)
    cipher_text = letters(caesar_numb)
    return cipher_text

def decrypt_transposition(cipher, key):
    # Number of columns
    column_numb = len(key)
    rows_numb = int(len(cipher)/len(key))

    #Add 5 (the length of the cipher/key) letters to a list of columns as one element
    columns = []
    for i in range(1, column_numb+1):
        columns.append(cipher[rows_numb*(i-1):rows_numb*i])

    # # creates the rows of the transposition cipher matrix with 8 letters
    matrix = []
    for j in range(len(columns)): # Happens 5 times
        row = []
        for i in range(rows_numb): # Happens 8 times
            row.append(columns[j][i])
        matrix.append(row)

    text = ""
    for j in range(rows_numb):
        for i in key:
            text += matrix[int(i)-1][j]
    return text


if __name__ == "__main__":
    house_key = 3
    cipher = "HSQQD XHDRP YFKWV HNHDL OULLQ DDWVW BDWWA RJULS"
    

    cipher_text = caesar(cipher, house_key)
    print((cipher_text))