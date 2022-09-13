def split_bytes_by(bits: int, base: int) -> list[int]:
    split_bytes = []
    mask = (1 << base) - 1  # 1111...1111
    while bits:
        split_bytes.append(bits & mask)
        bits = bits >> base
    split_bytes.reverse()
    return split_bytes


def concatenate_bytes_with_base(bits_array: [int], base: int):
    result = 0
    for bits in bits_array:
        result = result << base | bits

    return result


def insert(bits: int, bit: int) -> int:
    length = bits.bit_length()
    if bit > length:
        raise ValueError("argument out of range")
    right = bits & ((1 << length - bit) - 1)
    return ((bits - right) << 1) + right


def create_mask(n, base) -> int:
    mask = 0
    while mask.bit_length() < base:
        for _ in range(n):
            mask = (mask << 1) + 1
        mask = mask << n
    return mask


def crop_left_bits(bits: int, n: int) -> int:
    return bits & ((2 ** bits.bit_length() - 1) >> n)


def count_ones(bits: int) -> int:
    res = 0
    while bits:
        res += bits & 1
        bits = bits >> 1
    return res


def remove_bit(bits: int, n: int) -> int:
    if n < 0:
        return bits
    source_len = bits.bit_length()
    n = source_len - n
    right = bits & ((1 << n) - 1)
    left = bits >> 1 + n
    return left << (source_len - left.bit_length() - 1) | right
