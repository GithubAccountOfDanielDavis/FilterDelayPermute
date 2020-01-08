#!/usr/bin/python3
#delay-filter-permute hashing
#larsupilami73

import numpy as np

#the secret...good luck!
#the_secret = b'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

#hints
# Commented these two lines out
#print(len(the_secret)) #returns 40
#print(the_secret.isascii()) # returns True


#a 256-entry permutation table
permlookuptable = np.array([228,   6,  79, 206, 117, 185, 242, 167,   9,  30, 180, 222, 230,
       217, 136,  68, 199,  15,  96,  24, 235,  19, 120, 152,  33, 124,
       253, 208,  10, 164, 184,  97, 148, 190, 223,  25,  86,  18,  75,
       137, 196, 176, 239, 181,  45,  66,  16,  67, 215, 201, 177,  38,
       143,  84,  55, 220, 104, 139, 127,  60, 101, 172, 245, 126, 225,
       144, 108, 178,  73, 114, 158,  69, 141, 109, 115, 246, 113, 243,
        90,  29, 170,  82, 111,   5,  56, 132, 154, 162,  65, 186,  85,
       219, 237,  31,  12,  35,  28,  42, 112,  22, 125,  93, 173, 251,
        51, 240,  95, 146, 204,  76,  41, 119, 155,  78, 150,  26, 247,
       168, 118, 193, 140,   0,   2,  77,  46, 100, 205, 159, 183, 254,
        98,  36,  61, 200, 142,  11, 250, 224,  27, 231,   4, 122,  32,
       147, 182, 138,  62, 135, 128, 232, 194,  70, 197,  64,  44, 165,
       156,  40, 123, 153,  23, 192, 249,  81,  39, 244,  47,  94, 195,
       161,  43, 145, 175,   3, 105,  53, 133, 233, 198, 238,  49, 163,
        80,  34, 211,   7, 171, 216, 110,  91,  83, 229, 234,  89,   8,
        13,  59, 221, 131,  17, 166,  72, 226, 134, 209, 236,  63,  54,
       107,  50, 212, 174, 213, 189, 252, 207, 227, 169,  58, 218,  48,
        88,  21,  57, 203, 160, 248, 187, 191, 129,  37, 157, 241,   1,
        52, 149, 130, 151, 103,  99, 116,  87, 202,  74, 214, 210, 121,
       255,  20, 188,  71, 106,  14,  92, 179, 102])


#a simple delay line class
class Delay:
    def __init__(self, n=512, dtype='uint16'):
        self.d = np.zeros(n, dtype=dtype)
        self.index = 0
        self.n = n

    def advance(self, x):
        self.d[self.index] = x
        self.index += 1
        if self.index >= self.n:
            self.index = 0
        return self.d[self.index]

    def clear(self):
        self.d = self.d * 0
        self.index = 0

    def get(self):
        return self.d[self.index]

def encode (secret: bytes): # Wrapped these lines in a function for testing
    #make a delay line
    N = 512
    delay = Delay(N)

    #shift the ascii values of the secret in the delay line
    for c in secret:
        delay.advance(c)

    #delay-filter-permute
    state, perm = 0,0
    for k in range(N*20):
        state = state - (state>>4) + (perm<<4)
        perm = permlookuptable[delay.advance((state>>3)  & 0x00FF)]

    return state, delay.d

#the output
if __name__ == "__main__": # Added conditional console printing
    print("This is the original challenge file provided larsupilami73.")
    print("It has been unaltered as much as possible and all changes are noted")
    print("in comments, aside from the text here, which is pretty")
    print("self-evident. The following is the output of the original file:")
    print()
    state, delay_line = encode(b'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    print('State: {}'.format(state))
    print()
    print('Delay line:\n', delay_line)

"""
The challenge: the short Python code found here produces this as output:

State: 27466

Delay line:
[ 94 204 211 244 109 120 235  34 176  65 155 165 247 210 177 232  35  15
 44  43 253 117  34 106 251 145 188 165  30 112  81 208  43  11  60 228
252 138 176 105 244  45 244 159 253  92  64 126 142 191  49 168  64  22
166 234 113 164 248 131 142  82 106   2  46  21 104 139 124 135 152 133
223 195  11 144  73  36 186 205  26 230 174  87 212 104 252 184  55 221
237  45 234  63  53   2 190 254   2  32 154 217 109 204  38  15 232 116
169  58 122 159 115 132   8 147  94  50   9  80 191  46  69 118 217  56
250 114 241 212 209  86 227 177 106  23  26 218 230 252 252 174 214  36
 20 173  10   5  13 170 190  28 130 110 185   0 204 153 223  47  81 106
223 137 225  47 152 132 222  64 118  21 165  61 189 192   6 239  30 115
 77  51  26 204  87  14 155  33  41  13  36 210  65 231   6  24  26 171
238  65 219 220  10  91 226  58  46  23  40 235  73  88 127 141   6 158
196 127 118  12 189 214 158  26 221  19 174 219 239 101 148  99 187  87
  2  50   1 221 181  76  33  89 221 218 156 148 157 241 172  34  85 130
174 247 198 215 188  16 253  82  96   0  80  13 205 186  58 195  53  29
226 139 103 242 155 212  50  87 144 149  34  78  35 211  87 174 223  49
240 175  28 173  64 252 146   9  11 176 157  89   0 100 167 159  63  65
101 111 224  86  51  22 142  81 124  51 204 145 102 255  38  79   6  76
239  68 228  40 125  60 106 169 165 202 126 136 159  96 174 103 214 189
189 121 140 159 231 149 148  90 173  28  18 239  20 157   9  63  47 126
196  28 128  28 214 117   8 171  31 151 245  62 118  23 196 177 152   7
188 239 204  63 227 205 152  85 132 169  85  58  12  59  88 134 158 236
 69 155 183 172  57  60 118  56 131 185  81 248   7 234 178 165 120   9
110   8 137 177 100 195  85 142  93 231  19 198  15  71 254 244  89   6
 39 147 116 234 232 247  24 146 151 206 245 146 113  66 136 157 139 133
 94 147 103 199 249 237 254 201 194 142 223 179  76 179 186 121   5 195
155 141 216 201  88 199 234  48  63 133  93 247 236 151 209 206 230 191
167  39 235  92 154 163 196  26  25  13 168  54  22 251  73 117 150 220
243 229   5 221  61  95 154  32]

...given the correct (hint) 40-byte ascii secret sentence. Can you find what it is?

"""
