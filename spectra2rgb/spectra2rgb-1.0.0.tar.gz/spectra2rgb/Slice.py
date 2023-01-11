class Slice:
    def __init__(self, shape, axis):
        self.__before = shape[:axis]
        self.__after = shape[axis + 1:]

    @property
    def rgb_shape(self):
        return self.__before + (3,) + self.__after

    def at(self, index):
        slice_before = (slice(None),) * len(self.__before)
        slice_after = (slice(None),) * len(self.__after)
        return slice_before + (index,) + slice_after
