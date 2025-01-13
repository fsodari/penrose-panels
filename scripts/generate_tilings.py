#!/usr/bin/env python

from penrose_panels import tiling
from penrose_panels import penrose
import argparse
from pathlib import Path
import numpy as np


def main():
    """"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, help="Max Number of iterations for the tiling.")
    parser.add_argument("-save", type=Path, help="Save tiling as numpy file.")

    args = parser.parse_args()

    for i in range(1, args.n + 1):
        print(f"Generating N=={i} ...")
        init_tile = penrose.penrose_init(1.0)
        tiles = tiling.create_tiling_n(init_tile, penrose.inflate, i)
        save_file = Path(args.save) / f"tiling{i}.npy"
        np.save(save_file, tiles)


if __name__ == "__main__":
    main()
