#!/usr/bin/env python3
'''
Omegaconf utility functions.
'''

from typing import Any

from omegaconf import OmegaConf, DictConfig  # pylint: disable=import-self


def get(config: DictConfig, name: str, default: Any = None) -> Any:
    '''
    Get a nested parameter such as foo.bar.baz from an Omegaconf configuration
    object, with default value.

    Args:
        config:
            The configuration object.

        name:
            The nested parameter name. It will be split on ".".

        default:
            An optional default value. Default: None

    Returns:
        The parameter value, or the default value if any of the nested values
        are missing or the resulting value is None.
    '''
    value = config
    for component in name.split('.'):
        try:
            value = getattr(value, component)
        except AttributeError:
            return default
    if value is None:
        return default
    return value


def get_container(
    config: DictConfig,
    name: str,
    *,
    default: Any = None,
    resolve: bool = True
) -> Any:
    '''
    A wrapper around get() that transforms the result with OmegaConf.to_container.

    Args:
        config:
            Same as get().

        name:
            Same as get().

        default:
            Same as get().

        resolve:
            Passed through to to_container(). If True, the resolvers will be
            resolved before creating the container.

    Returns:
        Same as get().
    '''
    result = get(config, name, default=default)
    if OmegaConf.is_config(result):
        result = OmegaConf.to_container(result, resolve=resolve)
    return result
