def phi_1(arg: float):
    if -1 <= arg <= 1:
        return 1 - abs(arg)
    return 0


def phi_li(l: int, i: int, arg: float):
    arg_li = 2 ** l * arg - i
    return phi_1(arg_li)


def get_x(l: int, i: int):
    return i / 2 ** l


def make_a_getter(fun):
    def get_a(l: int, i: int):
        if l == 0:
            return fun(get_x(l, i))
        return fun(get_x(l, i)) - 0.5 * fun(get_x(l, i - 1)) - 0.5 * fun(get_x(l, i + 1))

    return get_a


def build_poly(fun, grid_level: int):
    a_coefficients = {}
    get_a = make_a_getter(fun)
    a_coefficients[(0, 0)] = get_a(0, 0)
    a_coefficients[(0, 1)] = get_a(0, 1)

    for l in range(1, grid_level + 1):
        for i in range(1, 2 ** l, 2):
            a_coefficients[(l, i)] = get_a(l, i)
    return a_coefficients


def build_poly_adaptively(fun, err):
    a_coefficients = {}
    get_a = make_a_getter(fun)

    def recur(l: int, i: int):
        a = get_a(l, i)
        a_coefficients[(l, i)] = a
        if abs(a) > err:
            recur(l + 1, 2 * i - 1)
            recur(l + 1, 2 * i + 1)

    a_coefficients[(0, 0)] = get_a(0, 0)
    a_coefficients[(0, 1)] = get_a(0, 1)

    recur(1, 1)
    return a_coefficients


def make_evaluator(a_coefficients):
    def evaluate(arg: float):
        result = 0
        for ((l, i), a) in a_coefficients.items():
            result += a * phi_li(l, i, arg)
        return result

    return evaluate
