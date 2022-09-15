import math

def calculate_fitness(sequences, quadgram):
    fitness = 0
    for i in sequences:
        print(i, "sequence")
        if i in quadgram.keys():
            count = int(quadgram[i])
        else:
            count = 0
        prob = math.log(count/len(quadgram))
        print(prob, "prob")
        fitness += prob
    return fitness

# Extracting each quadgram
def find_sequences(text):
    sequences=[]
    length = 4
    for j in range(len(text)):
        base = text[j:j+length]
        if len(base) < length:
            break
        if base not in sequences:
            sequences.append(base)
    return sequences

if __name__=="__main__":
    text = "ATTACK THE EAST WALL OF THE CASTLE AT DAWN"
    text = text.replace(" ", "").lower()
    sequences = find_sequences(text)
    quadgrams = {}
    with open("english_quadgrams.txt") as file:
        for line in file.readlines():
            line = line.strip().split(" ")
            quadgrams[line[0].lower()] = line[1]
    calculate_fitness(sequences, quadgrams)