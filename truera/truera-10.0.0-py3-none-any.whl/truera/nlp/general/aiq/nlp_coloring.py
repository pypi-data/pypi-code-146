import numpy as np

MAX_INTENSITY = 180  # Global constant ranging from 0 - 256 determining the level of saturation used in coloring.


def rgb_str(r, g, b):
    return "rgb(%d,%d,%d)" % (r, g, b)


def html_cstr(
    s, color='black', background='white', underline=False, font_size=16
):
    # replace < and > with their wide unicode counterparts to avoid HTML script injection effects
    processed_s = s.replace('<', '＜').replace('>', '＞')
    style = f'color:{color};background-color:{background};font-size:{font_size}px;'
    if underline:
        style += f'border-width:0px 0px 6px 0px;border-color:#4287f5;border-style:solid;'
    return f'<text style="{style}">{processed_s}</text>'


def attributions_to_rgb(
    attributions, norm_factor=None, max_intensity=MAX_INTENSITY
):
    """
    generate the list of rgb colors according to the values of attributions, 
    optional argument: 
        norm_factor specifies the normalizing constant for the list attributions
        max_intensity specifies the maximal saturation of the returned color. Ranges from 256 (most saturated) - 0 (least saturated/white)
    """
    rgbs = []
    if (norm_factor is None):
        max_imp = np.max(np.abs(attributions))
    else:
        max_imp = norm_factor
    for imp in attributions:
        if max_imp > 0:
            normed_imp = int(max(min(imp / max_imp, 1), -1) * max_intensity)
        else:
            normed_imp = 0
        intensity = abs(normed_imp)
        if normed_imp > 0:  # green
            rgbs.append(rgb_str(256 - intensity, 256, 256 - intensity))
        else:  # red
            rgbs.append(rgb_str(256, 256 - intensity, 256 - intensity))
    return rgbs


def generate_rgb_str(
    tokens,
    attributions,
    underline_idxs=None,
    norm_factor=None,
    max_intensity=MAX_INTENSITY
):
    """
    generate the html string of tokens, whose background color are decorated according to the values of attributions, 
    optional argument: underline_idx specifies the index of a token that is underlined .
    """
    rgbs = attributions_to_rgb(
        attributions, norm_factor=norm_factor, max_intensity=max_intensity
    )

    html = ''
    for i, token in enumerate(tokens):
        html += html_cstr(
            token,
            'black',
            rgbs[i],
            underline=(i in underline_idxs)
            if underline_idxs is not None else False
        ) + ' '
    line_style = "margin:4px;line-height:1.8;"
    return f"<p style={line_style}>{html}</p>"


def generate_highlight_str(tokens, is_highlighted, color='blue'):
    formatted_tokens = [
        html_cstr(token, font_size=20, color=color)
        if highlight else html_cstr(token)
        for highlight, token in zip(is_highlighted, tokens)
    ]
    return ' '.join(formatted_tokens)
