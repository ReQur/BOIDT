from dataclasses import dataclass
from functools import lru_cache


class StringIntConverter:
    def __init__(self, shift=10, split_by=7):
        self.splitter = 10**split_by+1
        self.shift = shift
        self.chars = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя "

    @lru_cache
    def convert(self, x):
        if isinstance(x, int):
            return self.chars[x - self.shift]
        elif isinstance(x, str):
            return self.chars.index(x) + self.shift
        else:
            raise

    def encode(self, string: str) -> [int]:
        string = string.lower()
        res = []
        n = 0
        for c in string:
            n *= 100
            n += self.convert(c)
            if n > self.splitter:
                res.append(int(str(n)[0:7]))
                n = int(str(n)[7:])
        res.append(n)
        res.reverse()
        return res

    def decode(self, nums: [int]) -> str:
        res = ""
        last = 0
        for num in nums:
            if last:
                num *= 10
                num += last
            while num % 100 > 9:
                res = self.convert(num % 100) + res
                num //= 100
            last = num
        return res
