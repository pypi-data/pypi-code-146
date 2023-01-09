from typing import List
import numpy as np
import ipywidgets as widgets
from IPython.display import display
from pycollimator.models import load_model
from pycollimator.simulations import Simulation, run_simulation


class _Widget:
    """Our representation of ipywidgets to manage shared state, and control results and displays.
    Seems hacky but was the fastest way. Should not be directly instantiated."""

    def __init__(self):
        self._model = None
        self._results = None
        self._widget = None
        # TODO add results plotting widget and store

    @property
    def results(self) -> List[Simulation]:
        """The simulations run by the widget

        :return: List of Simulations run by the widget
        :rtype: List[Simulation]
        """
        return self._results

    def display(self):
        """Display the widget"""
        display(self._widget)


def parameter_sweep_widget():
    """Create a parameter sweep widget.

    :return: A Widget instance that can be displayed and read from with the `results` field.
    :rtype: _Widget
    """
    widget = _Widget()

    param = widgets.Dropdown(description="Parameter")
    start = widgets.FloatText(description="Start")
    stop = widgets.FloatText(description="Stop", value=10)
    step = widgets.FloatText(description="Step", value=0.5)

    def run_parameter_sweep(param, start, stop, step):
        sim_data = list()
        for value in np.arange(start, stop, step):
            sim_data.append(run_simulation(widget._model, {param: value}, wait=False))
        widget._results = sim_data

    parameter_sweep = widgets.interactive(
        run_parameter_sweep,
        {"manual": True, "manual_name": "Run Parameter Sweep"},
        param=param,
        start=start,
        stop=stop,
        step=step,
    )

    def load_model_params(model):
        widget._model = load_model(model)
        param.options = widget._model.parameters.keys()

    model_select = widgets.interactive(
        load_model_params,
        {"manual": True, "manual_name": "Load Model"},
        model=widgets.Text(placeholder="Enter model name", description="Model"),
    )

    widget._widget = widgets.VBox([model_select, parameter_sweep])

    return widget
