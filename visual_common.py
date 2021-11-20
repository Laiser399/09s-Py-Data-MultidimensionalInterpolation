import numpy as np
from interpolator import interpolate, InterpolationMode
import matplotlib.pyplot as plt
from lib_multidim import get_x
import pandas as pd
import random


def interpolate_table(functions, dim, mode: InterpolationMode, indices_iterators):
    rows_count, columns_count = len(indices_iterators), len(functions)
    interpolated = np.full((rows_count, columns_count), None)
    for i in range(rows_count):
        indices_iterator = indices_iterators[i]
        for j in range(columns_count):
            fun = functions[j]
            interpolated[i, j] = interpolate(fun, dim, mode, indices_iterator)
    return interpolated


def display_2d_grid(interpolated, row_names, column_names):
    rows_count, columns_count = interpolated.shape

    fig, ax = plt.subplots(rows_count, columns_count,
                           figsize=(6 * columns_count, 6 * rows_count),
                           sharex=True, sharey=True)
    fig.subplots_adjust(wspace=0, hspace=0)

    for i in range(rows_count):
        for j in range(columns_count):
            a_coefficients, _ = interpolated[i, j]
            x = np.array([get_x(l, i) for l, i in a_coefficients.keys()])
            ax[i, j].plot(x[:, 0], x[:, 1], '.')
    for i in range(rows_count):
        ax[i, 0].set_ylabel(row_names[i], fontsize=30)
    for j in range(columns_count):
        ax[-1, j].set_xlabel(column_names[j], fontsize=30)


def display_3d_grid(interpolated):
    rows_count, columns_count = interpolated.shape

    fig = plt.figure(figsize=(6 * columns_count, 6 * rows_count))
    for i in range(rows_count):
        for j in range(columns_count):
            a_coefficients, _ = interpolated[i, j]
            x = np.array([get_x(l, i) for l, i in a_coefficients.keys()])
            ax = fig.add_subplot(rows_count, columns_count, i * columns_count + j + 1, projection='3d')
            ax.scatter3D(x[:, 0], x[:, 1], x[:, 2])
            ax.view_init(elev=35, azim=-50)


def get_points_counts(interpolated, row_names, column_names):
    rows_count, columns_count = interpolated.shape

    points_counts = np.full((rows_count, columns_count), -1, dtype='int')
    for i in range(rows_count):
        for j in range(columns_count):
            a_coefficients, _ = interpolated[i, j]
            points_counts[i, j] = len(a_coefficients)
    return pd.DataFrame(points_counts, row_names, column_names)


def calc_errors(interpolated, functions, dim, row_names, column_names):
    rows_count, columns_count = interpolated.shape
    random.seed(123)

    max_errors = np.full((rows_count, columns_count), None, dtype='float')
    for i in range(rows_count):
        for j in range(columns_count):
            fun = functions[j]
            _, evaluator = interpolated[i, j]
            max_err = 0
            for t in range(100):
                x = tuple(random.random() for k in range(dim))
                max_err = max(abs(fun(x) - evaluator(x)), max_err)
            max_errors[i, j] = max_err
    return pd.DataFrame(max_errors, row_names, column_names)


def display_2d_graphs(interpolated):
    rows_count, columns_count = interpolated.shape

    fig = plt.figure(figsize=(6 * columns_count, 6 * rows_count))
    fig.subplots_adjust(wspace=0, hspace=0)
    for i in range(rows_count):
        for j in range(columns_count):
            a_coefficients, evaluator = interpolated[i, j]
            X, Y, Z = [], [], []
            for li_pair in a_coefficients.keys():
                x = get_x(*li_pair)
                z = evaluator(x)
                X.append(x[0])
                Y.append(x[1])
                Z.append(z)
            X, Y, Z = np.array(X), np.array(Y), np.array(Z)
            ax = fig.add_subplot(rows_count, columns_count, i * columns_count + j + 1, projection='3d')
            ax.scatter3D(X, Y, Z)
            ax.view_init(elev=35, azim=-50)
