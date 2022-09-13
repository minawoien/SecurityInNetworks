# # Letters expressed numerically
# def numerically(encrypted):
#     numeric = []
#     for letter in encrypted:
#         numeric.append(ord(letter)-97)
#     return numeric

# # Numbers expressed as letters
# def letters(numbers):
#     text = ""
#     for numb in numbers:
#         text += chr(numb+97)
#     return text

# def decrypt(key, plain_text):
#     numbers = []
#     for i in range(len(key)):
#         if len(plain_text) > 0:
#             encrypted = plain_text[0]+key[i]
#             if encrypted > 25:
#                 print(encrypted, "før")
#                 encrypted = encrypted - 25
#                 print(encrypted, "etter")
#             numbers.append(encrypted)
#             plain_text.pop(0)
#     return numbers


# if __name__ == "__main__":
#     texten = "Hi my name is Mina and I am twenty years old I like swimming and skiing I study computer science at the University of Stavanger and have been there for three years I have just started my master degree and it is very difficult can anybody help me my boyfriend is very kind that tried to help me it helped a bit but I still have more to do in the code it is going to be some long nights before the assignment have its deadline"
#     texten = texten.replace(" ", "").lower()
#     text = numerically(texten)
#     keyy = "deceptive"
#     key = numerically(keyy)
#     cipher_text = ""
#     nxt_key = ""
#     #for i in range(len(keyy)):
#     nxt_key = texten
#     nxt_key = numerically(nxt_key)
#     print(nxt_key)
    
#     # number = decrypt(key, text)
#     # print(letters(number))
#     for x in range(round(len(text)/len(key))):
#         number = decrypt(key, text)
#         tall = (x+1)*len(key)
#         print("tallet mitt er ", tall)
#         key = nxt_key[tall:]
#         print(letters(key))
#         cipher_text += letters(number)
#     print(cipher_text)

ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def main():
    texten = "Hi my name is Mina and I am twenty years old I like swimming and skiing I study computer science at the University of Stavanger and have been there for three years I have just started my master degree and it is very difficult can anybody help me my boyfriend is very kind that tried to help me it helped a bit but I still have more to do in the code it is going to be some long nights before the assignment have its deadline"
    texten = texten.replace(" ", "").lower()
    print(texten)
    message = input('enter message:\n')
    key = input('enter your key:\n')
    mode = input('encrypt or decrypt\n')
    ## if len(key) < len(message):
        ## key = key[0:] + message[:100]
    #print(key)
    if mode == 'encrypt':
       cipher = encryptMessage(message, key)
    elif mode == 'decrypt':
       cipher = decryptMessage(message, key)
    #print(' message:',  (mode.title()))
    print(cipher)


## def encryptMessage (keys, messages):
##     return cipherMessage(keys, messages, 'encrypt')
def encryptMessage (messages, keys):  
    return cipherMessage(messages, keys, 'encrypt')


## def decryptMessage(keys,messages):
##     return cipherMessage(keys, messages, 'decrypt')
def decryptMessage(messages, keys):
    return cipherMessage(messages, keys, 'decrypt')


## def cipherMessage (keys, messages, mode):
def cipherMessage (messages, keys, mode):
    cipher = []
    k_index = 0
    key = keys.upper()
    for i in messages:
        text = ALPHA.find(i.upper())
        ## if text != -1:
        if mode == 'encrypt':
             text += ALPHA.find(key[k_index])
             key += i.upper()  # add current char to keystream

        elif mode == 'decrypt':
             text -= ALPHA.find(key[k_index])
             key += ALPHA[text]  # add current char to keystream
        text %= len(ALPHA)
        ## k_index += -1
        k_index += 1
        ## if k_index == len(key):
        ##     k_index = 0
        ## else:
        cipher.append(ALPHA[text])
    return ''.join(cipher)

if __name__ == "__main__":
    main()