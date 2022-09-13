import binascii


def text_to_int(text: str, encoding="ASCII") -> int:
    return int.from_bytes(text.encode(encoding), "big")


def int_to_text(bits, encoding="ASCII", errors="surrogatepass") -> str:
    return _int_to_bytes(bits).decode(encoding, errors)


def _int_to_bytes(i) -> bytes:
    hex_string = "%x" % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))
