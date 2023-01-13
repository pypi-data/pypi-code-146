from __future__ import annotations

from vega_datasets import data

from plotto import mark_plot


def test_scatter_plot(data=data.cars()):
    mark_plot(
        data=data,
        x="Horsepower",
        y="Miles_per_Gallon",
        shape_by="Origin",
        opacity=0.75,
        y_title=["Miles", "per Gallon"],
        # save_fname="pytest.html",
    )
