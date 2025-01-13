"""
Generic tiling interface. In order to eventually support different tiling
patterns.

Generating a tile set requires these operations:

Initialization: start with an initial shape or pattern (multiple shapes).

Inflate: Enlarge the pattern by one "step". Patterns may grow however they need to.
A list of shapes (ndarrays) is passed to the inflate step, and a list of shapes is
expected to be returned.

For example, a simple square tiling may work like this
initial_tile = polygon(-1 -1j, -1 + 1j, 1 + 1j, 1 - 1j)
def square_inflate(square) -> tuple[np.ndarray,...]:
    # Create a new square that extends out from the origin square.
    # Return the list of 5 squares created from one.
        __
     __|__|__
    |__|__|__|
       |__|


For every pass, every shape will be inflated, and duplicate shapes will be removed.
Additional error checking can be done to look for interecting shapes or gaps.

It's not very efficient, but this is how the penrose tiling generation works
and it can work for other tiling schemes.

"""

from typing import Callable
import numpy as np
import numpy.typing as npt

Shape = npt.NDArray[np.complex128]

InflateFunc = Callable[[Shape], list[Shape]]


def remove_duplicates(tiles: list[Shape], tol: float = 1e-6) -> list[Shape]:
    """"""
    #   This seems rather difficult to do.
    #   Checking if each element is equal to every other element is kind of slow O(n**2)
    #   If we sort the list, it should require fewer comparisons since we only have to check
    #   a certain range.
    # Sort elements.
    selements = sorted(tiles, key=lambda e: (np.mean(e).real, np.mean(e).imag))

    # First item is unique.
    unique_elements = [selements[0]]

    # Go through the entire list
    for element in selements:
        # Check if the element is already in the unique elements list.
        found = False
        for unique in unique_elements:
            """"""
            # Sorted by real first. If we move past an element, we can skip early.
            if np.isclose(np.mean(unique), np.mean(element)):
                found = True
                break

        if not found:
            unique_elements.append(element)

    return unique_elements


def find_minmax(poly: Shape) -> tuple[np.complex128, ...]:
    minx = poly[0]
    maxx = minx
    miny = minx
    maxy = miny

    for p in poly:
        p: complex
        if p.real < minx.real:
            minx = p
        if p.real > maxx.real:
            maxx = p
        if p.imag < miny.imag:
            miny = p
        if p.imag > maxy.imag:
            maxy = p

    return minx, maxx, miny, maxy


def find_minmaxv(polygons: list[Shape]) -> tuple[np.complex128, ...]:
    """"""
    minx = polygons[0][0]
    maxx = minx
    miny = minx
    maxy = miny

    for poly in polygons:
        pminx, pmaxx, pminy, pmaxy = find_minmax(poly)

        if pminx.real < minx.real:
            minx = pminx
        if pmaxx.real > maxx.real:
            maxx = pmaxx
        if pminy.imag < miny.imag:
            miny = pminy
        if pmaxy.imag > maxy.imag:
            maxy = pmaxy

    return minx, maxx, miny, maxy


def _tiling_step(tiles: list[Shape], inflate_func: InflateFunc) -> list[Shape]:
    """
    Execute the tiling step.
    Call inflate func, flatten, remove duplicates.
    """
    # Call inflate function and flatten the list.
    return [i for t in tiles for i in inflate_func(t)]


def create_tiling_n(
    tiles: Shape | list[Shape], inflate_func: InflateFunc, n: int
) -> list[Shape]:
    """
    Iterate the tiling procedure n times, then remove duplicates.
    """
    for _ in range(n):
        tiles = _tiling_step(tiles, inflate_func)

    # Mirror the image across the x axis and remove duplicates
    return np.array(remove_duplicates(tiles + [np.conjugate(t) for t in tiles]))
