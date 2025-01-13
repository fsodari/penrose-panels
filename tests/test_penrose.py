from penrose_panels import geometry
from penrose_panels import penrose

from penrose_panels import tiling
from penrose_panels import image

from pathlib import Path

from matplotlib import pyplot as plt
from matplotlib.patches import Polygon

import seaborn as sns
import numpy as np

sns.set_theme()


def test_init_penrose():
    tiles = penrose.penrose_init(1.0)
    print(*tiles, sep="\n")


def test_penrose_ntiles():
    # max_iter = 12
    # ntiles = []
    # for i in range(max_iter):
    #     init_tile = penrose.penrose_init(10.0, theta=penrose.THICK)
    #     tiles = tiling.create_tiling_n(init_tile, penrose.inflate, i)
    #     ntiles.append(len(tiles))
    #     print(f"i: {i}, len: {len(tiles)}")
    # # print(ntiles)
    x = np.array(range(0, 9))
    y = np.array([1, 5, 10, 25, 61, 154, 393, 1013, 2626])

    print(x)
    print(y)
    base = 1.2
    fit = np.polyfit(x, np.log(y) / np.log(base), 1)
    # a = np.exp(fit[1])
    a = np.pow(base, fit[1])
    b = fit[0]

    # yfit = a * np.exp(b * x)
    yfit = a * np.pow(base, b * x)
    print(yfit.astype(np.int64))

    print(f"Fit: {fit}")
    print(f"a: {a}, b:{b}")
    print(f"error: {yfit.astype(np.int64) - y}")
    # # plt.plot(ntiles)
    # plt.plot(y)
    # plt.plot(yfit)
    # plt.show()


def test_tiling():
    n_iter = 6
    init_tile = penrose.penrose_init(1.0, theta=penrose.THICK)
    tiles = tiling.create_tiling_n(init_tile, penrose.inflate, n_iter)

    im = image.make_svg(tiles, stroke_width=1.0)
    with open(Path("tiles.svg"), "w") as fp:
        fp.write(im)

    # Plot polygons
    def to_polycoord(t):
        coord = [[x.real, x.imag] for x in t]
        coord.append(coord[0])
        return coord

    # Make rhombuses look like rhombuses
    plt.gca().set_aspect("equal")

    # Plot all tiles.
    for t in tiles:
        assert np.all(np.isclose(geometry.side_lengths(t), np.array(4 * [1.0])))
        xs, ys = zip(*to_polycoord(t))
        plt.plot(xs, ys)

    plt.show()
