import binascii

ENCODING = "ASCII"
BYTE_ORDER = "big"


def bit_acii_generator(text_file: str):
    with open(text_file, 'r') as file:
        text = file.read()
        for c in text:
            num = int.from_bytes(c.encode(ENCODING), BYTE_ORDER)
            for i in range(8):
                yield num & 0b1
                num >>= 1


def int_to_text(bits: int) -> str:
    return _int_to_bytes(bits).decode(ENCODING)


def _int_to_bytes(i) -> bytes:
    hex_string = "%x" % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


def merge_bits_to_ascii(bits: list):
    bits.reverse()
    res = ''
    while bits:
        char, bits = bits[-8:], bits[:-8]
        try:
            res += int_to_text(int(''.join([str(b) for b in char]), 2))
        except:
            break
    return res
