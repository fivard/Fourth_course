import numpy as np
from matplotlib import pyplot as plt
from matplotlib import collections as mc
import json

SIZE = 10
points_x = []
points_y = []

points = []

# start points
with open("module2.json", "r") as f:
    points = json.loads(f.read())["curve"]
    for point in points:
        points_x.append(point[0])
        points_y.append(point[1])

lines = np.empty(0)
for i in range(SIZE - 1):
    lines = np.append(lines, [points_x[i], points_y[i], points_x[i + 1], points_y[i + 1]])
lines = np.reshape(lines, (lines.shape[0] // 4, 2, 2))

fig = plt.figure(1)
ax = plt.axes(xlim=(100, 1000), ylim=(100, 1000))
lc = mc.LineCollection(lines, colors='green', linewidths=1.2)
ax.add_collection(lc)


def getBezierBasis(i, n, t):
    def fact(n):
        return 1 if n <= 1 else n * fact(n - 1)

    return (fact(n) / (fact(i) * fact(n - i))) * pow(t, i) * pow(1 - t, n - i)


def getBezierCurve(arr, step=0.01):
    res = []
    t = 0.0

    while t <= 1.0:
        if t > 1:
            t = 1

        ind = len(res)

        res.append([0, 0])

        for i in range(SIZE):
            b = getBezierBasis(i, SIZE - 1, t)

            res[ind][0] += arr[i][0] * b
            res[ind][1] += arr[i][1] * b

        t += step

    return res


# get bezier points:
bezier_points_x = np.empty(0)
bezier_points_y = np.empty(0)
points_on_plot, = ax.plot(points_x, points_y, 'ro')

res = getBezierCurve(points)

for point in res:
    bezier_points_x = np.append(bezier_points_x, point[0])
    bezier_points_y = np.append(bezier_points_y, point[1])

bezier_p, = ax.plot(bezier_points_x, bezier_points_y, color='darkorchid', linewidth=3)

plt.show()
