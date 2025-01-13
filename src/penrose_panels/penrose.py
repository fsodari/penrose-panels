import numpy as np

from .geometry import midpoint, rotate, scale

from .tiling import Shape

# psi = 1/phi where phi is the Golden ratio, sqrt(5)+1)/2
PSI: float = (np.sqrt(5.0) - 1.0) / 2.0
# psi**2 = 1 - psi
PSI2: float = 1 - PSI

# THIN = 2.0 * np.pi / 5.0
THICK = 1.0 * np.pi / 5.0
THIN = 2.0 * np.pi / 5.0


class PenroseRhombus(np.ndarray):
    def __new__(
        cls,
        a: np.complex128,
        b: np.complex128,
        c: np.complex128,
        d: np.complex128,
        *,
        theta: float,
    ):
        # Generate a rhombus, use that to initialize the array.
        obj = np.asarray((a, b, c, d), dtype=np.complex128).view(cls)

        # obj = super().__new__(cls, (4,), np.complex128, rhomb, 0, None, None)
        # Save theta as metadata to indentify which type of rhombus it is.
        obj.theta = theta
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.theta = getattr(obj, "theta", None)

    @classmethod
    def create(cls, theta: float):
        """"""
        # Center at 0
        c: complex = np.real(np.exp(1j * theta))
        b: complex = 1.0j * np.imag(np.exp(1j * theta))
        a = -c
        d = -b

        # Return a shape centered at the origin
        return cls(a, b, c, d, theta=theta)


def penrose_init(side_length: float, theta: float = THICK) -> list[Shape]:
    """"""
    rhomb = PenroseRhombus.create(theta=theta)
    return [scale(rhomb, side_length)]


def _inflate_thick(rhomb: PenroseRhombus) -> list[PenroseRhombus]:
    """"""
    # D and E divide sides AC and AB respectively
    a, b, c, *_ = rhomb

    # Preserve side lengths
    scale_factor = 1.0 / PSI

    d = PSI2 * a + PSI * c
    e = PSI2 * a + PSI * b
    # Take care to order the vertices here so as to get the right
    # orientation for the resulting triangles.
    return [
        scale(
            PenroseRhombus(
                d, e, a, rotate(e, np.pi, origin=midpoint(d, a)), theta=THICK
            ),
            scale_factor,
        ),
        scale(
            PenroseRhombus(
                e, d, b, rotate(d, np.pi, origin=midpoint(e, b)), theta=THIN
            ),
            scale_factor,
        ),
        scale(
            PenroseRhombus(
                c, d, b, rotate(d, np.pi, origin=midpoint(c, b)), theta=THICK
            ),
            scale_factor,
        ),
    ]


def _inflate_thin(rhomb: PenroseRhombus) -> list[PenroseRhombus]:
    """"""
    a, b, c, *_ = rhomb
    d = PSI * a + PSI2 * b

    # Preserve side lengths
    scale_factor = 1.0 / PSI

    return [
        scale(
            PenroseRhombus(
                d, c, a, rotate(c, np.pi, origin=midpoint(d, a)), theta=THIN
            ),
            scale_factor,
        ),
        scale(
            PenroseRhombus(
                c, d, b, rotate(d, np.pi, origin=midpoint(c, b)), theta=THICK
            ),
            scale_factor,
        ),
    ]


def inflate(rhomb: PenroseRhombus) -> list[PenroseRhombus]:
    return (
        _inflate_thin(rhomb) if np.isclose(rhomb.theta, THIN) else _inflate_thick(rhomb)
    )


def iterations_for_n_tiles(n_tiles: int) -> int:
    """
    Returns the number of inflation operations required to generate at least n_tiles.
    Tested up to 12 iterations.
    8 iterations and above takes a looooooong time.
    """
    iter_sizes = {
        0: 1,
        1: 5,
        2: 10,
        3: 25,
        4: 61,
        5: 154,
        6: 393,
        7: 1013,
        8: 2626,
    }
    for k, v in iter_sizes.items():
        if v > n_tiles:
            return k
