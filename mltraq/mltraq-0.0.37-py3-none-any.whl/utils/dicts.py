import itertools


class ObjectDictionary(dict):
    def __init__(self, *args, **kwargs):
        if args == (None,) and not kwargs:
            super().__init__()
        else:
            super().__init__(*args, **kwargs)

    def __reduce__(self):
        return self.__class__, (dict(self),)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(key) from e

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as e:
            raise AttributeError(key) from e

    @classmethod
    def deep(cls, d):
        if isinstance(d, ObjectDictionary):
            return d
        elif not isinstance(d, dict):
            return d
        else:
            return ObjectDictionary({k: ObjectDictionary.deep(v) for k, v in d.items()})


def ordered_dict_equality(p, q):
    return p == q and all(k1 == k2 for k1, k2 in zip(p, q))


def product_dict(**kwargs):
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))
