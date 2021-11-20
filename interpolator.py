from enum import Enum
from lib_multidim import make_a_getter as make_a_getter_linear
from lib_quad_multidim import make_a_getter as make_a_getter_quad
from lib_multidim import iterate_l, iterate_i
from lib_multidim import phi_li as phi_li_linear
from lib_quad_multidim import phi_li as phi_li_quad


class InterpolationMode(Enum):
    Linear = 0,
    Quad = 1


def interpolate(fun, dim: int, mode: InterpolationMode, k_indices_iterator):
    get_a = make_a_getter(fun, dim, mode)
    phi_li = get_phi_li(mode)
    a_coefficients = build_a_coefficients(dim, k_indices_iterator, get_a)
    evaluator = make_evaluator(a_coefficients, phi_li)

    return a_coefficients, evaluator


def get_full_indices_iterator(grid_level: int):
    def iterator(_: float, l: tuple):
        for k in range(len(l)):
            if l[k] < grid_level:
                yield k

    return iterator


def get_sparse_indices_iterator(grid_level: int, dim: int):
    max_sum = grid_level + dim - 1

    def iterator(_: float, l: tuple):
        if sum(l) >= max_sum:
            return
        for k in range(len(l)):
            yield k

    return iterator


def get_adaptive_indices_iterator(err: float):
    def iterator(a: float, l: tuple):
        if abs(a) <= err:
            return
        for k in range(len(l)):
            yield k

    return iterator


def make_a_getter(fun, dim: int, mode: InterpolationMode):
    if mode == InterpolationMode.Linear:
        return make_a_getter_linear(fun, dim)
    if mode == InterpolationMode.Quad:
        return make_a_getter_quad(fun, dim)
    raise ValueError()


def get_phi_li(mode: InterpolationMode):
    if mode == InterpolationMode.Linear:
        return phi_li_linear
    if mode == InterpolationMode.Quad:
        return phi_li_quad
    raise ValueError()


def build_a_coefficients(dim: int, k_indices_iterator, get_a):
    a_coefficients = {}

    def recursion(l: tuple, i: tuple):
        a = get_a(l, i)
        a_coefficients[(l, i)] = a
        for k in k_indices_iterator(a, l):
            if l[k] == 0:
                continue
            next_l = l[:k] + (l[k] + 1,) + l[k + 1:]
            left_i = i[:k] + (2 * i[k] - 1,) + i[k + 1:]
            right_i = i[:k] + (2 * i[k] + 1,) + i[k + 1:]
            recursion(next_l, left_i)
            recursion(next_l, right_i)

    for l in iterate_l(1, dim):
        for i in iterate_i(l):
            recursion(l, i)

    return a_coefficients


def make_evaluator(a_coefficients, phi_li):
    def evaluate(arg: tuple):
        result = 0
        for ((l, i), a) in a_coefficients.items():
            result += a * phi_li(l, i, arg)
        return result

    return evaluate
