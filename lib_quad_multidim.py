from lib_quad import phi_li as phi_li_d1
from lib_multidim import get_x
from functools import lru_cache


def phi_li(l: tuple, i: tuple, arg: tuple):
    result = 1
    for l_, i_, arg_ in zip(l, i, arg):
        result *= phi_li_d1(l_, i_, arg_)
    return result


def make_a_getter(fun, dim: int):
    @lru_cache(maxsize=None)
    def recursion(l: tuple, i: tuple, k=0):
        if k == dim:
            return fun(get_x(l, i))
        common_part = recursion(l, i, k + 1)
        if l[k] == 0:
            return common_part
        if l[k] == 1:
            first_i = i[:k] + (i[k] - 1,) + i[k + 1:]
            second_i = i[:k] + (i[k] + 1,) + i[k + 1:]
            first = recursion(l, first_i, k + 1)
            second = recursion(l, second_i, k + 1)
            return common_part - (first + second) / 2
        if i[k] % 4 == 1:
            first_i = i[:k] + (i[k] - 1,) + i[k + 1:]
            second_i = i[:k] + (i[k] + 1,) + i[k + 1:]
            third_i = i[:k] + (i[k] + 3,) + i[k + 1:]
            first = 3 * recursion(l, first_i, k + 1)
            second = 6 * recursion(l, second_i, k + 1)
            third = - recursion(l, third_i, k + 1)
            return common_part - (first + second + third) / 8
        if i[k] % 4 == 3:
            first_i = i[:k] + (i[k] + 1,) + i[k + 1:]
            second_i = i[:k] + (i[k] - 1,) + i[k + 1:]
            third_i = i[:k] + (i[k] - 3,) + i[k + 1:]
            first = 3 * recursion(l, first_i, k + 1)
            second = 6 * recursion(l, second_i, k + 1)
            third = - recursion(l, third_i, k + 1)
            return common_part - (first + second + third) / 8
        raise ValueError(f'Wrong arguments: l={l}, i={i}')

    def get_a(l: tuple, i: tuple):
        return recursion(l, i)

    return get_a
