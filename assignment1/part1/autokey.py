
class AutoKey:
    def __init__(self):
        self.plaintext = ""
        self.plaintext_numb = []

    # Letters expressed numerically
    def numerically(self, encrypted):
        numeric = []
        for letter in encrypted:
            numeric.append(ord(letter)-97)
        return numeric

    # Numbers expressed as letters
    def letters(self, numbers):
        for numb in numbers:
            self.plaintext += chr(numb+97)
        return self.plaintext

    # Find plaintext numerically with the use of the key
    # Returns plaintext in numbers for det first len(key) letters
    def find_plaintext(self, key, encrypted):
        numbers = []
        for i in range(len(key)):
            plain_number = encrypted[0]-key[i]
            if plain_number < 0:
                plain_number = 26 + plain_number
            numbers.append(plain_number)
            encrypted = encrypted.pop(0)
        return numbers
        


if __name__ == "__main__":
    encrypted = 'ULPWZ'
    encrypted = encrypted.replace(" ", "").lower()

    auto_key = AutoKey()

    cipher_numb = auto_key.numerically(encrypted)

    key = "n"
    key_numb = auto_key.numerically(key)

    for i in range(len(encrypted)-len(key_numb)+1):
        number = auto_key.find_plaintext(key_numb, cipher_numb)
        key_numb = number
        text = auto_key.letters(number)
        print(text)

    

    # plain_numb = auto_key.find_plaintext(key_numb, cipher_numb)
    # # text = auto_key.letters(plain_numb)


    # numb_2 = auto_key.find_plaintext(plain_numb, cipher_numb)
    
    # print(len(encrypted))