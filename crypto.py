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


def Init_Permutation(inputBlock):
    initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]
    inputAsBin = f"{int(inputBlock, 16):064b}"
    print(f"Input Hex: {inputBlock}")
    print(f"Input Bin: {inputAsBin}")
    result = "".join([inputAsBin[x - 1] for x in initial_perm])
    return result

# result = Init_Permutation("0200000000400040")
# print(f"Result after initial permutation: {result}")

def Straight_P_Box(inputVal):
    p_box = [ 16,  7, 20, 21,
        29, 12, 28, 17,
         1, 15, 23, 26,
         5, 18, 31, 10,
         2,  8, 24, 14,
        32, 27,  3,  9,
        19, 13, 30,  6,
        22, 11,  4, 25 ]
    inputAsBin = f"{int(inputVal, 16):032b}"
    print(f"Input Hex: {inputVal}")
    print(f"Input Bin: {inputAsBin}")
    result = "".join([inputAsBin[x - 1] for x in p_box])
    return result

def Sbox(inputVal):
    S_box = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
          [ 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
          [ 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
          [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 ]],
            
         [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
           [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 ]],
   
         [ [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
           [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
           [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ]],
       
          [ [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
           [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
           [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14] ],
        
          [ [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
           [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
           [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ]],
       
         [ [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
           [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13] ],
         
          [ [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
           [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12] ],
        
         [ [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11] ] ]
    numIter = int(len(inputVal)/6)
    result= []
    for i in range(0,numIter):
        valSpec = inputVal[i*6:i*6+6]
        rowIndex = int(valSpec[0] + valSpec[5], 2)
        colIndex = int(valSpec[1:5],2)
        result.append(S_box[i][rowIndex][colIndex])
    print(f"Kết quả từ bảng S-box decimal{result}")
    return "".join([ f"{x:04b}" for x in result])




