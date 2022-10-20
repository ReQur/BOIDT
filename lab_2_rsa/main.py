from converter import StringIntConverter

P, G, SHIFT = 3163, 5869, 10


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x


def get_bits(number):
    while number:
        yield number % 2
        number >>= 1


def coding(e, c, n):
    w = 1
    u = c
    for bit in get_bits(e):
        if bit:
            w = (w*u) % n
        u = (u**2) % n
    return w


def main():
    n = P*G
    eil_exp = (P-1)*(G-1)
    decode_key = 65537
    # print(extended_gcd(decode_key, eil_exp))
    # print(extended_gcd(7, 33))
    encode_key = [x for x in extended_gcd(decode_key, eil_exp)
                  if (x*decode_key) % eil_exp == 1 and abs(x*decode_key) != 1][0]

    converter = StringIntConverter()
    encoded = converter.encode("студент хабибуллин данил дамирович")
    print(encoded)

    rsa_encoded = []

    for c in encoded:
        rsa_encoded.append(coding(encode_key, c, n))

    encoded = []
    for c in rsa_encoded:
        encoded.append(coding(decode_key, c, n))

    print(converter.decode(encoded))



# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
