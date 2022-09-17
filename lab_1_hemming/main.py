from lab_1_hemming.source import (
    hemming_operations as ho,
    convert_operations as co,
    bit_operations as bo,
)


def main():
    bi = "ry"
    hemming = ho.HemmingAlgorithm(16, 5)
    converter = co.StringIntConverter()
    int_bi = converter.text_to_int(bi)
    print("integer bi " + bin(int_bi))
    prepared_bi = hemming.prepare_check_bits(int_bi)
    #print("prepared bi " + bin(prepared_bi))
    calculated_bi = hemming.control_bits_calculation(prepared_bi)
    print("calculated bi " + bin(calculated_bi))
    corrupted_bi = calculated_bi & 0b111111111111011111111
    print("corrupted bi" + bin(corrupted_bi))
    cleared_bi = hemming.clear_control_bits(corrupted_bi)
    print("corrupted cleared bi " + bin(cleared_bi))
    recalculated_bi = hemming.control_bits_calculation(hemming.prepare_check_bits(cleared_bi))
    print("recalculated bi "+ bin(recalculated_bi))
    recovered_bi = hemming.recover_corrupted_bit(corrupted_bi, recalculated_bi)
    print("recovered bi " + bin(recovered_bi))
    print(converter.int_to_text(hemming.clear_control_bits(recovered_bi)))


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
