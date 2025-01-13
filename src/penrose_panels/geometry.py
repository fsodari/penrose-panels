"""
Functions for handling common geometry operations.

Points on the plane are represented with complex numbers, and shapes are represented with
numpy arrays of complex points representing the vertices.

"""

import numpy as np
import numpy.typing as npt


def point(p: complex) -> npt.NDArray[np.complex128]:
    """"""
    return np.array([p], dtype=np.complex128)


def polygon(*points: complex) -> npt.NDArray[np.complex128]:
    """
    Construct a polygon (ndarray of complex dtype) from discrete complex points.
    Point order? Validate shape?
    """
    return np.array(points, dtype=np.complex128)


def side_lengths(poly: npt.NDArray[np.complex128]) -> npt.NDArray[np.float64]:
    """
    Compute all side lengths of a polygon and return as an array.
    |b-a|, |c-b|, ... , |a-z|
    """
    return np.abs(np.diff(poly, 1, append=poly[0]))


def isoceles(theta: float) -> npt.NDArray[np.complex128]:
    """
    Create an isoceles triangle with leg length=1.0
    Theta is the angle between the base and the leg.
    The triangle will be created with its base centered at the origin
    """
    # isoceles triangle bisected along axis of symmetry gives two right triangles.
    a = -1.0 * np.cos(theta)
    b = 1.0j * np.sin(theta)
    c = 1.0 * np.cos(theta)
    return polygon(a, b, c)


def rhombus(theta: float) -> npt.NDArray[np.complex128]:
    """Generate a rhombus with side length = 1, and one angle given."""

    # Create an isoceles triangle
    a, b, c = isoceles(theta / 2.0)
    return polygon(a, b, c, np.conj(b))


def midpoint(a: np.complex128, b: np.complex128) -> np.complex128:
    """"""
    return (a + b) / 2.0


def translate(
    points: npt.NDArray[np.complex128], amount: complex
) -> npt.NDArray[np.complex128]:
    """Translate a set of points by a constant amount."""
    return points + amount


def rotate(
    points: npt.NDArray[np.complex128], theta: float, origin: np.complex128 = 0j
) -> npt.NDArray[np.complex128]:
    """Rotate a set of points by theta radians. Optionally provide an origin to rotate around."""
    return origin + np.exp(1j * theta) * (points - origin)


def scale(
    points: npt.NDArray[np.complex128], k: float, origin: np.complex128 = 0j
) -> npt.NDArray[np.complex128]:
    """Zoom/Scale a set of points relative to an origin."""
    return k * (points - origin) + origin


# def reflect(*points: npt.NDArray[np.complex128], line: tuple[np.complex128, ...]):
#     """
#     Reflect point(s) across a line.
#     """


def intersects(
    poly1: npt.NDArray[np.complex128], poly2: npt.NDArray[np.complex128]
) -> bool:
    """
    Check if polygon intersects with another Polygon
    """

    def ccw(a: np.complex128, b: np.complex128, c: np.complex128):
        return (c.imag - a.imag) * (b.real - a.real) > (b.imag - a.imag) * (
            c.real - a.real
        )

    # Check all of poly1's edges.
    for i, p in enumerate(poly1):
        p: np.complex128

        a = poly1[i - 1]
        b = p

        for k, p2 in enumerate(poly2):
            c = poly2[k - 1]
            d = p2

            ix = ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)
            if ix:
                return True

    return False
