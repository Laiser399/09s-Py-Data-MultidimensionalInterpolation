from lib_multidim import make_a_getter, iterate_l, iterate_i


def iterate_l_sparse(grid_level: int, dim: int):
    max_sum = grid_level + dim - 1

    def generator(state: list, last_increment_index: int = 0):
        if sum(state) > max_sum:
            return
        yield tuple(state)
        for i in range(last_increment_index, len(state)):
            state[i] += 1
            for val in generator(state, i):
                yield val
            state[i] -= 1

    return generator([0] * dim)


def build_poly_full(fun, grid_level: int, dim: int):
    a_coefficients = {}
    get_a = make_a_getter(fun, dim)

    for l in iterate_l(grid_level, dim):
        for i in iterate_i(l):
            a_coefficients[(l, i)] = get_a(l, i)
    return a_coefficients


def build_poly_sparse(fun, grid_level: int, dim: int):
    a_coefficients = {}
    get_a = make_a_getter(fun, dim)

    for l in iterate_l_sparse(grid_level, dim):
        for i in iterate_i(l):
            a_coefficients[(l, i)] = get_a(l, i)
    return a_coefficients
