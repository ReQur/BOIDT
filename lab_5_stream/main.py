from md import md
from converter import SIConverter


MESSAGE = "This message secured by stream encoding"
SEED = 1100

BUFFER = []

conv = SIConverter()


def encode(seed, message):
    rnd = md(seed)
    text_bits = conv.bit_acii_generator(message)
    for bit, key in zip(text_bits, rnd):
        BUFFER.append(bit ^ key)


def decode(seed, buffer):
    rnd = md(seed)
    decoded_buff: list[int] = []
    for bit, key in zip(buffer, rnd):
        decoded_buff.append(bit ^ key)

    text = conv.merge_bits_to_ascii(decoded_buff)
    print(text)


encode(SEED, MESSAGE)
decode(SEED, BUFFER)