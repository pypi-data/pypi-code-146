# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class MoonThreejs(Component):
    """A MoonThreejs component.


Keyword arguments:

- id (string; required)

- height (number; default 8)

- nforests (number; default 3)

- ntrees (number; default 1000)

- radius (number; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'moon_threejs'
    _type = 'MoonThreejs'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, radius=Component.REQUIRED, height=Component.UNDEFINED, ntrees=Component.UNDEFINED, nforests=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'height', 'nforests', 'ntrees', 'radius']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'height', 'nforests', 'ntrees', 'radius']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'radius']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(MoonThreejs, self).__init__(**args)
