from functools import lru_cache
from lib import get_x as get_x_d1, phi_li as phi_li_d1


def phi_li(l: tuple, i: tuple, arg: tuple):
    result = 1
    for l_, i_, arg_ in zip(l, i, arg):
        result *= phi_li_d1(l_, i_, arg_)
    return result


@lru_cache(maxsize=None)
def get_x(l: tuple, i: tuple):
    return tuple(get_x_d1(*pair) for pair in zip(l, i))


def make_a_getter(fun, dim: int):
    @lru_cache(maxsize=None)
    def recursion(l: tuple, i: tuple, k=0):
        if k == dim:
            return fun(get_x(l, i))
        common_part = recursion(l, i, k + 1)
        if l[k] == 0:
            return common_part
        left_i = i[:k] + (i[k] - 1,) + i[k + 1:]
        right_i = i[:k] + (i[k] + 1,) + i[k + 1:]
        return common_part - 0.5 * recursion(l, left_i, k + 1) - 0.5 * recursion(l, right_i, k + 1)

    def get_a(l: tuple, i: tuple):
        return recursion(l, i)

    return get_a


def iterate_l(grid_level: int, dim: int):
    def generator(state: list, last_increment_index: int = 0):
        yield tuple(state)
        for i in range(last_increment_index, len(state)):
            if state[i] >= grid_level:
                continue
            state[i] += 1
            for val in generator(state, i):
                yield val
            state[i] -= 1

    return generator([0] * dim)


def iterate_i(l: tuple):
    def iterate_i_k(l_k: int):
        if l_k == 0:
            yield 0
            yield 1
        else:
            for p in range(1, 2 ** (l_k - 1) + 1):
                yield 2 * p - 1

    def recursion(state: list, k: int = 0):
        if k >= len(state):
            yield tuple(state)
            return
        for i_k in iterate_i_k(l[k]):
            state[k] = i_k
            for val in recursion(state, k + 1):
                yield val

    state = [None] * len(l)
    return recursion(state)









