import numpy as np
from PIL import Image
from collections.abc import Iterable
from converter import SIConverter


class LSB:

    width: int
    converter: SIConverter

    def __init__(self):
        self.converter = SIConverter()
        self._cur = []

    def flatten(self, l):
        for el in l:
            if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
                yield from self.flatten(el)
            else:
                self._cur = el
                yield el

    def nested(self, l):
        triplet = []
        triples = []
        res = []
        for el in l:
            triplet.append(el)
            if len(triplet) == 3:
                triples.append(triplet)
                triplet = []
                if len(triples) == self.width:
                    res.append(triples)
                    triples = []

        return res

    def encode(self, image, text):
        res = []
        img = np.array(Image.open(image))
        self.width = len(image[0])
        img_bits = self.flatten(img)
        mes_bits = self.converter.bit_acii_generator(text)
        for el, bit in zip(img_bits, mes_bits):
            el >>= 1
            el <<= 1
            el |= bit
            res.append(el)

        res.append(self._cur)
        for el in img_bits:
            res.append(el)

        encoded_image = self.nested(res)
        encoded_image = np.array(encoded_image)
        _img = Image.fromarray(encoded_image.astype(np.uint8))
        _img.save(image[:-4]+'-encoded.bmp')

    def decode(self, image, text_length=0):
        img = np.array(Image.open(image))
        img_bits = self.flatten(img)
        mes_bits = []
        for el in img_bits:
            mes_bits.append(el&1)

        res = self.converter.merge_bits_to_ascii(mes_bits)
        if text_length:
            res = res[:text_length]

        return res
