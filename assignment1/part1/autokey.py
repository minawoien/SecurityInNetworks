from multiprocessing.connection import deliver_challenge
from operator import le
import time
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
            if len(encrypted) > 0:
                plain_number = encrypted[0]-key[i]
                if plain_number < 0:
                    plain_number = 26 + plain_number
                numbers.append(plain_number)
                encrypted.pop(0)
        return numbers


class frequencies():
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
    
    def highest_frequency(self, occurrences):
        highest = 0
        second_highest = 0
        third_highest = 0
        for letter in occurrences:
            if occurrences[letter] > highest:
                highest = occurrences[letter]
            if second_highest < occurrences[letter] < highest:
                second_highest = occurrences[letter]
            if third_highest < occurrences[letter] < second_highest:
                third_highest = occurrences[letter]
        three_highest = {}
        for letter in occurrences:
            if occurrences[letter] == highest:
                three_highest[letter] = highest
            if occurrences[letter] == second_highest:
                three_highest[letter] = second_highest
            if occurrences[letter] == third_highest:
                three_highest[letter] = third_highest
        return three_highest



if __name__ == "__main__":
    start_time = time.time()
    encrypted = 'FRRPU TIIYE AMIRN QLQVR BOKGK NSNQQ IUTTY IIYEA WIJTG LVILA ZWZKT ZCJQH IFNYI WQZXH RWZQW OHUTI KWNNQ YDLKA EOTUV XELMT SOSIX JSKPR BUXTI TBUXV BLNSX FJKNC HBLUK PDGUI IYEAM OJCXW FMJVM MAXYT XFLOL RRLAA JZAXT YYWFY NBIVH VYQIO SLPXH ZGYLH WGFSX LPSND UKVTR XPKSS VKOWM QKVCR TUUPR WQMWY XTYLQ XYYTR TJJGO OLMXV CPPSL KBSEI PMEGC RWZRI YDBGE BTMFP ZXVMF MGPVO OKZXX IGGFE SIBRX SEWTY OOOKS PKYFC ZIEYF DAXKG ARBIW KFWUA SLGLF NMIVH VVPTY IJNSX FJKNC HBLUK PDGUI IYEAM HVFDY CULJS EHHMX LRXBN OLVMR'
    encrypted = encrypted.replace(" ", "").lower()

    auto_key = AutoKey()

    cipher_numb = auto_key.numerically(encrypted)

    key = "buy"
    key_numb = auto_key.numerically(key)
    text = ""
    for i in range(round(len(encrypted)/len(key_numb))):
        number = auto_key.find_plaintext(key_numb, cipher_numb)
        key_numb = number
        text = auto_key.letters(number)
    print(text)
    end_time = time.time()


    freq = frequencies()
    occurrences = freq.find_frequencies(encrypted)
    print(freq.highest_frequency(occurrences))
