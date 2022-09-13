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


class HemmingAlgorithm:
    """
    That class implements Hemming algorithm
    to encode and decode binary information

    Allows to choose any size of message  length
    by provide INFORMATION_BITS_COUNT and CONTROL_BITS_COUNT
    """
    INFORMATION_BITS_COUNT: int
    CONTROL_BITS_COUNT: int
    TOTAL_PIECE_LENGTH: int
    POWERS_OF_TWO: [int]
    CONTROL_VALUES_MASKS: [int]

    def __init__(self, information_bit_count: int, control_bit_count: int) -> None:
        self.INFORMATION_BITS_COUNT = information_bit_count
        self.CONTROL_BITS_COUNT = control_bit_count
        self.POWERS_OF_TWO = [2 ** x for x in range(control_bit_count)]
        self.TOTAL_PIECE_LENGTH = information_bit_count + control_bit_count
        self.CONTROL_VALUES_MASKS = [create_mask(x, self.TOTAL_PIECE_LENGTH) for x in self.POWERS_OF_TWO]

    def encode(self, data: str) -> [int]:
        """
        Encode string to list of int (binary information)
        :param data: str
        :return: [int]
        """
        return [
            self.control_bits_calculation(prepared)
            for prepared in [
                self.prepare_check_bits(bits)
                for bits in split_bytes_by(
                    text_to_int(data), self.INFORMATION_BITS_COUNT
                )
            ]
        ]

    def decode(self, bits_array: [int]) -> str:
        """
        Decode list of int to string

        :param bits_array: [int]
        :return: str
        """
        return int_to_text(
            concatenate_bytes_with_base(
                [
                    self.clear_control_bits(self.recover_corrupted_bit(obits, rbits))
                    for (obits, rbits) in zip(
                        bits_array,
                        [
                            self.control_bits_calculation(
                                self.prepare_check_bits(cbits)
                            )
                            for cbits in [
                                self.clear_control_bits(bits) for bits in bits_array
                            ]
                        ],
                    )
                ],
                self.INFORMATION_BITS_COUNT,
            )
        )

    def prepare_check_bits(self, bits: int) -> int:
        """
        Inserts zeros into binary number
            and returns new number
        :param bits: int
        :return: int
        """
        diff = self.INFORMATION_BITS_COUNT - bits.bit_length()
        for pos in self.POWERS_OF_TWO:
            diff += bits == (bits := insert(bits, pos - 1 - diff))
        return bits

    def control_bits_calculation(self, bits: int) -> int:
        """
        Calculate and set control bits values
        in one piece of message
        with TOTAL_PIECE_LENGTH
        :param bits: int
        :return: int
        """
        def len(x: int) -> int:
            return x.bit_length()
        discarded_zeros = self.TOTAL_PIECE_LENGTH - len(bits)
        _discarded_zeros = 0
        for (mask, pos) in zip(self.CONTROL_VALUES_MASKS, self.POWERS_OF_TWO):
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
                discarded_zeros = 0
                _discarded_zeros = pos - 1
            else:
                # shift control value to required pos and concatenate
                control_value = (
                        control_value << (self.TOTAL_PIECE_LENGTH - (pos - 1)) - 1
                )
            bits |= control_value
        return bits

    def clear_control_bits(self, bits: int) -> int:
        """
        Delete all control bits from piece of message
        :param bits: int
        :return: int
        """
        diff = self.TOTAL_PIECE_LENGTH - bits.bit_length()
        for pos in self.POWERS_OF_TWO:
            diff += bits.bit_length() - (
                bits := remove_bit(bits, pos - diff)
            ).bit_length()
        return bits

    def recover_corrupted_bit(self, origin_bits: int, recalculated_bits: int) -> int:
        """
        Compare control bits of received piece and recalculated piece
        Recover origin message if one of the bits was corrupted
        :param origin_bits: int
        :param recalculated_bits: int
        :return: int
        """
        if origin_bits == recalculated_bits:
            return origin_bits
        control_bits_mask = 0
        for x in range(self.TOTAL_PIECE_LENGTH + 1):
            control_bits_mask = (control_bits_mask << 1) + (x in self.POWERS_OF_TWO)
        diff = (origin_bits & control_bits_mask) ^ (
            recalculated_bits & control_bits_mask
        )
        corrupted_bit = 0
        while diff:
            corrupted_bit += self.TOTAL_PIECE_LENGTH - diff.bit_length() + 1
            diff = crop_left_bits(diff, 1)
        if origin_bits & (1 << diff):
            origin_bits &= (
                (1 << (self.TOTAL_PIECE_LENGTH - corrupted_bit))
                ^ ((1 << origin_bits.bit_length() + 1) - 1)
            )
        else:
            origin_bits |= (
                1 << (self.TOTAL_PIECE_LENGTH - corrupted_bit)
            )
        return origin_bits
