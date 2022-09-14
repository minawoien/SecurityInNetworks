
def remove_duplicates():
    for seq_dict in sequences:
        sequences[seq_dict] = list(dict.fromkeys(sequences[seq_dict]))

# Find the repeated sequences
sequences = {}
def find_sequences(encrypted):
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
    remove_duplicates()
    remove_keys()
    print(sequences)


# Removes the keys where the keys are inside another key if their length of repetitions are less than 4
def remove_keys():
    rm_keys = []
    for i in sequences:
        for j in sequences:
            if i == j:
               continue
            elif i in j:
                if i not in rm_keys:
                    if len(sequences[i]) < 4:
                        rm_keys.append(i)
    for key in rm_keys:
        sequences.pop(key)


# Finds the lengths between the repetitions 
def find_length():
    for i in sequences:
        sequences[i].sort()
        # Blir dette riktig?
        length = sequences[i][1]-sequences[i][0]
        find_factors(length)


def find_factors(length):
    for i in range(1, length + 1):
       if length % i == 0:
            if 1 < i <= 10:
                print(i, length)
        

# Receives the encrypted text, removes the spaces and covert to lowercase
encrypted = input("Write in your encrypted text: ")
encrypted = encrypted.replace(" ", "").lower()

find_sequences(encrypted)
find_length()

