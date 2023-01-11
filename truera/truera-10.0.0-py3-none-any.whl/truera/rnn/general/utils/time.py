import numpy as np


class TemporalData(object):

    def __init__(self, ndarray, lengths, forward_padded):
        self.ndarray = ndarray
        self.lengths = lengths
        self.forward_padded = forward_padded

    def get_ndarray(self):
        return self.ndarray

    def get_lengths(self):
        return self.lengths

    def get_forward_padded(self):
        return self.forward_padded

    def defaulted_pad_transform(self):
        '''
        The default transform that visualization methods can expect: backwards transformed data
        Perform a forward transform followed by the backward transform to make sure that unused values are all 0.
        '''
        return self.forward_pad_transform().backward_pad_transform()

    def forward_pad_transform(self):
        '''
        Shifts all temporal data to be right justified. Assumes the temporal index is the second index.
        '''
        if (self.forward_padded):
            return self
        else:
            new_array = np.zeros_like(self.ndarray)
            max_len = len(self.ndarray[0])
            for i in range(len(self.lengths)):
                curr_length = self.lengths[i]
                new_array[i, max_len -
                          curr_length:max_len] = self.ndarray[i, 0:curr_length]
                new_array[i, 0:max_len - curr_length] = 0
            return TemporalData(
                new_array, self.lengths, not self.forward_padded
            )

    def backward_pad_transform(self):
        '''
        Shifts all temporal data to be left justified. Assumes the temporal index is the second index.
        '''
        if (not self.forward_padded):
            return self
        else:
            new_array = np.zeros_like(self.ndarray)
            max_len = len(self.ndarray[0])
            for i in range(len(self.lengths)):
                curr_length = self.lengths[i]
                new_array[i, 0:curr_length] = self.ndarray[i, max_len -
                                                           curr_length:max_len]
                new_array[i, curr_length:] = 0
            return TemporalData(
                new_array, self.lengths, not self.forward_padded
            )

    def mean_over_timestep(self):
        summed = self.ndarray.sum(1)
        tiled_lengths = np.tile(
            self.lengths, tuple(list(summed.shape[1:]) + [1])
        ).T
        return summed / tiled_lengths
