# Letters expressed numerically
def numerically(cipher):
    numeric = []
    for letter in cipher:
        numeric.append(ord(letter)-97)
    return numeric

# Numbers expressed as letters
def letters(numbers):
    plaintext = ""
    for numb in numbers:
        plaintext += chr(numb+97)
    return plaintext

# The Caesar algorithm that takes in the cipher text and the key
# The cipher text gets expressed numerically before the key is subtracted from each letter in the text
# If the number is lower than zero it gets added with 26, the length of the English alphabet
# The numbers are expressed back in letters before the text is returned
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

# Algorithm for the column transposition cipher which takes in the cipher text and the key
def decrypt_transposition(cipher, key):
    # Number of columns and rows
    column_numb = len(key)
    rows_numb = int(len(cipher)/len(key))

    #Add the length of the cipher/key (5) letters to a list of columns as one column
    columns = []
    for i in range(1, column_numb+1):
        columns.append(cipher[rows_numb*(i-1):rows_numb*i])

    # Creates the rows of the transposition cipher matrix with 8 letters
    # Adds the first letter of each column to each row
    matrix = []
    for j in range(len(columns)): # Happens 5 times
        row = []
        for i in range(rows_numb): # Happens 8 times
            row.append(columns[j][i])
        matrix.append(row)

    # Adds the letters in the key direction column wise
    # The rows are added downwards to a string which becomes the plaintext
    text = ""
    for j in range(rows_numb):
        for i in key:
            text += matrix[int(i)-1][j]
    return text


if __name__ == "__main__":
    phone_key = "51634782"
    house_key = 3
    cipher = "HSQQD XHDRP YFKWV HNHDL OULLQ DDWVW BDWWA RJULS"
    cipher_text = caesar(cipher, house_key)
    plain_text = decrypt_transposition(cipher_text, phone_key)
    print(plain_text)