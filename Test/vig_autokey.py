import string
import random

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

class AutoKey:
    # Find plaintext numerically with the use of the key
    # Returns plaintext in numbers for det first len(key) letters
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


class GenerateKey:
    def __init__(self, common_words):
        self.current_key = "aaa"
        self.key_length = len(self.current_key)
        self.low_freq = ["q", "x", "z"]
        self.list = common_words
        self.high_freq = ["t", "e", "a"]
        #self.saved = numerically(list(string.ascii_lowercase))
        self.saved = []
        self.count = 0
        self.nxt_saved = []
        self.save = []

    # Look at all lists in the self.saved list
    def next_key(self):
        num_par_key = numerically(self.current_key)
        # res = all(ele == 25 for ele in num_par_key)
        # if res is True:
        #     return None
        # if self.count == 5000:
        #     return None
        if (len(num_par_key) > 3):
            for j in range(len(self.saved)):
                num_par_key[0] = self.saved[j]
                for i in range(1, len(num_par_key)):
                    num_par_key[i] += 1
                    if num_par_key[i] > 25:
                        num_par_key[i] = 0
                    else:
                        self.count += 1
                        break
        else:       
            for i in range(len(num_par_key)):
                num_par_key[i] += 1
                if num_par_key[i] > 25:
                    num_par_key[i] = 0
                else:
                    self.count += 1
                    break
        print(num_par_key, "num")
        child_key = letters(num_par_key)
        self.current_key = child_key
        return num_par_key
        
    def calculate_freq_score(self, text):
        score = 0
        # for i in text:
        #     if i in self.high_freq:
        #         score += 1
        # return score

        for i in range(len(self.list)):
            if self.list[i] in text:
                score += 1
        return score
    
    def remove_low_score(self, key_score):
        sorted_score = dict(sorted(key_score.items(), key=lambda item: item[1],reverse=True))
        best_score = {}
        count = 0
        for i in sorted_score:
            if count == 10:
                break
            best_score[i] = sorted_score[i]
            count += 1
        return best_score

    # One list with letters for each index
    def best_letter(self, key_score):
        index = []
        count = 0
        if len(self.save) == 0:
            for j in key_score:
                if count == self.key_length:
                    break
                if j[0] not in index:
                    index.append(j[0])
                    count += 1
        else:
            for i in range(len(self.save)):
                for j in key_score:
                    if count == self.key_length:
                        break
                    if j[i+1] not in index:
                        index.append(j[i+1])
                        count += 1
        print(self.save)
        self.saved.append(numerically(index))
        print(self.saved, "saved")

        # count = 0
        # if self.key_length == 3:
        #     self.saved = []
        #     for j in key_score:
        #         if count == 3:
        #             break
        #         if j[0] not in self.saved:
        #             self.saved.append(j[0])
        #             count += 1
        #     print(self.saved, "saved")
        #     self.saved = numerically(self.saved)
        #     return self.saved
        # else:
        #     self.nxt_saved = []
        #     for j in key_score:
        #         if count == self.key_length:
        #             break
        #         print(j[:self.key_length-1], "j")
        #         if j[:self.key_length-1] not in self.nxt_saved:
        #             self.nxt_saved.append(numerically(j[:self.key_length-1]))
        #             count+=1
        #     print(self.nxt_saved)
        

        return self.saved
    
    # def key_from_list(self):
    #     if len(self.saved) == 0:
    #         return False
    #     else:
    #         return True
            

class Tester:
    def __init__(self, common_words):
        self.gen_key = GenerateKey(common_words)
        self.auto_key = AutoKey()
    
    def test(self):
        # Gjør om current nøkkel til tall
        key = numerically(self.gen_key.current_key)
        self.gen_key.key_length = len(key)
        #while key is not None:
        for j in range(5000):
            start_key = key
            text = ""
            # cipher text til tall
            cipher_numb = numerically(encrypted)
            for x in range(round(len(encrypted)/len(key))):
                number = self.auto_key.find_plaintext(key, cipher_numb)
                key = number
                text += letters(number)
            score = self.gen_key.calculate_freq_score(text)
            self.gen_key.current_key = letters(start_key)
            if score > 0:
                key_score[self.gen_key.current_key] = score
            key = self.gen_key.next_key()
        self.gen_key.current_key = self.gen_key.current_key + "a"
        best_score = self.gen_key.remove_low_score(key_score)
        print("best score: ", best_score)
        saved = self.gen_key.best_letter(best_score)
        print(text)
        return key_score

if __name__ == "__main__":
    with open("words.txt", "r") as file:
        common_words = []
        i = file.read()
        common_words = i.split(" ")

        encrypted = 'FRRPU TIIYE AMIRN QLQVR BOKGK NSNQQ IUTTY IIYEA WIJTG LVILA ZWZKT ZCJQH IFNYI WQZXH RWZQW OHUTI KWNNQ YDLKA EOTUV XELMT SOSIX JSKPR BUXTI TBUXV BLNSX FJKNC HBLUK PDGUI IYEAM OJCXW FMJVM MAXYT XFLOL RRLAA JZAXT YYWFY NBIVH VYQIO SLPXH ZGYLH WGFSX LPSND UKVTR XPKSS VKOWM QKVCR TUUPR WQMWY XTYLQ XYYTR TJJGO OLMXV CPPSL KBSEI PMEGC RWZRI YDBGE BTMFP ZXVMF MGPVO OKZXX IGGFE SIBRX SEWTY OOOKS PKYFC ZIEYF DAXKG ARBIW KFWUA SLGLF NMIVH VVPTY IJNSX FJKNC HBLUK PDGUI IYEAM HVFDY CULJS EHHMX LRXBN OLVMR'
        #encrypted = "ZICVTWQNGKZEIIGAS XSTSLVVWLA "
        encrypted = encrypted.replace(" ", "").lower()

        gen_key = GenerateKey(common_words)

        auto_key = AutoKey()
        cipher_numb = numerically(encrypted)

        key_score = {}
        

        tester = Tester(common_words)
        for i in range(6):
            tester.test()
        # key_score = tester.test()
        # key_score2 = tester.test()
        # key_score3 = tester.test()
        # key_score3 = tester.test()



        #key_score
        #key_score = tester.test(key)
        # gen_key.remove_low_score(key_score)
            # best_score = min(key_score, key=key_score.get)
            # print(best_score)