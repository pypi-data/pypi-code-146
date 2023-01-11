#!/usr/bin/env python
from .elements import abundance_dict


def __dir__():
    """forward attributes for autocompletion"""
    return list(abundance_dict.keys())


locals().update(abundance_dict)
