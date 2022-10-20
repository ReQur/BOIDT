from binary_tree import Leave, Node, get_haffman_codes

inpt_str = "beep boop beer!"

chars = list(set([Leave(inpt_str.count(c), c) for c in inpt_str]))
chars.sort(key=lambda x: x.freq)
print(chars)

while len(chars) != 1:
    l, r, *chars = chars
    node = Node(l.freq + r.freq, l, r)
    chars.append(node)
    chars.sort(key=lambda x: x.freq)

encode_map = get_haffman_codes(chars[0])
decode_map = dict(zip(encode_map.values(), encode_map.keys()))
encoded = ''.join(encode_map[c] for c in inpt_str)
print(encoded)

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

