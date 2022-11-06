import numpy as np
from PIL import Image
from collections.abc import Iterable
from converter import bit_acii_generator, merge_bits_to_ascii


width = 600
height = 400

_cur = []


def flatten(l):
    global _cur
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            _cur = el
            yield el


def nested(l):
    triplet = []
    triples = []
    res = []
    for el in l:
        triplet.append(el)
        if len(triplet) == 3:
            triples.append(triplet)
            triplet = []
            if len(triples) == width:
                res.append(triples)
                triples = []

    return res


def encode(image, text):
    res = []
    img = np.array(Image.open(image))
    img_bits = flatten(img)
    mes_bits = bit_acii_generator(text)
    for el, bit in zip(img_bits, mes_bits):
        el >>= 1
        el <<= 1
        el |= bit
        res.append(el)

    res.append(_cur)
    for el in img_bits:
        res.append(el)

    encoded_image = nested(res)
    encoded_image = np.array(encoded_image)
    _img = Image.fromarray(encoded_image.astype(np.uint8))
    _img.save(image[:-4]+'-encoded.bmp')


def decode(image, text_length=0):
    img = np.array(Image.open(image))
    img_bits = flatten(img)
    mes_bits = []
    for el in img_bits:
        mes_bits.append(el&1)

    res = merge_bits_to_ascii(mes_bits)
    if text_length:
        res = res[:text_length]

    return res

# _new_image = nested(list(flatten(img)))
# _img = Image.fromarray(np.array(_new_image))
# _img.save('./DSC_0163-copy.bmp')
