from copy import copy

from binary_tree import Leave, Node, get_haffman_codes, build_tree

inpt_str = "aadafagahahaajaka"

freqs = list(set([Leave(inpt_str.count(c), c) for c in inpt_str]))
freqs.sort(key=lambda x: x.freq)
chars = copy(freqs)
print(chars)

# encode part
chars = build_tree(chars)
encode_map = get_haffman_codes(chars[0])
print(encode_map)
encoded = ''.join(encode_map[c] for c in inpt_str)
print(encoded)

# decode part
chars = copy(freqs)
chars = build_tree(chars)
encode_map = get_haffman_codes(chars[0])
decode_map = dict(zip(encode_map.values(), encode_map.keys()))
word = ''
decoded = ''
while encoded:
    word += encoded[0]
    encoded = encoded[1:]
    try:
        decoded += decode_map[word]
    except KeyError:
        pass
    else:
        word = ''

print(decoded)

