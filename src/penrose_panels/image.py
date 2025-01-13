"""
Convert ndarrays to svgs
"""

import numpy as np
from pathlib import Path
from .tiling import Shape, find_minmaxv
from .geometry import translate


def svg_path(poly: Shape):
    """
    Return the SVG "d" path element specifier for a polygon. Make sure the points are in the right order.
    """

    svg_str = ""
    p_prev = 0j
    for i, p in enumerate(poly):
        p: complex
        if i == 0:
            svg_str += f"m{p.real}, {p.imag}"
        else:
            diff = p - p_prev
            svg_str += f" l{diff.real}, {diff.imag}"
        p_prev = p

    svg_str += "z"
    return svg_str


def make_svg(tiling: list[Shape], stroke_width: float = 0.01, stroke_color=(0, 0, 0)):
    """Make and return the SVG for the tiling as a str."""

    minx, maxx, miny, maxy = find_minmaxv(tiling)
    stroke_colorfmt = (
        f"#{stroke_color[0]:02x}{stroke_color[1]:02x}{stroke_color[2]:02x}"
    )

    viewbox = f"{minx.real} {miny.imag} {(maxx - minx).real} {(maxy - miny).imag}"

    svg = [
        '<?xml version="1.0" encoding="utf-8"?>',
        f'<svg width="100%" height="100%" viewBox="{viewbox}"'
        ' preserveAspectRatio="xMidYMid meet" version="1.1"'
        ' baseProfile="full" xmlns="http://www.w3.org/2000/svg">',
    ]

    # The tiles' stroke widths scale with ngen
    svg.append(
        '<g style="stroke:{}; stroke-width: {}; stroke-linejoin: round;">'.format(
            stroke_colorfmt, stroke_width
        )
    )

    for t in tiling:
        svg.append(
            '<path fill="#ffffff" fill-opacity="0.0" d="{}"/>'.format(
                svg_path(t),
            )
        )

    svg.append("</g>\n</svg>")

    return "\n".join(svg)
