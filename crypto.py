import string

Z_26_star = [1,3,5,7,9,11,15,17,19,21,23,25]
look_up_table = dict(zip(string.ascii_lowercase, range(0,27)))

class Affinecipher:

    def __init__(self, k1, k2, plText):
        self.k1 = k1
        self.k2 = k2
        self.plText = plText
        self._k1 = self.inverse(k1)[0]
    def inverse(self,value):
        return [x for x in Z_26_star if (value*x)%26 == 1]
    def encrypt(self):
        print(f"Plain text: {self.plText}\nk1: {self.k1}\nk2: {self.k2}")
        print(f"Plain text Z26 value: {[look_up_table[x] for x in self.plText]}")
        result = [(look_up_table[x]*self.k1+self.k2)%26 for x in self.plText]
        print(f"cipher text Z26 value: {result}")
        return "".join([list(look_up_table.keys())[list(look_up_table.values()).index(x)] for x in result])
    def decrypt(self):
        print(f"Cipher text: {self.plText}\nk1: {self.k1}\nk2: {self.k2}")
        print(f"Cipher text Z26 value: {[look_up_table[x] for x in self.plText]}")
        result = [self._k1*(look_up_table[x]-self.k2)%26 for x in self.plText]
        print(f"Plain text Z26 value: {result}")
        return "".join([list(look_up_table.keys())[list(look_up_table.values()).index(x)] for x in result])
        


class AutokeyCipher:
    
    def __init__(self, key=0, plTxt="affinecipher"):
        self.plTxt = plTxt
        self.key = key
    def key_generate(self):
        self.key_stream = [look_up_table[x] for x in self.plTxt]
        self.key_stream.insert(0,self.key)
        self.key_stream.pop()
    def encrypt(self):
        self.key_generate()
        result = [(look_up_table[self.plTxt[i]] + self.key_stream[i])%26 for i in range(0, len(self.plTxt))]
        print(f"Plain text: {self.plTxt}")
        print(f"Plain text Z26 value: {[look_up_table[x] for x in self.plTxt]}")
        print(f"Autokey: {[x for x in self.key_stream]}")
        print(f"Plain text Z26 value: {result}")
        return self.key_stream,"".join([list(look_up_table.keys())[list(look_up_table.values()).index(x)] for x in result])
    def decrypt(self, key, cipherTxt):
        self.key_generate()
        result = [(look_up_table[cipherTxt[i]] - key[i])%26 for i in range(0, len(cipherTxt))]
        print(f"Cipher text: {cipherTxt}")
        print(f"Cipher text Z26 value: {[look_up_table[x] for x in cipherTxt]}")
        print(f"Autokey: {[x for x in key]}")
        print(f"Cipher text Z26 value: {result}")
        return "".join([list(look_up_table.keys())[list(look_up_table.values()).index(x)] for x in result])


