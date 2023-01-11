"""
Create colour palettes relating to Urban Intelligence's main products
"""

__all__ = ["generate_colour_palette"]

import colour

def generate_colour_palette(palette="risk", scheme="divergent", n=5) -> list:
    """
    Return a list of hex strings that relate to an Urban Intelligence colour palette (planning, access or risk) for a given colour scheme (monochromatic or divergent). Colours are always returned in the order of positive to worst (in respect of what the palette is defining as a good and poor colour).
    """

    colour_palettes = {
    "planning": {
        "monochromatic": ["#5aa33b", "#48942e", "#358520", "#207611", "#006700"],
        "divergent": ["#5aa33b", "#76b05a", "#8fbd77", "#a8ca95", "#c0d7b3", "#d9e4d2", "#f1f1f1", "#f1d4d4", "#f0b8b8", "#ec9c9d", "#e67f83", "#de6069", "#d43d51"], 
        },
    "access": {
        "monochromatic": ["#246783", "#21779a", "#1b86b2", "#1396cb", "#09a7e5", "#00b7ff"],
        "divergent": ["#246783", "#307d91", "#44929d", "#5ca8a8", "#78beb1", "#97d3bb", "#93daa7", "#9fdd8c", "#b7de6a", "#d8dc44", "#ffd416"], 
        },
    "risk": {
        "monochromatic": ["#0b2948", "#344a69", "#596d8d", "#7f93b1", "#a7bad8", "#d1e3ff"],
        "divergent": ["#0b2948", "#3b4b67", "#657187", "#9198a8", "#bfc2ca", "#eeeeee", "#fad3c1", "#ffb896", "#ff9d6b", "#fe813f", "#f86302"], 
        }
    }

    if palette not in colour_palettes.keys():
        raise ValueError(f"The given pallete: {palette} is not acceptable. Please choose from: {list(colour_palettes.keys())}")
    if scheme not in colour_palettes[palette].keys():
        raise ValueError(f"The given scheme: {scheme} is not acceptable. Please choose from: {list(colour_palettes[palette].keys())}")
    
    default_colours = colour_palettes[palette][scheme]
    if len(default_colours) == 0:
        raise NotImplementedError(f"Unfortunately, there is no colour scheme for the {palette} palette using a {scheme} scheme. Apologies for the inconvenience.")
    elif len(default_colours) == n:
        return default_colours
    else:
        return [color.get_hex() for color in colour.Color(default_colours[0]).range_to(colour.Color(default_colours[-1]), steps=n)]
