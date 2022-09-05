# Receives the encrypted text, removes the spaces and covert to lowercase
encrypted = input("Write in your encrypted text: ")
encrypted = encrypted.replace(" ", "").lower()

#key_length = int(input("Key length: "))

# Encrypted text expressed numerically
encrypted_numeric = []
for letter in encrypted:
    encrypted_numeric.append(ord(letter)-97)

# Find the highest repeated sequence
sequences = []
for i in range(len(encrypted_numeric)):
    if i+1 < len(encrypted_numeric):
        numbers = []
        numbers.append(encrypted_numeric[i])
        numbers.append(encrypted_numeric[i+1])
        sequences.append(numbers)

for i in range(0, len(sequences), 2):
    for j in range(2, len(sequences)+1, 2):
        print(sequences[i])
        print(sequences[j])
        if sequences[i] == sequences[j]:
            print("ja")



# for i in encrypted_numeric:
#     print(i)