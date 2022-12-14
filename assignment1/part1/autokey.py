
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
    # The first letter in cipher_text will be removed from the list of encrypted letters because the function
    # always decipher the first letter in the cipher_text
    def find_plaintext(self, key, cipher_text):
        numbers = []
        for i in range(len(key)):
            if len(cipher_text) > 0:
                plain_number = cipher_text[0]-key[i]
                if plain_number < 0:
                    plain_number = 26 + plain_number
                numbers.append(plain_number)
                cipher_text.pop(0)
        return numbers


class Frequencies:
    def __init__(self):
        self.relative_frequency = ["E", "T", "A"]
        self.relative_frequency_low = ["Q", "Z", "X"]

    # Finds the occurrences of each letter in the cipher text, stores the letters in a dictionary with the 
    # letter as key and the occurrences in percent as the value
    def find_frequencies(self, text):
        occurrences = {}
        for letter in text:
            if letter in occurrences:
                count = occurrences[letter] + 1
                occurrences[letter] = count
            else:
                occurrences[letter] = 1
        for letter in occurrences:
            percent = occurrences[letter] * 100 / len(text)
            percent = round(percent, 2)
            occurrences[letter] = percent
        return occurrences
    
    # Finds the three letters with highest frequency, and saves them in a dictionary
    def highest_frequency(self, occurrences):
        three_highest = {}
        highest = 0
        second_highest = 0
        third_highest = 0
        for letter in occurrences:
            if occurrences[letter] > highest:
                highest = occurrences[letter]
                three_highest["highest"] = letter
            if second_highest < occurrences[letter] < highest:
                second_highest = occurrences[letter]
                three_highest["second"] = letter
            if third_highest < occurrences[letter] < second_highest:
                third_highest = occurrences[letter]
                three_highest["third"] = letter
        return three_highest
    
    # Finds the letters with lowest frequency, and store them in a list, sorted by the lowest freq 
    def lowest_frequency(self, occurrences):
        lowest_freq = [100, 100]
        for letter in occurrences:
            if occurrences[letter] < lowest_freq[0]:
                lowest_freq[0] = occurrences[letter]
            elif lowest_freq[1] > occurrences[letter] > lowest_freq[0]:
                lowest_freq[1] = occurrences[letter]
        for letter in occurrences:
            if occurrences[letter] == lowest_freq[0]:
                lowest_freq[0] = letter
            if occurrences[letter] == lowest_freq[1]:
                lowest_freq[1] = letter
        return lowest_freq
    
    # Replaces the highest frequency letters with the letters from the highest frequency letters list
    # Replaces the lowest frequency letters with the letters from the lowest frequency letters list
    def replace_cipher(self, cipher_text, three_highest, lowest):
        for i in range(len(cipher_text)):
            if cipher_text[i] == three_highest["highest"]:
                cipher_text = cipher_text.replace(cipher_text[i], self.relative_frequency[0])
            if cipher_text[i] == three_highest["second"]:
                cipher_text = cipher_text.replace(cipher_text[i], self.relative_frequency[1])
            if cipher_text[i] == three_highest["third"]:
                cipher_text = cipher_text.replace(cipher_text[i], self.relative_frequency[2])
            if cipher_text[i] == lowest[0]:
                cipher_text = cipher_text.replace(cipher_text[i], self.relative_frequency_low[0])
            if cipher_text[i] == lowest[1]:
                cipher_text = cipher_text.replace(cipher_text[i], self.relative_frequency_low[1])
        print(cipher_text)                


class Sequences:
    def find_sequences(self, encrypted):
        sequences = {}
        # Range over length of the sequences
        for i in range(3,5):
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
        return sequences

    # Check if the letters from the three highest occurrences are in the sequences
    def sequence_check(self, sequences, highest):
        for seq in sequences:
            for letter in highest.values():
                if letter in seq:
                    print(seq)


if __name__ == "__main__":
    # The encrypted text from part 1.1
    encrypted = 'FRRPU TIIYE AMIRN QLQVR BOKGK NSNQQ IUTTY IIYEA WIJTG LVILA ZWZKT ZCJQH IFNYI WQZXH RWZQW OHUTI KWNNQ YDLKA EOTUV XELMT SOSIX JSKPR BUXTI TBUXV BLNSX FJKNC HBLUK PDGUI IYEAM OJCXW FMJVM MAXYT XFLOL RRLAA JZAXT YYWFY NBIVH VYQIO SLPXH ZGYLH WGFSX LPSND UKVTR XPKSS VKOWM QKVCR TUUPR WQMWY XTYLQ XYYTR TJJGO OLMXV CPPSL KBSEI PMEGC RWZRI YDBGE BTMFP ZXVMF MGPVO OKZXX IGGFE SIBRX SEWTY OOOKS PKYFC ZIEYF DAXKG ARBIW KFWUA SLGLF NMIVH VVPTY IJNSX FJKNC HBLUK PDGUI IYEAM HVFDY CULJS EHHMX LRXBN OLVMR'
    # The encrypted text from part 1.3
    # encrypted = 'IRKPV YNZPT UFQZL ULCDI OEVWF ETBAW SHLGOYQSXT UQRRK LRQUT FHUSE ZBFPR BEPHY DYEKFZSPPT VYQSY GKUHJ GNHXN UMWFF XIZFN NLWTJCKYHZ YDPDX KCOUO JEOMU AKVAU EGUEX RKHFCSNHGG WRABW RASXJ IFJHO JRLLJ KOQLO UQRITYHVFV GZGRM TLRQJ ZGNNP NYJAE DFLQI SLYSVRVKLE AJUNL MHDGE IFFQN FKEKT NJGQN OPOXMVVRRC JGHEH FEVGB QDAEI FDHTA AWFYG ZLLVOAUXFV JRPGV DYOYK BFMQA TWFMS WUQEB PQHXCWWEUP LGSGL NYMTM RXOWK FZFOE FUBFG QFNVIOVLHZ NETBS AIBBT PEIHQ DRTAU EGUEX RKHFCSNHGG PDDHY OBGOV CJBXG DVEIZ LWMJS'
    encrypted = encrypted.replace(" ", "").lower()
    auto_key = AutoKey()

    cipher_numb = auto_key.numerically(encrypted)

    statement = input("Is the key known? y/n ")
    # If the key is known the key must be written in before it gets expressed numerically
    if statement == "y":
        key = input("Key: ")
        key_numb = auto_key.numerically(key)
        # Decipher the text with the key
        # We can only decipher a key length at one time, and the loop which finds the plain text is
        # therefore run length of the cipher_text divided by the key length times
        # First it runs with the key and returns numbers which represents the first part of the
        # plaintext, it gets saved and the next time the loop runs this plaintext is used as the key
        text = ""
        for i in range(round(len(encrypted)/len(key_numb))):
            number = auto_key.find_plaintext(key_numb, cipher_numb)
            key_numb = number
            text = auto_key.letters(number)
        print(text)
    else:
        # If the key is not known it calculates the highest and lowest frequency and replaces them 
        freq = Frequencies()
        occurrences = freq.find_frequencies(encrypted)
        highest = freq.highest_frequency(occurrences)
        lowest = freq.lowest_frequency(occurrences)
        freq.replace_cipher(encrypted, highest, lowest)

        # Started on checking if the sequences included the highest frequency letters but it did not get me
        # any further
        seq = Sequences()
        sequences = seq.find_sequences(encrypted)
        seq.sequence_check(sequences, highest)

