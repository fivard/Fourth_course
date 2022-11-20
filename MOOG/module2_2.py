import numpy as np
from tqdm import tqdm
from functools import lru_cache
from matplotlib.tri.triangulation import Triangulation
import matplotlib.pyplot as plt
import json

DEGREE = 3


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        return Point(self.x * other, self.y * other, self.z * other)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)


def load_data_surface(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    points = [Point(p[0], p[1], p[2]) for p in data.get('surface', {}).get('points', [])]
    dim = data.get('surface', {}).get('gridSize', [13, 13])
    indices = data.get('surface', {}).get('indices')
    return points, dim, indices


@lru_cache
def calc_N(i, k, U, u):
    if k == 1:
        if U[i] <= u < U[i + 1]:
            return 1
        return 0
    c1 = (u - U[i]) / (U[i + k - 1] - U[i])
    c2 = (U[i + k] - u) / (U[i + k] - U[i + 1])
    return c1 * calc_N(i, k - 1, U, u) + c2 * calc_N(i + 1, k - 1, U, u)


@lru_cache
def calc_all_n(k, U, u, n):
    return [calc_N(i, k, U, u) for i in range(n)]


def calc_r(index, dim, U, u, v):
    all_ns_u = calc_all_n(DEGREE, U, u, dim[0])
    all_ns_v = calc_all_n(DEGREE, U, v, dim[1])
    numerator = all_ns_u[index[0]] * all_ns_v[index[1]] * 1
    if not numerator:
        return numerator
    denumerator = 0
    for p in range(dim[0]):
        for q in range(dim[1]):
            denumerator += all_ns_u[p] * all_ns_v[q] * 1
    return numerator / denumerator


def calc_nurbs(points, dim, indices) -> list[Point]:
    U = tuple(range(dim[0] + DEGREE + 1))
    controls = np.arange(max(U), step=0.1)

    res = []
    for u in tqdm(controls):
        for v in controls:
            res_p = Point(0, 0, 0)
            for k in range(dim[0]):
                for l in range(dim[1]):
                    a = points[indices.index([k, l])]
                    b = calc_r([k, l], dim, U, u, v)
                    res_p += points[indices.index([k, l])] * calc_r([k, l], dim, U, u, v)
            res.append(res_p)
    return res


def vizualize(points: list[Point]):
    X = [p.x for p in points if [p.x, p.y, p.z] != [0, 0, 0]]
    Y = [p.y for p in points if [p.x, p.y, p.z] != [0, 0, 0]]
    Z = [p.z for p in points if [p.x, p.y, p.z] != [0, 0, 0]]

    _, ax = plt.subplots(subplot_kw={"projection": "3d"})
    triangulation = Triangulation(X, Y)
    ax.plot_trisurf(triangulation, Z)
    plt.show()


if __name__ == "__main__":
    points, dim, indices = load_data_surface('module2.json')
    data = calc_nurbs(points, dim, indices)
    vizualize(data)
