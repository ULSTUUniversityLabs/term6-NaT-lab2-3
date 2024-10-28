import struct

def F(x, y, z):
    return (x & y) | (~x & z)

def G(x, y, z):
    return (x & y) | (x & z) | (y & z)

def H(x, y, z):
    return x ^ y ^ z

def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

class MD4:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.A = 0x67452301
        self.B = 0xEFCDAB89
        self.C = 0x98BADCFE
        self.D = 0x10325476
        self._message = b''
        self._message_len = 0

    def _process_block(self, block):
        X = list(struct.unpack('<16I', block))
        A, B, C, D = self.A, self.B, self.C, self.D

        A = left_rotate(A + F(B, C, D) + X[0], 3)
        D = left_rotate(D + F(A, B, C) + X[1], 7)
        C = left_rotate(C + F(D, A, B) + X[2], 11)
        B = left_rotate(B + F(C, D, A) + X[3], 19)

        A = left_rotate(A + F(B, C, D) + X[4], 3)
        D = left_rotate(D + F(A, B, C) + X[5], 7)
        C = left_rotate(C + F(D, A, B) + X[6], 11)
        B = left_rotate(B + F(C, D, A) + X[7], 19)

        A = left_rotate(A + F(B, C, D) + X[8], 3)
        D = left_rotate(D + F(A, B, C) + X[9], 7)
        C = left_rotate(C + F(D, A, B) + X[10], 11)
        B = left_rotate(B + F(C, D, A) + X[11], 19)

        A = left_rotate(A + F(B, C, D) + X[12], 3)
        D = left_rotate(D + F(A, B, C) + X[13], 7)
        C = left_rotate(C + F(D, A, B) + X[14], 11)
        B = left_rotate(B + F(C, D, A) + X[15], 19)

        # Раунд 2
        A = left_rotate(A + G(B, C, D) + X[0] + 0x5A827999, 3)
        D = left_rotate(D + G(A, B, C) + X[4] + 0x5A827999, 5)
        C = left_rotate(C + G(D, A, B) + X[8] + 0x5A827999, 9)
        B = left_rotate(B + G(C, D, A) + X[12] + 0x5A827999, 13)

        A = left_rotate(A + G(B, C, D) + X[1] + 0x5A827999, 3)
        D = left_rotate(D + G(A, B, C) + X[5] + 0x5A827999, 5)
        C = left_rotate(C + G(D, A, B) + X[9] + 0x5A827999, 9)
        B = left_rotate(B + G(C, D, A) + X[13] + 0x5A827999, 13)

        A = left_rotate(A + G(B, C, D) + X[2] + 0x5A827999, 3)
        D = left_rotate(D + G(A, B, C) + X[6] + 0x5A827999, 5)
        C = left_rotate(C + G(D, A, B) + X[10] + 0x5A827999, 9)
        B = left_rotate(B + G(C, D, A) + X[14] + 0x5A827999, 13)

        A = left_rotate(A + G(B, C, D) + X[3] + 0x5A827999, 3)
        D = left_rotate(D + G(A, B, C) + X[7] + 0x5A827999, 5)
        C = left_rotate(C + G(D, A, B) + X[11] + 0x5A827999, 9)
        B = left_rotate(B + G(C, D, A) + X[15] + 0x5A827999, 13)

        # Раунд 3
        A = left_rotate(A + H(B, C, D) + X[0] + 0x6ED9EBA1, 3)
        D = left_rotate(D + H(A, B, C) + X[8] + 0x6ED9EBA1, 9)
        C = left_rotate(C + H(D, A, B) + X[4] + 0x6ED9EBA1, 11)
        B = left_rotate(B + H(C, D, A) + X[12] + 0x6ED9EBA1, 15)

        A = left_rotate(A + H(B, C, D) + X[2] + 0x6ED9EBA1, 3)
        D = left_rotate(D + H(A, B, C) + X[10] + 0x6ED9EBA1, 9)
        C = left_rotate(C + H(D, A, B) + X[6] + 0x6ED9EBA1, 11)
        B = left_rotate(B + H(C, D, A) + X[14] + 0x6ED9EBA1, 15)

        A = left_rotate(A + H(B, C, D) + X[1] + 0x6ED9EBA1, 3)
        D = left_rotate(D + H(A, B, C) + X[9] + 0x6ED9EBA1, 9)
        C = left_rotate(C + H(D, A, B) + X[5] + 0x6ED9EBA1, 11)
        B = left_rotate(B + H(C, D, A) + X[13] + 0x6ED9EBA1, 15)

        A = left_rotate(A + H(B, C, D) + X[3] + 0x6ED9EBA1, 3)
        D = left_rotate(D + H(A, B, C) + X[11] + 0x6ED9EBA1, 9)
        C = left_rotate(C + H(D, A, B) + X[7] + 0x6ED9EBA1, 11)
        B = left_rotate(B + H(C, D, A) + X[15] + 0x6ED9EBA1, 15)

        self.A = (self.A + A) & 0xFFFFFFFF
        self.B = (self.B + B) & 0xFFFFFFFF
        self.C = (self.C + C) & 0xFFFFFFFF
        self.D = (self.D + D) & 0xFFFFFFFF

    def _pad_message(self, message):
        original_length = len(message) * 8
        message += b'\x80'
        message += b'\x00' * ((56 - len(message) % 64) % 64)
        message += struct.pack('<Q', original_length)
        return message

    def update(self, message):
        self._message = self._pad_message(message)
        for i in range(0, len(self._message), 64):
            self._process_block(self._message[i:i + 64])

    def digest(self):
        return struct.pack('<4I', self.A, self.B, self.C, self.D)

    def hexdigest(self):
        return ''.join(f'{value:08x}' for value in struct.unpack('<4I', self.digest()))

    def to_hash(self, text):
        self.update(text.encode('utf-8'))
        h = self.hexdigest()
        self.reset()
        return h