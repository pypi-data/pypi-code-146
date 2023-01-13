from __future__ import annotations

import altair as alt
import numpy as np
import pandas as pd
from pandas import DataFrame


def random_colors(n):
    colors = ["#DA722E", "#0B5345", "#DDCC77", "#88CCEE", "#2275A9", "#CC6677"]

    if n <= len(colors):
        return colors

    add_n = n - len(colors)

    for _i in range(add_n):
        c = "".join(np.random.choice(list("ABCDEF0123456789"), size=6))
        colors.append(f"#{c}")
    return colors


def add_straight_line(
    xy: str, at: float, enc: str = None, configure_vh_line: dict = None
):
    if configure_vh_line is None:
        configure_vh_line = {}

    xy_enc = f"{xy}:{enc}" if enc is not None else xy

    line = (
        alt.Chart(pd.DataFrame({xy: [at]}))
        .mark_rule(**configure_vh_line)
        .encode(**{xy: xy_enc})
    )

    return line


def coefficient_plot(
    data: DataFrame,
    y: str,
    x: str,
    lower_upper: list,
):
    data[y] = data[y].astype(str)

    data_long = (
        data.set_index(y)[lower_upper]
        .unstack()
        .reset_index()
        .pipe(lambda x: x.set_axis(["idx", y, "interval"], axis=1))
    )

    # data_long =
    line = (
        alt.Chart(data=data_long)
        .mark_rule()
        .encode(y=y, x="interval", detail=y)  # 'group:N'
    )

    points = alt.Chart(data=data).mark_point().encode(x=x, y=y)  # 'group:N',

    chart = (
        alt.layer(line, points)
        .resolve_scale(
            color="independent", shape="independent", strokeDash="independent"
        )
        .interactive()
    )

    return chart


def chart_html(
    altair_chart,
    figure_caption: str = None,
    caption_font: str = "helvetica",
    save_fname: str = None,
):
    """takes an altair chart and returns a manually modified html with a figure caption"""

    if not isinstance(caption_font, str):
        caption_font = "helvetica"

    if figure_caption is None and save_fname is not None:
        altair_chart.save(
            save_fname,
            # embed_options={'renderer': 'svg'}
        )
    else:
        chart_html = altair_chart.to_html()
        chart_html = chart_html.replace(
            r"<style>",
            f"<style>"
            f"figure "
            f"{{display: table;"
            f"font-family:{caption_font};}} "
            f"figcaption "
            f"{{display:table-caption;"
            f"caption-side:bottom;"
            f"text-align:justify;"
            f"margin:0em;"
            f"padding:0em;"
            f"font-size:smaller;"
            f'font-family:{caption_font};}}"',
        )

        chart_html = chart_html.replace(r"<body>", "<body>" '<figure id="fig_id">')

        # be careful there are multiple '</script>'
        chart_html = chart_html.replace(
            r" </script>",
            f"</script>"
            f"\n<figcaption>"
            f"{figure_caption}"
            f"\n</figcaption>"
            f"\n</figure>",
        )

        if save_fname:
            # overwrite html
            with open(save_fname, "w+") as f:
                f.write(chart_html)
        else:
            return chart_html


def plot_table_note(
    data: DataFrame | dict,
    col_names: list | None = None,
    configure_table_note: dict = None,
    properties_table_note: dict = None,
):
    if isinstance(data, dict):
        data = pd.DataFrame.from_dict(data, orient="index").reset_index()
        data.columns = ["name", "info"]
        col_names = ["name", "info"]

    if configure_table_note is None:
        configure_table_note = {}
    if properties_table_note is None:
        properties_table_note = {}

    ranked_text = (
        alt.Chart(data)
        .mark_text(**configure_table_note)
        .encode(y=alt.Y("row_number:O", axis=None))
        .transform_window(row_number="row_number()")
    )

    ranked_text_bold = (
        alt.Chart(data)
        .mark_text(fontWeight="bold", **configure_table_note)
        .encode(y=alt.Y("row_number:O", axis=None))
        .transform_window(row_number="row_number()")
    )

    # Data Tables'
    col_1 = ranked_text_bold.encode(text=f"{col_names[0]}").properties(
        **properties_table_note
    )
    col_2 = ranked_text.encode(text=f"{col_names[1]}").properties(
        **properties_table_note
    )

    text = alt.hconcat(col_1, col_2)  # Combine data tables

    return text
