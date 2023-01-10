# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TextInput(Component):
    """A TextInput component.


Keyword arguments:

- id (string; optional)

- label (string; required)

- value (string; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'bubble_train'
    _type = 'TextInput'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, label=Component.REQUIRED, value=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'label', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'label', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['label']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(TextInput, self).__init__(**args)
