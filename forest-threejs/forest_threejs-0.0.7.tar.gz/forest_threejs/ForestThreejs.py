# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ForestThreejs(Component):
    """A ForestThreejs component.


Keyword arguments:

- id (string; required)

- spacing (number; default 30)

- stats (boolean; default True)

- totalX (number; default 100)

- totalZ (number; default 100)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'forest_threejs'
    _type = 'ForestThreejs'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, totalX=Component.UNDEFINED, totalZ=Component.UNDEFINED, spacing=Component.UNDEFINED, stats=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'spacing', 'stats', 'totalX', 'totalZ']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'spacing', 'stats', 'totalX', 'totalZ']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(ForestThreejs, self).__init__(**args)
