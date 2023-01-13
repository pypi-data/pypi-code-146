import numpy as np

__all__ = ["PeriodicVector"]


class PeriodicVector:
    r"""A point i periodic enironment - e.g. in a crystal system.

    A periodic vector has three coordinates in range [0, 1). The periodic vector space only has fractional entries,
    meaning that values greater or equal to 1 or smaller than 0 can be reduced: 1.1 == 0.1 and -0.2 == 0.8
    This class is a wrapper of a numpy. To access the array use :meth:`value`.

    :param vector: list of numerals
    :return: PeriodicVector with fractional coordinates

    Examples
    --------
    >>> PeriodicVector([1.0, 0.1, -0.6])
    PeriodicVector([0.0, 0.1, 0.4])

    """

    def __init__(self, vector):
        vector = getattr(vector, "value", vector)
        if len(vector) != 3:
            raise ValueError("PeriodicVector must have a dimension of 3!")
        self.__value = np.array(vector) % 1.0

    def __add__(self, other):
        other = getattr(other, "value", other)
        new_vec = PeriodicVector(self.value + other)
        return new_vec

    def __sub__(self, other):
        other = getattr(other, "value", other)
        new_vec = PeriodicVector(self.value - other)
        return new_vec

    def __truediv__(self, other: float):
        new_vec = PeriodicVector(self.value / other)
        return new_vec

    def __mul__(self, other):
        other = getattr(other, "value", other)
        new_vec = PeriodicVector(self.value * other)
        return new_vec

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "PeriodicVector({})".format(self.value.tolist())

    def __getitem__(self, item):
        return self.value[item]

    def __len__(self):
        return len(self.value)

    @property
    def value(self):
        """ Get the wrapped numpy array

        :return: numpy array
        """
        return self.__value

    @value.setter
    def value(self, vec):
        raise TypeError("PeriodicVector is immutable")

    @property
    def x(self):
        """ Get the x component of this vector, is identical to vec[0]

        :return: x scalar
        """
        return self[0]

    @property
    def y(self):
        """ Get the y component of this vector, is identical to vec[0]

        :return: y scalar
        """
        return self[1]

    @property
    def z(self):
        """ Get the z component of this vector, is identical to vec[0]

        :return: z scalar
        """
        return self[2]

    def tolist(self):
        """ Unwrap vector and get list representation of numpy array

        :return: list of entries
        """
        return self.value.tolist()

    def diff(self, other):
        """ Get the difference vector between this PeriodicVector and another point.

        :param other: vector like container
        :return: 1xN numpy array where N is the dimension of the vectors

        Examples
        --------
        >>> PeriodicVector([0.2, 0, 0]).diff([0, 0, 0.2])
        array([-0.2,  0. ,  0.2])

        >>> vec1 = PeriodicVector([0.5, 0.5, 0.5])
        >>> vec2 = PeriodicVector([0.6, 0.7, 0.8])
        >>> vec2.diff(vec1)
        array([0.1,  0.2 ,  0.3])
        >>> vec1.diff(vec2)
        array([-0.1,  -0.2 ,  -0.3])
        """
        other = PeriodicVector(other)
        vec = self.value - np.array(other.value)
        return np.array([_min_periodic_distance(c) for c in vec])


def _min_periodic_distance(x):
    """Calculate the minimal periodic distance from the origin for one coordinate

    :param x: coordinate value
    :return: distance of coordinate from origin

    Examples
    --------
    >>>_min_periodic_distance(-0.6)
    0.4
    """
    if abs(x) > 0.5:
        return _min_periodic_distance(x - np.sign(x))
    else:
        return x

