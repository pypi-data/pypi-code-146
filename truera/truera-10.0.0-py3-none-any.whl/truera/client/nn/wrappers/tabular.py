from dataclasses import dataclass

from truera.client.nn import wrappers as base


class Wrappers(base.Wrappers):
    """
    Wrappers for models that take tabular data. Could be handled as timeseries
    with a single time step.

    * CURRENTLY NOT USED *
    """

    class ModelRunWrapper(base.Wrappers.ModelRunWrapper):
        ...

    class ModelLoadWrapper(base.Wrappers.ModelLoadWrapper):
        ...

    class SplitLoadWrapper(base.Wrappers.SplitLoadWrapper):
        ...


@dataclass
class WrapperCollection(base.WrapperCollection):
    pass
    #split_load_wrapper: Wrappers.SplitLoadWrapper
    #model_load_wrapper: Wrappers.ModelLoadWrapper
    #model_run_wrapper: Wrappers.ModelRunWrapper
