import binascii


class SIConverter:
    ENCODING: str
    BYTE_ORDER: str

    def __init__(self, encoding="ASCII", byte_orded="big"):
        self.ENCODING = encoding
        self.BYTE_ORDER = byte_orded

    def bit_acii_generator(self, text_file: str):
        with open(text_file, 'r') as file:
            text = file.read()
            for c in text:
                num = int.from_bytes(c.encode(self.ENCODING), self.BYTE_ORDER)
                for i in range(8):
                    yield num & 0b1
                    num >>= 1

    def merge_bits_to_ascii(self, bits: list):
        res = ''
        char = []
        for bit in bits:
            char.insert(0, bit)
            if len(char) == 8:
                try:
                    res += self.int_to_text(int(''.join([str(b) for b in char]), 2))
                except:
                    break
                else:
                    char = []
        return res

    def int_to_text(self, bits: int) -> str:
        return self._int_to_bytes(bits).decode(self.ENCODING)

    def _int_to_bytes(self, i) -> bytes:
        hex_string = "%x" % i
        n = len(hex_string)
        return binascii.unhexlify(hex_string.zfill(n + (n & 1)))
