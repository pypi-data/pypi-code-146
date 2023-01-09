from __future__ import annotations

XYZ = tuple[float, float, float]
XY = tuple[float, float]
RGB = tuple[float, float, float]


def rgb_to_xyz(rgb: XYZ) -> RGB:
    conversion = (
        (0.41239080, 0.35758434, 0.18048079),
        (0.21263901, 0.71516868, 0.07219232),
        (0.01933082, 0.11919478, 0.95053215),
    )
    # manual matrix product, because I didn't want the numpy dependency
    # tuple(sum(i * j for i, j in zip(rgb, row)) for row in conversion)
    return (
        sum(i * j for i, j in zip(rgb, conversion[0])),
        sum(i * j for i, j in zip(rgb, conversion[1])),
        sum(i * j for i, j in zip(rgb, conversion[2])),
    )


def xyz_to_xy(xyz: XYZ) -> XY:
    return (
        round(xyz[0] / sum(xyz), 2),
        round(xyz[1] / sum(xyz), 2),
    )


def rgb_to_xy(rgb: RGB) -> XY:
    return xyz_to_xy(rgb_to_xyz(rgb))
