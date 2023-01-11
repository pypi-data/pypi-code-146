from trulens.nn.backend import get_backend
from trulens.nn.quantities import MaxClassQoI
from trulens.nn.quantities import QoI


class MultiQoI(QoI):
    """Get an attribution per every idx from a list of neuron_idxs of the tensor.
    """

    def __init__(self, neuron_idxs):
        self.neuron_idxs = neuron_idxs

    def __call__(self, x):
        qois = [x[:, i] for i in self.neuron_idxs]
        return qois


class PerTimestepQoI(QoI):
    '''
    Creates a list of QoI's per timestep which Trulens will return attributions per each of the timesteps
    '''

    def __init__(self, attr_config):
        self.attr_config = attr_config

    def __call__(self, x):
        if isinstance(x, tuple):
            x = x[0]  # torch RNN layer outputs tuple of (vals, hidden_states)
        if len(x.shape) == 3:
            if self.attr_config.n_time_step_output != x.shape[
                1] or self.attr_config.n_output_neurons != x.shape[2]:
                raise Exception(
                    f"QoI did not get expected shape. Shape should be doi_batch x timestep_out x class_out. Supplied Config shows n_time_step_output: {self.attr_config.n_time_step_output}, n_output_neurons: {self.attr_config.n_output_neurons}. The QoI Layer {self.attr_config.output_layer},anchor:{self.attr_config.output_anchor} has n_time_step_output: {x.shape[1]}, n_output_neurons: {x.shape[2]}. Check that the output layer and anchor are correct."
                )
            # Shape should be doi_batch x timestep x class
            # TODO: use attr_config.output_dimension_order to get the right QoI ordering
            num_classes = x.shape[-1]
            num_timesteps = x.shape[1]
            out = []
            for i in range(num_timesteps):
                for j in range(num_classes):
                    out.append(x[:, i, j])
            return out
        if len(x.shape) == 2:
            # Assuming single class or timestep output
            if self.attr_config.n_time_step_output != 1 and self.attr_config.n_output_neurons != 1:
                raise Exception(
                    f"QoI did not get expected shape. Shape should be doi_batch x timestep_out x class_out. Supplied Config shows n_time_step_output: {self.attr_config.n_time_step_output}, n_output_neurons: {self.attr_config.n_output_neurons}. The QoI Layer {self.attr_config.output_layer},anchor:{self.attr_config.output_anchor} has only 2 dimensions. This should only happen if n_output_neurons or n_time_step_output is 1. Check that the output layer and anchor are correct."
                )
            if self.attr_config.n_output_neurons == 1:
                # Assuming single class
                if self.attr_config.n_time_step_output != x.shape[1]:
                    raise Exception(
                        f"QoI did not get expected shape. Supplied Config shows n_time_step_output: {self.attr_config.n_time_step_output}, n_output_neurons: {self.attr_config.n_output_neurons}. So the expected shape should be doi_batch x timestep_out. The QoI Layer {self.attr_config.output_layer},anchor:{self.attr_config.output_anchor} has n_time_step_output: {x.shape[1]}. Check that the output layer and anchor are correct."
                    )
                # Shape should be doi_batch x timestep
                num_timesteps = x.shape[1]
                out = []
                for i in range(num_timesteps):
                    out.append(x[:, i])
                return out
            if self.attr_config.n_time_step_output == 1:
                # Assuming single class
                if self.attr_config.n_output_neurons != x.shape[1]:
                    raise Exception(
                        f"QoI did not get expected shape. Supplied Config shows n_time_step_output: {self.attr_config.n_time_step_output}, n_output_neurons: {self.attr_config.n_output_neurons}. So the expected shape should be doi_batch x classes_out. The QoI Layer {self.attr_config.output_layer},anchor:{self.attr_config.output_anchor} has class_out: {x.shape[1]}. Check that the output layer and anchor are correct."
                    )
                # Shape should be doi_batch x timestep
                num_classes = x.shape[1]
                out = []
                for i in range(num_classes):
                    out.append(x[:, i])
                return out
        if len(x.shape) == 1:
            # Assuming single class and timestep output
            if self.attr_config.n_time_step_output != 1 or self.attr_config.n_output_neurons != 1:
                raise Exception(
                    f"QoI did not get expected shape. Supplied Config shows n_time_step_output: {self.attr_config.n_time_step_output}, n_output_neurons: {self.attr_config.n_output_neurons}. The QoI Layer {self.attr_config.output_layer},anchor:{self.attr_config.output_anchor} has only 1 dimension. This should only happen if both n_output_neurons and n_time_step_output are 1. Check that the output layer and anchor are correct."
                )
            out = [x]


class IndexClassQoI(QoI):

    def __init__(self, index, timestep=None, index_dim=None):
        self.index = index
        self.timestep = timestep
        self.index_dim = index_dim

    def __call__(self, x):
        if isinstance(x, tuple):
            x = x[0]  # torch RNN layer outputs tuple of (vals, hidden_states)
        if self.index_dim == 1:
            return x[:, self.
                     index, :] if self.timestep is None else x[:, self.index,
                                                               self.timestep]
        elif self.index_dim == -1:

            return x[:, :,
                     self.index] if self.timestep is None else x[:,
                                                                 self.timestep,
                                                                 self.index]
        elif self.index_dim is None and self.timestep is None and len(
            x.shape
        ) == 2:
            return x[:, self.index]


class SequentialMaxClassQoI(MaxClassQoI):

    def __call__(self, x):
        if isinstance(x, tuple):
            x = x[0]  # torch RNN layer outputs tuple of (vals, hidden_states)
        x = x[:, -1]
        return super(SequentialMaxClassQoI, self).__call__(x)


class InternalAveragePerTimestepQoI(QoI):

    def __init__(self, indx):
        self._indx = indx

    def __call__(self, x):
        B = get_backend()
        if isinstance(x, tuple):
            x = x[0]  # torch RNN layer outputs tuple of (vals, hidden_states)
        qoi_calc = [B.sum(x[:, i, self._indx]) for i in range(x.shape[1])]
        return qoi_calc
