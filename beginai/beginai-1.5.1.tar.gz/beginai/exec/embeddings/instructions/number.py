from .utils import sequence_encoder
from math import log

class Slice(object):
    def __init__(self, minv, maxv, num_slices, skip_masking = False):
        self.minv = minv
        self.maxv = maxv
        self.number_slices = num_slices
        self.skip_masking = skip_masking

    def define_bin_bounds(self):
        inner_range = self.maxv - self.minv # calculate the total inner range
        bin_size = inner_range / self.number_slices # calculate the size each bin needs to be
        bin_bounds = [] # init empty list
        bin_start = self.minv # start bound of current bin
        bin_end = None # end bound of the previous bin

        for i in range(self.number_slices):
            bin_end = round(bin_start + bin_size, 4)
            if i == 0: # edge case where a value could be == minv
                bin_start -= 0.1
            if i == self.number_slices-1: # edge case where a value could be == maxv
                bin_end += 0.1
            bin_bounds.append((bin_start, bin_end))
            bin_start = bin_end
        
        return bin_bounds

    def find_my_position_in_numerical_band(self, my_number):
        all_slices = self.define_bin_bounds()
        slices_encoding = sequence_encoder(all_slices)

        # find index of range for my_number
        for i, s in enumerate(all_slices):
            
            # return if it belongs to current slice
            if my_number<=s[1] and my_number>=s[0]:
                return slices_encoding[i]
            
        # if values goes beyond maxv
        return len(slices_encoding) + 1 

    def apply(self, value):
        # force it to be a number
        value = float(value)
        if self.skip_masking:
            return value
        return self.find_my_position_in_numerical_band(value)


class CompareToField(object):
    def __init__(self):
        pass

    def apply(self, value, compare_to_field_value):
        try:
            return int(value) == int(compare_to_field_value)
        except ValueError:
            return False


class CompareToNumber(object):
    def __init__(self, compare_to_number):
        self.compare_to_number = compare_to_number

    def apply(self, value):
        return value == self.compare_to_number


instructions_map = {
    "Slice": Slice,
    "CompareToField": CompareToField,
    "CompareToNumber": CompareToNumber
}
