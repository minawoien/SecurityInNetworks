# Receives the encrypted text, removes the spaces and covert to lowercase
encrypted = input("Write in your encrypted text: ")
encrypted = encrypted.replace(" ", "").lower()

key_length = int(input("Key length: "))

# Encrypted text expressed numerically
encrypted_numeric = []
for letter in encrypted:
    encrypted_numeric.append(ord(letter)-97)
    
for i in encrypted_numeric:
    print(i)