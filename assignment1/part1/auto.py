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
    def __init__(self):
        self.plaintext_numb = []
        #self.parent_key = ''.join(random.choices(string.ascii_uppercase, k=key_length)).lower()

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
        self.list = common_words
        self.saved = []
        self.count = 0
        self.all_scores = []

    # Look at all lists in the self.saved list
    def next_key(self):
        num_par_key = numerically(self.current_key)
        if len(num_par_key)>3:
            res = all(ele == 25 for ele in num_par_key[-3:])
        else:
            res = all(ele == 25 for ele in num_par_key)
        if res is True:
            return None  
        now = len(num_par_key)-4
            
            # for j in range(len(self.saved[now])):
            #     print(j, "j hver gang")
            #     print(now, "now")
            #     num_par_key[0] = self.saved[now][j]
        for i in range(now+1, len(num_par_key)):
            num_par_key[i] += 1
            if num_par_key[i] > 25:
                num_par_key[i] = 0
            else:
                break
        child_key = letters(num_par_key)
        self.current_key = child_key
        return num_par_key
        # else:
        #     res = all(ele == 25 for ele in num_par_key)
        #     if res is True:
        #         return None  
        #     for i in range(len(num_par_key)):
        #         num_par_key[i] += 1
        #         if num_par_key[i] > 25:
        #             num_par_key[i] = 0
        #         else:
        #             break
        # child_key = letters(num_par_key)
        # print(child_key)
        # self.current_key = child_key
        # return num_par_key
        
    def calculate_freq_score(self, text):
        score = 0
        for i in range(len(self.list)):
            if self.list[i] in text:
                score += 1
        return score
    
    def remove_low_score(self, key_score):
        sorted_score = dict(sorted(key_score.items(), key=lambda item: item[1], reverse=True))
        best_score = {}
        count = 0
        for i in sorted_score:
            if count == 15:
                break
            best_score[i] = sorted_score[i]
            count += 1
        return best_score

    # One list with letters for each index
    def best_letter(self, key_score):
        index = []
        count = 0
        print(self.saved)
        if len(self.saved) == 0:
            for j in key_score:
                if count == self.key_length:
                    break
                if j[0] not in index:
                    index.append(j[0])
                    count += 1
        else:
            for i in range(len(self.saved)):
                for j in key_score:
                    if count == self.key_length:
                        break
                    if j[i+1] not in index:
                        index.append(j[i+1])
                        count += 1
        self.saved.append(numerically(index))
        print(self.saved)
        return self.saved

class Tester:
    def __init__(self, common_words):
        self.gen_key = GenerateKey(common_words)
        self.auto_key = AutoKey()
    
    def test(self):
        # Gjør om current nøkkel til tall
        key = numerically(self.gen_key.current_key)
        self.gen_key.key_length = len(key)
        key_score ={}
        while key is not None:
        #for j in range(100000):
            generate = 1
            if (len(key) > 3):
                now = len(key)-4
                generate = len(self.gen_key.saved[now])
                print(generate, "generate")
            for j in range(generate):
                if len(key) > 3 :
                    print("Lengde:" ,len(key))
                    print(now)
                    key[now] = self.gen_key.saved[now][j]
                    print(key[0], "key[0]")
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
                if key is None:
                    break
        #print(key_score)
        best_score = self.gen_key.remove_low_score(key_score)
        print("best score: ", best_score)
        saved = self.gen_key.best_letter(best_score)
        print(text)
        print(self.gen_key.current_key)
        self.gen_key.current_key = self.gen_key.current_key + "a"
        return best_score

if __name__ == "__main__":
    common_words = []
    with open("words.txt", "r") as file:
        for i in file.readlines():
            common_words.append(i.strip())

    #encrypted = 'FRRPU TIIYE AMIRN QLQVR BOKGK NSNQQ IUTTY IIYEA WIJTG LVILA ZWZKT ZCJQH IFNYI WQZXH RWZQW OHUTI KWNNQ YDLKA EOTUV XELMT SOSIX JSKPR BUXTI TBUXV BLNSX FJKNC HBLUK PDGUI IYEAM OJCXW FMJVM MAXYT XFLOL RRLAA JZAXT YYWFY NBIVH VYQIO SLPXH ZGYLH WGFSX LPSND UKVTR XPKSS VKOWM QKVCR TUUPR WQMWY XTYLQ XYYTR TJJGO OLMXV CPPSL KBSEI PMEGC RWZRI YDBGE BTMFP ZXVMF MGPVO OKZXX IGGFE SIBRX SEWTY OOOKS PKYFC ZIEYF DAXKG ARBIW KFWUA SLGLF NMIVH VVPTY IJNSX FJKNC HBLUK PDGUI IYEAM HVFDY CULJS EHHMX LRXBN OLVMR'
    #encrypted = "ZICVTWQNGKZEIIGAS XSTSLVVWLA "
    encrypted = "TIFGNSTMUQZIZEIFPQNMTJHVTKRAEELMJHICAYPVETUWMFCIZPAXOIAJACBCQEKGFJXRGFERCXRTWCBXUGYNBOLVMVBTSWKBTTOSYXRVNQNEMEOHLNOLFVISHYXYVJSPXHIWMFEVVBCZTNXJLLXVFYDTWWQPPEYKIVDRJZXMSIHZRLAAJZAXTYHIPUYRDOQYUCMDPCTCMDKJDGFBBNJDIEBSAIHKFKBGUBLDMHYMPSFSPXSTXTMWHFTIFXTJAMJFEPSOMXZYEOSPCZRMVHQWQXPXKGJSQGOLUPMFUFSMSFUZMRVGYOMLVKWULJOJWBNRMWFBNNHIVMZDZELEAQI"

    encrypted = encrypted.replace(" ", "").lower()

    gen_key = GenerateKey(common_words)

    auto_key = AutoKey()
    cipher_numb = numerically(encrypted)

    tester = Tester(common_words)
    for i in range(4):
        best_score = tester.test()
    print(best_score)
    for key in best_score:
        key_num = numerically(key)
        cipher_numb = numerically(encrypted)
        text =""
        for x in range(round(len(encrypted)/len(key_num))):
            number = auto_key.find_plaintext(key_num, cipher_numb)
            key_num = number
            text += letters(number)
        print(key)
        print(text)
        print()
    
