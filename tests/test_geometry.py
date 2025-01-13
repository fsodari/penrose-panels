import numpy as np

from penrose_panels import geometry


def test_isoceles():
    # Equilateral triangle.
    theta = np.pi / 3
    iso = geometry.isoceles(theta)
    a, b, c = iso

    # Check that side lengths are equal to 1.
    assert np.isclose(np.abs(b - a), 1.0)
    assert np.isclose(np.abs(b - c), 1.0)

    # Check using the side lengths function.
    assert np.all(np.isclose(geometry.side_lengths(iso), 3 * [1.0]))

    # Check that base is centered at zero.
    assert np.isclose((c + a) / 2.0, 0.0)


def test_rhombus():
    theta = np.pi / 8
    rhomb = geometry.rhombus(theta)
    a, b, c, d = rhomb

    # Check all side lengths are equal to 1.
    assert np.isclose(np.abs(b - a), 1.0)
    assert np.isclose(np.abs(c - b), 1.0)
    assert np.isclose(np.abs(d - c), 1.0)
    assert np.isclose(np.abs(a - d), 1.0)

    # Check using side lengths function
    assert np.all(np.isclose(geometry.side_lengths(rhomb), 4 * [1.0]))

    # Check that it's centered at zero
    assert np.isclose(np.mean((a, b, c, d)), 0.0)


def test_translate():
    rhomb = geometry.rhombus(np.pi / 7)

    dist = 0.25 + -1.4j

    # Translate the rhombus
    translated = geometry.translate(rhomb, dist)

    # The rhombus origin was originally at 0, so it should now be at dist.
    assert np.isclose(np.mean(translated), dist)


def test_scale():
    rhomb = geometry.rhombus(np.pi / 6.234)
    assert np.all(np.isclose(geometry.side_lengths(rhomb), 4 * [1.0]))

    scaled = geometry.scale(rhomb, 1.2)

    assert np.all(np.isclose(geometry.side_lengths(scaled), 4 * [1.2]))
