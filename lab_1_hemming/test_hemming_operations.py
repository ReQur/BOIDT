import pytest
import source.hemming_operations as hemming


def test_encode():
    assert hemming.encode("binary") == [
        0b10111010010011001001,
        0b110111011110011100001,
        0b111110010011111001,
    ]


@pytest.mark.parametrize(
    "origin, transformed",
    [
        (0b110001001101001, 0b10111010010011001001),
        (0b110111001100001, 0b110111011110011100001),
        (0b111001001111001, 0b111110010011111001),
    ],
)
def test_control_bits_calculation(origin, transformed):
    assert transformed == hemming.control_bits_calculation(
        hemming.prepare_check_bits(origin)
    ), f"\n{bin(transformed)}\n{bin(hemming.control_bits_calculation(hemming.prepare_check_bits(origin)))}"


def test_add_clear_control_pos():
    n: int = 0b10101011100101
    cn = hemming.prepare_check_bits(n)
    assert n == hemming.clear_control_bits(cn)


def test_filled_control_clear_pos():
    n: int = 0b10101011100101
    cn = hemming.prepare_check_bits(n)
    cn = hemming.control_bits_calculation(cn)
    assert n == hemming.clear_control_bits(cn)


def test_decode_encode_without_corruption():
    word = "binary"
    decoded_word = hemming.encode(word)
    encoded_word = hemming.decode(decoded_word)
    assert word == encoded_word
