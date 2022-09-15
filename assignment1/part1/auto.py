import math

# Letters expressed numerically
def numerically(encrypted):
    numeric = []
    for letter in encrypted:
        numeric.append(ord(letter)-97)
    return numeric

# Numbers expressed as letters
def letters(numbers):
    text = ""
    for numb in numbers:
        text += chr(numb+97)
    return text

# Class used to decipher the text
class AutoKey:
    # Find plaintext numerically with the use of the key
    # Returns plaintext in numbers for det first len(key) letters
    # The first letter in cipher_text will be removed from the list of encrypted letters because the function
    # always decipher the first letter in the cipher_text
    def find_plaintext(self, key, encrypted):
        numbers = []
        for i in range(len(key)):
            if len(encrypted) > 0:
                plain_number = encrypted[0]-key[i]
                if plain_number < 0:
                    plain_number = 26 + plain_number
                numbers.append(plain_number)
                encrypted.pop(0)
        return numbers


# Class used to generate the most correct key
# The class takes in a list of common English words used to generate the best keys
# It saves a current_key variable which starts as "aa"
# It also saves a list where the letters I want to save and further use to generate keys, gets saved
# count?
class GenerateKey:
    def __init__(self, common_words):
        self.current_key = "aa"
        self.list = common_words
        self.saved = []
        self.count = 0

    # Finds the next current key
    # Express the current key numerically, and return None to indicate that a letter can be added to the key,
    # to increase the key length by one, if the three last letters are the same
    def next_key(self):
        num_par_key = numerically(self.current_key)
        if len(num_par_key)>3:
            res = all(ele == 25 for ele in num_par_key[-3:])
        else:
            res = all(ele == 25 for ele in num_par_key)
        if res is True:
            return None
        
        # Finds the current index to change letter of
        now = len(num_par_key)-3

        # Loop through the length of the numerically key and starts on the current index
        # If the letter numerically is higher than 25, which is higher than the English alphabet it becomes an
        # a and the loop stops for each changed letter
        # The key gets expressed in letters and set as current key, and returned numerically
        for i in range(now, len(num_par_key)):
            num_par_key[i] += 1
            if num_par_key[i] > 25:
                num_par_key[i] = 0
            else:
                break
        child_key = letters(num_par_key)
        self.current_key = child_key
        return num_par_key
    
    # Calculates a score based on who many common English words are in the current deciphered text
    def calc_score(self, text):
        score = 0
        for i in range(len(self.list)):
            if self.list[i] in text:
                # if len(self.list[i]) > 2:
                #     score += 1
                score += 1
        return score
    
    # The dictionary with the keys and scores are sorted by fitness, and only the 25 keys with the highest
    # fitness are saved
    def remove_low_score(self, key_score):
        sorted_score = dict(sorted(key_score.items(), key=lambda item: item[1], reverse=True))
        best_score = {}
        count = 0
        for i in sorted_score:
            if count == 25:
                break
            best_score[i] = sorted_score[i]
            count += 1
        return best_score

    # Function to find which letter to save
    def best_letter(self, key_score):
        index = []
        count = 0
        # If no letters are saved, we loop through the keys with the highest fitness and saves the first letter
        # of the 6 first keys
        if len(self.saved) == 0:
            for j in key_score:
                if count == 6:
                    break
                if j[0] not in index:
                    index.append(j[0])
                    count += 1
        # If there already are letters saved in the list, we save the next letter of the 6 first keys
        else:
            for i in range(len(self.saved)):
                for j in key_score:
                    if count == 6:
                        break
                    if j[i+1] not in index:
                        index.append(j[i+1])
                        count += 1
        # The letters that are going to be saved gets expressed numerically and added to the saved list
        self.saved.append(numerically(index))
        return self.saved
    
    # Calculates the fitness by taking the logarithmic sum of the probability for each sequence
    # The probability for each 4-letter sequence is calculated by finding the number of appearances of the 
    # sequence from the file containing sequences from an English book, and dividing it with the number of 
    # sequences from the book
    def calculate_fitness(self, sequences):
        fitness = 0
        for i in sequences:
            if i in self.quadgrams.keys():
                count = int(self.quadgrams[i])
                prob = math.log(count/len(self.quadgrams))
                fitness += prob
        return fitness

    # Extracting each quadgram from the deciphered text, adding them to a list if they are not in the list
    def find_sequences(self, text):
        sequences = []
        length = 4
        for j in range(len(text)):
            base = text[j:j+length]
            if len(base) < length:
                break
            if base not in sequences:
                sequences.append(base)
        return sequences


# Test class that takes in the GenerateKey and AutoKey class
class Tester:
    def __init__(self, common_words):
        self.gen_key = GenerateKey(common_words)
        self.auto_key = AutoKey()
    
    def test(self):
        # Express the key numerically
        key = numerically(self.gen_key.current_key)
        self.gen_key.key_length = len(key)
        key_score ={}
        # Loops until the last three letters in the key are the same, before the key length can be increased
        # with one
        while key is not None:
            generate = 1
            # If the key length is higher than three, we find the current index to change and witch saved 
            # letters we want to loop through
            if (len(key) > 3):
                now = len(key)-4
                generate = len(self.gen_key.saved[now])
            # Loop trough the 1 time if the key length are 2 or 3, and loops through 6 times if the key is
            # longer than 3
            for j in range(generate):
                # Sets the current index of the key to the current saved list letters
                if len(key) > 3:
                    key[now] = self.gen_key.saved[now][j]
                start_key = key 
                text = ""
                # Express the cipher text numerically
                cipher_numb = numerically(encrypted)
                # Decipher the text with the current key
                # We can only decipher a key length at one time, and the loop which finds the plain text is
                # therefore run length of the cipher_text divided by the key length times
                # First it runs with the key and returns numbers which represents the first part of the
                # plaintext, it gets saved and the next time the loop runs this plaintext is used as the key
                for x in range(round(len(encrypted)/len(key))):
                    number = self.auto_key.find_plaintext(key, cipher_numb)
                    key = number
                    text += letters(number)
                # The fitness score is calculated and saved with the key expressed in letters before the next
                # key is find
                score = self.gen_key.calc_score(text)
                self.gen_key.current_key = letters(start_key)
                key_score[self.gen_key.current_key] = score
                key = self.gen_key.next_key()
                if key is None:
                    break
        # The keys with the best fitness is find and and used to find which letters to save and use for the
        # next key length before the best score dictionary are returned
        best_score = self.gen_key.remove_low_score(key_score)
        self.gen_key.best_letter(best_score)
        self.gen_key.current_key = self.gen_key.current_key + "a"
        return best_score


if __name__ == "__main__":
    # Imports common English words from a file and put them into a list
    common_words = []
    with open("words.txt", "r") as file:
        for i in file.readlines():
            common_words.append(i.strip())

    # The cipher_text gets expressed in low letters and spaces are removed before it gets expressed numerically
    encrypted = 'FRRPU TIIYE AMIRN QLQVR BOKGK NSNQQ IUTTY IIYEA WIJTG LVILA ZWZKT ZCJQH IFNYI WQZXH RWZQW OHUTI KWNNQ YDLKA EOTUV XELMT SOSIX JSKPR BUXTI TBUXV BLNSX FJKNC HBLUK PDGUI IYEAM OJCXW FMJVM MAXYT XFLOL RRLAA JZAXT YYWFY NBIVH VYQIO SLPXH ZGYLH WGFSX LPSND UKVTR XPKSS VKOWM QKVCR TUUPR WQMWY XTYLQ XYYTR TJJGO OLMXV CPPSL KBSEI PMEGC RWZRI YDBGE BTMFP ZXVMF MGPVO OKZXX IGGFE SIBRX SEWTY OOOKS PKYFC ZIEYF DAXKG ARBIW KFWUA SLGLF NMIVH VVPTY IJNSX FJKNC HBLUK PDGUI IYEAM HVFDY CULJS EHHMX LRXBN OLVMR'
    encrypted = encrypted.replace(" ", "").lower()
    cipher_numb = numerically(encrypted)

    gen_key = GenerateKey(common_words)
    auto_key = AutoKey()
    tester = Tester(common_words)

    # Loops through the length of the maximum key length I want to find the best score of
    for i in range(9):
        best_score = tester.test()
        best_key = {}
        # Loops through the best score and decipher the cipher text again with the best keys
        # Then a score is calculated based on how many common English words there are in the deciphered text
        key = max(best_score, key=best_score.get)
        key_num = numerically(key)
        cipher_numb = numerically(encrypted)
        text =""
        for x in range(round(len(encrypted)/len(key_num))):
            number = auto_key.find_plaintext(key_num, cipher_numb)
            key_num = number
            text += letters(number)
        # The key with the highest score gets saved for each key length, and then the key with the highest
        # score are the best key the algorithm finds
        #wanted_key = max(best_key, key=best_key.get)
        print("Key length: ", len(key))
        print("Best suited key: ", key)
        print(text)
        print()


    
