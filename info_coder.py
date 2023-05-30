class InfoCoder:
    def __init__(self):
        self.data = None
        self.encoded = ""
        self.decoded = ""

    def set_file(self, bytes):
        self.data = bytes.read()

    def encode_info(self, key):
        data = b""
        for shift, i in enumerate(self.data):
            char = key[shift % len(key)]
            charsum = sum([int(j) for j in str(ord(char))])
            byte = bin(i)[2:]
            byte = '0' * (8 - len(byte)) + byte
            new_byte_shift = (bin(ord(char)).count('1') + charsum + shift) % 8
            new_byte = ''.join([byte[(j * 2 + new_byte_shift) % 8] for j in range(4)] +
                       [byte[(1 + j * 2 + new_byte_shift) % 8] for j in range(4)])
            data += int(new_byte, 2).to_bytes(1, 'big')
        self.encoded = data

    def decode_info(self, key):
        data = b""
        for shift, i in enumerate(range(len(self.data))):
            char = key[shift % len(key)]
            charsum = sum([int(j) for j in str(ord(char))])
            byte = bin(self.data[i])[2:]
            byte = '0' * (8 - len(byte)) + byte
            new_byte_shift = (bin(ord(char)).count('1') + charsum + shift) % 8
            new_byte = [" "] * 8
            for j in range(4):
                new_byte[(j * 2 + new_byte_shift) % 8] = byte[j]
                new_byte[(1 + j * 2 + new_byte_shift) % 8] = byte[j + 4]
            res = int(''.join(new_byte), 2)
            data += res.to_bytes(1, 'big')
        self.decoded = data

    def get_locked(self):
        return self.encoded

    def get_unlocked(self):
        return self.decoded