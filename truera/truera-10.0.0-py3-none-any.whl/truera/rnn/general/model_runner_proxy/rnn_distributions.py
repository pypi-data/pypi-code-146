import numpy as np
from trulens.nn.backend import Backend
from trulens.nn.backend import get_backend
from trulens.nn.distributions import DoI


# NOTE all this does is take the right element out of a list because tf rnn outputs 2 items instead of 1.
# TODO see if this is general enough of a case to be ported into lens-api. or if its too model specific, figuring out a way to generalize this
# NOTE worst case we can put the whole thing into explain_helpers
class RNNLinearDoi(DoI):

    def __init__(self, backend, baseline=None, resolution=10, cut=None):
        """
        __init__ Constructor

        Parameters
        ----------
        baseline : backend.Tensor
            Must be same shape as support, i.e., shape of z points
            eventually passed to __call__
        resolution : int
            Number of points returned by each call to this DoI
        """
        super(RNNLinearDoi, self).__init__(cut)
        self._baseline = baseline
        self._resolution = resolution
        self.backend = backend

    def calc_doi(self, x_input, tf_cell=False):
        x = x_input[0] if tf_cell else x_input
        batch_size = len(x)
        B = get_backend()

        if self._baseline is None:
            if B.is_tensor(x):
                x = B.as_array(x)
            baseline = np.zeros_like(x)
        else:
            baseline = self._baseline

        tile_dims = [1] * len(baseline.shape)
        tile_dims[0] = batch_size
        baseline = baseline[0, ...]
        baseline = np.tile(baseline, tuple(tile_dims))

        if B.is_tensor(x) and not B.is_tensor(baseline):
            baseline = B.as_tensor(baseline)

        if not B.is_tensor(x) and B.is_tensor(baseline):
            baseline = B.as_array(baseline)

        r = self._resolution - 1.
        doi_out = [
            (1. - i / r) * x + i / r * baseline
            for i in range(self._resolution)
        ]
        if tf_cell:
            doi_out = [[d, x_input[1]] for d in doi_out]
        return doi_out

    def __call__(self, x):
        tf_cell = self.backend == Backend.TENSORFLOW and isinstance(x, tuple)
        return self.calc_doi(x, tf_cell=tf_cell)

    def get_activation_multiplier(self, activation):
        B = get_backend()
        batch_size = len(activation)
        if (self._baseline is None):
            baseline = np.zeros_like(activation)
        else:
            baseline = self._baseline

        tile_dims = [1] * len(baseline.shape)
        tile_dims[0] = batch_size
        baseline = baseline[0, ...]
        baseline = np.tile(baseline, tuple(tile_dims))
        if (B.is_tensor(activation) and not B.is_tensor(baseline)):
            baseline = B.as_tensor(baseline)

        if (not B.is_tensor(activation) and B.is_tensor(baseline)):
            baseline = B.as_array(baseline)

        batch_size = len(activation)
        return activation - baseline
