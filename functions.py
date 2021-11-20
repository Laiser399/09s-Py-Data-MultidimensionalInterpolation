import math


def fun1(x: tuple):
    return math.sin(4 * x[0]) + math.cos(4 * x[1]) + 0.01 * math.sin(16 * x[0] * x[1])


def fun2(x: tuple):
    return math.sin(4 * x[0]) + math.cos(4 * x[1]) + 0.1 * math.sin(16 * x[0] * x[1])


def fun3(x: tuple):
    return math.sin(4 * x[0]) + math.cos(4 * x[1]) + math.sin(16 * x[0] * x[1])


functions_2d = [fun1, fun2, fun3]
functions_2d_names = ['fun1', 'fun2', 'fun3']


def fun4(x: tuple):
    return math.sin(4 * x[0]) + math.cos(4 * x[1]) + math.sin(4 * x[2])


def fun5(x: tuple):
    return math.sin(4 * x[0]) + math.cos(4 * x[1]) + 0.01 * math.sin(4 * x[2])


def fun6(x: tuple):
    return math.sin(4 * x[0]) + math.cos(16 * x[0] * x[1]) + math.sin(4 * x[2])


def fun7(x: tuple):
    return math.sin(4 * x[0]) + math.cos(64 * x[0] * x[1] * x[2]) + math.sin(4 * x[2])


functions_3d = [fun4, fun5, fun6, fun7]
functions_3d_names = ['fun4', 'fun5', 'fun6', 'fun7']
