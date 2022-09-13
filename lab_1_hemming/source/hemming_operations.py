from math import sqrt

from .bit_operations import (
    insert,
    create_mask,
    crop_left_bits,
    split_bytes_by,
    count_ones,
    remove_bit,
    concatenate_bytes_with_base,
)
from .convert_operations import text_to_int, int_to_text

BASE = 16
BASE_WITH_CONTROL = BASE + int(sqrt(BASE) + 1)
POWERS_OF_TWO = [2 ** x for x in range(int(sqrt(BASE) + 1))]  # 1, 2, 4, ..., BASE
# BASE = 11
# BASE_WITH_CONTROL = 15
# POWERS_OF_TWO = [1, 2, 4, 8]


def encode(data: str) -> [int]:
    return [
        control_bits_calculation(prepared)
        for prepared in [
            prepare_check_bits(bits) for bits in split_bytes_by(text_to_int(data), BASE)
        ]
    ]


def decode(bits_array: [int]) -> str:
    return int_to_text(
        concatenate_bytes_with_base(
            [
                clear_control_bits(recover_corrupted_bit(obits, rbits))
                for (obits, rbits) in zip(
                    bits_array,
                    [
                        control_bits_calculation(prepare_check_bits(cbits))
                        for cbits in [clear_control_bits(bits) for bits in bits_array]
                    ],
                )
            ],
            BASE,
        )
    )


def prepare_check_bits(bits: int) -> int:
    """
    Inserts zeros into binary number
        and returns new number
    :param bits: int
    :return: int
    """
    diff = BASE - bits.bit_length()
    for pos in POWERS_OF_TWO:
        diff += bits == (bits := insert(bits, pos - 1 - diff))
    return bits


def control_bits_calculation(bits: int) -> int:
    def len(x: int) -> int:
        return x.bit_length()

    masks = [create_mask(x, BASE_WITH_CONTROL) for x in POWERS_OF_TWO]
    discarded_zeros = BASE_WITH_CONTROL - len(bits)
    _discarded_zeros = 0
    for (mask, pos) in zip(masks, POWERS_OF_TWO):
        control_value = (
            count_ones(
                crop_left_bits(bits, pos - 1 - _discarded_zeros)
                & mask >> (len(mask) - (len(bits) - (pos - 1 - _discarded_zeros)))
            )
            % 2
        )
        # skip insertion if the control value is 0
        if not control_value:
            continue
        if pos < discarded_zeros:
            # shift control bit to the left given that
            # we need to place zeros after control bite
            # also shift to the len of bits for concatenation
            control_value = control_value << discarded_zeros - pos + len(bits)
            bits = control_value | bits
            discarded_zeros = 0
            _discarded_zeros = pos - 1
        else:
            # shift control value to required pos and concatenate
            control_value = control_value << (BASE_WITH_CONTROL - (pos - 1)) - 1
            bits = bits | control_value
    return bits


def clear_control_bits(bits: int):
    diff = BASE_WITH_CONTROL - bits.bit_length()
    for pos in POWERS_OF_TWO:
        diff += bits.bit_length() - (
            bits := remove_bit(bits, pos - diff)
        ).bit_length()
    return bits


def recover_corrupted_bit(origin_bits: int, recalculated_bits: int) -> int:
    if origin_bits == recalculated_bits:
        return origin_bits
    control_bits_mask = 0
    for x in range(BASE_WITH_CONTROL + 1):
        control_bits_mask = (control_bits_mask << 1) + (x in POWERS_OF_TWO)
    diff = (origin_bits & control_bits_mask) ^ (recalculated_bits & control_bits_mask)
    corrupted_bit = 0
    while diff:
        corrupted_bit += BASE_WITH_CONTROL - diff.bit_length() + 1
        diff = crop_left_bits(diff, 1)
    if origin_bits & (1 << diff):
        origin_bits = origin_bits & (
            (1 << (BASE_WITH_CONTROL - corrupted_bit))
            ^ ((1 << origin_bits.bit_length() + 1) - 1)
        )
    else:
        origin_bits = origin_bits | (1 << (BASE_WITH_CONTROL - corrupted_bit))
    return origin_bits
