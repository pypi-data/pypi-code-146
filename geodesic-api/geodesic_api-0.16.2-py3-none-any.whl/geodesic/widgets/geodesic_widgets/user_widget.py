#!/usr/bin/env python
# coding: utf-8

# Copyright (c) seerai.
# Distributed under the terms of the Modified BSD License.

"""
UI widget for displaying a User 
"""

from ._frontend import module_name, module_version
from geodesic.utils import DeferredImport

ipywidgets = DeferredImport('ipywidgets')
traitlets = DeferredImport('traitlets')

class UserWidget(ipywidgets.DOMWidget):
    """
    Jupyter widget for displaying a user
    """
    _model_name = traitlets.Unicode('UserModel').tag(sync=True)
    _model_module = traitlets.Unicode(module_name).tag(sync=True)
    _model_module_version = traitlets.Unicode(module_version).tag(sync=True)
    _view_name = traitlets.Unicode('UserView').tag(sync=True)
    _view_module = traitlets.Unicode(module_name).tag(sync=True)
    _view_module_version = traitlets.Unicode(module_version).tag(sync=True)
    object_value = traitlets.Dict().tag(sync=True)

    def __init__(self, obj={}, **kwargs):
        super().__init__(**kwargs)
        self.object_value = dict(obj)
