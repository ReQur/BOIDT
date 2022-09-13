import binascii


class StringIntConverter:
    """
    That class converts string to int and int to string
    """
    ENCODING: str
    BYTE_ORDER: str

    def __init__(self, encoding="ASCII", byte_orded="big"):
        self.ENCODING = encoding
        self.BYTE_ORDER = byte_orded

    def text_to_int(self, text: str) -> int:
        return int.from_bytes(text.encode(self.ENCODING), self.BYTE_ORDER)

    def int_to_text(self, bits: int) -> str:
        return self._int_to_bytes(bits).decode(self.ENCODING)

    def _int_to_bytes(self, i) -> bytes:
        hex_string = "%x" % i
        n = len(hex_string)
        return binascii.unhexlify(hex_string.zfill(n + (n & 1)))
