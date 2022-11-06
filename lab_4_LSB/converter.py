import binascii


class SIConverter:
    ENCODING: str
    BYTE_ORDER: str

    def __init__(self, measure, encoding="ASCII", byte_orded="big"):
        self.ENCODING = encoding
        self.BYTE_ORDER = byte_orded
        self.measure = measure

    def bit_acii_generator(self, text_file: str):
        _gen = self._bit_acii_generator(text_file)
        while True:
            tmp = 0
            try:
                for i in range(self.measure):
                    tmp <<= 1
                    tmp |= next(_gen)
            except StopIteration:
                break
            else:
                yield tmp

    def _bit_acii_generator(self, text_file: str):
        with open(text_file, 'r') as file:
            text = file.read()
            for c in text:
                num = int.from_bytes(c.encode(self.ENCODING), self.BYTE_ORDER)
                for i in range(8):
                    yield num & 0b1
                    num >>= 1

    def merge_bits_to_ascii(self, bits: list):
        bits.reverse()
        res = ''
        img_length = len(bits)
        _percent = 0
        prev_percent = -1
        process_counter = 0
        while bits:
            char, bits = bits[-8:], bits[:-8]
            try:
                res += self.int_to_text(int(''.join([str(b) for b in char]), 2))
                process_counter += 1
                _percent = int((process_counter / img_length) * 100)
                if _percent != prev_percent:
                    print('text is {}% prepared'.format(_percent))
                    prev_percent = _percent
            except:
                break
        return res

    def int_to_text(self, bits: int) -> str:
        return self._int_to_bytes(bits).decode(self.ENCODING)

    def _int_to_bytes(self, i) -> bytes:
        hex_string = "%x" % i
        n = len(hex_string)
        return binascii.unhexlify(hex_string.zfill(n + (n & 1)))
