import numpy as np
from penrose_panels import tiling, image, geometry
from pathlib import Path

from matplotlib import pyplot as plt
import seaborn as sns

sns.set_theme()


def test_readback():
    tiles = np.load(Path("tilings/tiling8.npy"))
    print(len(tiles))

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
