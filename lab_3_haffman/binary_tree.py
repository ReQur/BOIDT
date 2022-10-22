class Leave:
    freq: int
    data: str

    def __init__(self, _freq, _data):
        self.freq = _freq
        self.data = _data

    def __repr__(self):
        return f"'{self.data}': {self.freq}"

    def __hash__(self):
        return hash((self.data, self.freq))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.freq == other.freq and self.data == other.data


class Node:
    freq: int
    left: None
    right: None

    def __init__(self, _freq, _left, _right):
        self.freq = _freq
        self.left = _left
        self.right = _right

    def __repr__(self):
        return f"{self.freq=} {self.left=} {self.right=}"


def get_haffman_codes(node, code=''):
    if isinstance(node, Leave):
        return {node.data: code}
    l = dict()
    r = dict()
    if node.left:
        l = get_haffman_codes(node.left, code+'1')
    if node.right:
        r = get_haffman_codes(node.right, code+'0')
    return l | r


def build_tree(chars):
    while len(chars) != 1:
        l, r, *chars = chars
        node = Node(l.freq + r.freq, l, r)
        chars.append(node)
        chars.sort(key=lambda x: x.freq)
    return chars
