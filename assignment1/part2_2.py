tele_key = "51634782"
house_key = 3
cipher = "HSQQD XHDRP YFKWV HNHDL OULLQ DDWVW BDWWA RJULS"
cipher = cipher.replace(" ", "").lower()

def numerically(cipher):
    numeric = []
    for letter in cipher:
        numeric.append(ord(letter)-97)
    return numeric

def letters(numbers):
    plaintext = []
    for numb in numbers:
        plaintext.append(chr(numb+97))
    return plaintext

def ceasar(cipher, house_key):
    cipher_numb = numerically(cipher)
    print(cipher_numb)
    ceasar_numb = []
    for i in cipher_numb:
        number = i - house_key
        if number < 0:
            number += 26
            print(number)
        ceasar_numb.append(number)

    return ceasar_numb

cipher_ceasar = ceasar(cipher, house_key)
cipher_text = letters(cipher_ceasar)
print((cipher_text))