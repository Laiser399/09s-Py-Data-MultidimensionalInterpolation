from lib import phi_1, get_x


def phi_2(arg: float):
    if -1 <= arg <= 1:
        return - (arg - 1) * (arg + 1)
    return 0


def phi_li(l: int, i: int, arg: float):
    arg_li = 2 ** l * arg - i
    if l == 0:
        return phi_1(arg_li)
    return phi_2(arg_li)


def make_a_getter(fun):
    def get_a(l: int, i: int):
        common_part = fun(get_x(l, i))
        if l == 0:
            return common_part
        if l == 1:
            first = 0.5 * fun(get_x(l, i - 1))
            second = 0.5 * fun(get_x(l, i + 1))
            return common_part - first - second
        if i % 4 == 1:
            first = 3 * fun(get_x(l, i - 1))
            second = 6 * fun(get_x(l, i + 1))
            third = - fun(get_x(l, i + 3))
            return common_part - (first + second + third) / 8
        if i % 4 == 3:
            first = 3 * fun(get_x(l, i + 1))
            second = 6 * fun(get_x(l, i - 1))
            third = - fun(get_x(l, i - 3))
            return common_part - (first + second + third) / 8
        raise ValueError(f'Wrong arguments: l={l}, i={i}')

    return get_a
