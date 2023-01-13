import numpy


def ToList(args, dtype: type = None):
    if dtype is not None:
        output = numpy.atleast_1d(args).astype(dtype)
    else:
        output = numpy.atleast_1d(args)

    none_idx = numpy.where(output==None)

    if len(none_idx[0]) != 0:
        output[none_idx] = numpy.nan

    return output


class UnitArray(numpy.ndarray):
    unit = None
    prefixes = {'femto': {'sign': 'f', 'exp': -12},
                'nano': {'sign': 'n', 'exp': -9},
                'micro': {'sign': '\u03BC', 'exp': -6},
                'milli': {'sign': 'm', 'exp': -3},
                'none': {'sign': '', 'exp': +0},
                'kilo': {'sign': 'k', 'exp': +3},
                'mega': {'sign': 'M', 'exp': +6},
                'giga': {'sign': 'G', 'exp': +9},
                'peta': {'sign': 'P', 'exp': +12}}

    def __new__(cls, input_array, unit: str, info=None):
        obj = numpy.asarray(input_array).view(cls)
        obj = numpy.atleast_1d(obj)
        obj[numpy.where(obj==None)] = numpy.nan
        obj.info = info
        obj.unit = unit

        return obj

    def __array_finalize__(self, obj):
        if obj is None: 
            return 1

        self.info = getattr(obj, 'info', None)
        self._suffix = None

    @property
    def suffix(self):
        if not self._suffix:
            self._suffix = self._get_suffix_()
        return self._suffix

    def _get_suffix_(self):
        if numpy.all(numpy.isnan(self)):
            return {'sign': '[noA.U.]', 'exp': None}

        min_val_exp = numpy.log10(self.min())

        exp_diff = {}
        for prefix, dic in self.prefixes.items():
            exp_value = dic['exp']
            exp_diff[prefix] = abs(min_val_exp - exp_value)

        prefix = min(exp_diff, key=exp_diff.get)

        suffix = self.prefixes[prefix]['sign'] + self.unit

        return suffix

    def Normalize(self):
        self /= self.max()
        self._suffix = "A.U."
        return self

    def __repr__(self):
        return self.__str__()

    def __str__(self):

        return super().__str__() + f"[{self.suffix}]"

    def __getitem__(self, *args):
        return UnitArray(super().__getitem__(*args), unit=self.unit)


# -
