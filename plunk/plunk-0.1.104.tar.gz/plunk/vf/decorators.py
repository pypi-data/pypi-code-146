from warnings import warn


def deprecate_attr(attr_name, attr_replacement_name):
    """Deprecates an attribute by printing a deprecation message and bind the usage of
    this attribute with another non-deprecated attribute.

    >>> @deprecate_attr('deprecated_attr', 'valid_attr')
    ... class Foo:
    ...     valid_attr = 'Some valid attribute'

    >>> foo = Foo()
    >>> foo.deprecated_attr
    'Some valid attribute'

    >>> foo.deprecated_attr = 'Got deprected attribute'
    >>> foo.deprecated_attr 
    'Got deprected attribute'

    >>> foo.valid_attr
    'Got deprected attribute'
    """

    def wrapper(cls):
        def warn_deprecated_sig_attr():
            warn(
                f'"{cls.__qualname__}.{attr_name}" is deprecated, consider using "{cls.__qualname__}.{attr_replacement_name}" instead.',
                DeprecationWarning,
                stacklevel=2,
            )

        def get_attr(self):
            warn_deprecated_sig_attr()
            return getattr(self, attr_replacement_name)

        def set_attr(self, value):
            setattr(self, attr_replacement_name, value)

        prop = property(get_attr, set_attr)
        setattr(cls, attr_name, prop)
        return cls

    return wrapper
