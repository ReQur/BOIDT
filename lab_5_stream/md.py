from copy import copy


def md(seed=2):
    init_state = []
    _num = seed*365
    for i in range(10):
        init_state.append(_num&1)
        _num >>= 1
    state_1 = copy(init_state)
    state_2 = copy(init_state)
    for i in range(10):
        i_1 = state_1.pop(0)
        i_2 = state_2.pop(0)
        state_1.append(i_2 ^ state_1[-1])
        state_2.append(i_1 ^ state_2[-1] ^ state_2[0] ^ state_2[5])
    while True:
        i_1 = state_1.pop(0)
        i_2 = state_2.pop(0)
        state_1.append(i_2 ^ state_1[-1])
        state_2.append(i_1 ^ state_2[-1] ^ state_2[0] ^ state_2[5])
        yield i_1 ^ i_2
