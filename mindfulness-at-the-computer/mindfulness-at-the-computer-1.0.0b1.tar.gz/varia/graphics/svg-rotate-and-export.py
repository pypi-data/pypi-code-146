import logging

# Dependencies:
import svgutils  # https://svgutils.readthedocs.io/en/latest/
import cairosvg

"""
online search: inkscape save only shape not page

rotate svg
https://stackoverflow.com/questions/43199869/rotate-and-scale-a-complete-svg-document-using-python
"""

FILE_NAME = "moving-icon-gradient.svg"
orig_svg_figure = svgutils.transform.fromfile(FILE_NAME)
assert orig_svg_figure.width == orig_svg_figure.height
print(f"{orig_svg_figure.width=} (height is same)")

index = 0
numeric = "0123456789."
for char in orig_svg_figure.width:
    if char not in numeric:
        break
    index += 1
width_and_height: float = float(orig_svg_figure.width[:index])

orig_svg = svgutils.compose.SVG(FILE_NAME)
orig_svg.rotate(60, width_and_height/2, width_and_height/2)
# https://svgutils.readthedocs.io/en/latest/transform.html#svgutils.transform.FigureElement.rotate
new_svg_figure = svgutils.compose.Figure(orig_svg_figure.height, orig_svg_figure.width, orig_svg)
new_svg_figure.save("test-rotate-60.svg")

cairosvg.svg2png(
    bytestring=open("test-rotate-60.svg").read().encode('utf-8'),
    write_to="test-rotate-60.png"
)
