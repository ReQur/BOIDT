P, G, SHIFT = 3163, 5869, 10


def gcd_rem_division(num1, num2):
    while num1 != 0 and num2 != 0:
        if num1 >= num2:
            num1 %= num2
        else:
            num2 %= num1
    return num1 or num2


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x


def coding(e, c, n):
    w = 1
    u = c

def main():
    n = P*G
    eil_exp = (P-1)*(G-1)
    d = 65537
    e = [x for x in extended_gcd(d, eil_exp) if (x*d) % eil_exp == 1][0]


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
