from lab_1_hemming.source import (
    hemming_operations as ho,
    convert_operations as co,
    bit_operations as bo,
)


def main():
    bin_hello = co.text_to_int("binary")
    # norm_hello = co.int_to_text(bin_hello)
    # print(norm_hello)
    # print('binary')
    # print(bin(bin_hello))
    # # changed = bo.insert(bin_hello, 0)
    # # print(bin(changed))
    #
    # split_bin_hello = bo.split_bytes_by(bin_hello, 16)
    # # print([bin(x) for x in split_bin_hello])
    # # conacat_bin_hello = bo.concatenate_bytes_with_base(split_bin_hello, 16)
    # # print(co.int_to_text(conacat_bin_hello))
    # prepared = ho.prepare_check_bits(split_bin_hello[0])
    # # print(bin(int.from_bytes("bi".encode("ASCII"), "big")))
    # print(bin(split_bin_hello[0]))
    # result = ho.control_bits_calculation(prepared)
    # print(bin(result))
    # print([bin(x) for x in ho.encode("binary")])
    # print(bo.count_ones(7))
    # print(bo.remove_bit(65, 5))
    # bi = 'aa'
    # tmp = co.text_to_int(bi)
    # tmp = ho.prepare_check_bits(tmp)
    # # tmp = ho.control_bits_calculation(tmp)
    # tmp = ho.clear_control_bits(tmp)
    # tmp = co.int_to_text(tmp)
    # print(tmp)
    hemmig = ho.HemmingAlgorithm(16, 5)
    hemmig.prepare_check_bits(0b1111111)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
