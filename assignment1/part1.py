# Receives the encrypted text, removes the spaces and covert to lowercase
from itertools import count


encrypted = input("Write in your encrypted text: ")
encrypted = encrypted.replace(" ", "").lower()

#key_length = int(input("Key length: "))

# Encrypted text expressed numerically
# encrypted_numeric = []
# for letter in encrypted:
    #encrypted_numeric.append(ord(letter)-97)

def remove_duplicates():
    for seq_dict in sequences:
        sequences[seq_dict] = list(dict.fromkeys(sequences[seq_dict]))
        #print(sequences[seq_dict])
           

# Find the repeated sequences
sequences = {}
def find_sequences(text):
    # Range over length of the sequences
    for i in range(3,30):
        # Range over the cipher text and find the base for each loop
        for j in range(len(encrypted)-i):
            base = encrypted[j:j+i]
            # Range over the cipher text again and skips the equal indexes of the base
            # If the base is equal to another sequence it will be added to a dictionary, 
            # with the base as a key and the indexes of where it is placed in the text
            for k in range(len(encrypted)-i):
                if k == j:
                    continue
                if base == encrypted[k:k+i]:
                    if base not in sequences.keys():
                        sequences[base] = [k, j]
                    else:
                        sequences[base].append(k)
                        sequences[base].append(j)

find_sequences(encrypted)
remove_duplicates()
print(sequences)



# sequences = []
# for i in range(len(encrypted_numeric)):
#     if i+1 < len(encrypted_numeric):
#         numbers = []
#         numbers.append(encrypted_numeric[i])
#         numbers.append(encrypted_numeric[i+1])
#         sequences.append(numbers)

# for i in range(0, len(sequences), 2):
#     for j in range(2, len(sequences)+1, 2):
#         print(sequences[i])
#         print(sequences[j])
#         if sequences[i] == sequences[j]:
#             print("ja")



# for i in encrypted_numeric:
#     print(i)