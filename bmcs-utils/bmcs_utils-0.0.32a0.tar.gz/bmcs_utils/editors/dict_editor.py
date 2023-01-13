

import traits.api as tr
from .editors import EditorFactory
import ipywidgets as ipw

class DictEditor(EditorFactory):
    """Polymorphic instance editor.
    """

    _values = tr.Dict

    def render(self):
        print('render dict')
        self._values = getattr(self.model, self.name)
        list_keys = list(items)
        print('values', self._values)
        if len(list_keys) == 0:
            key = '<empty list>'
            return ipw.VBox()
        else:
            key = list_keys[0]
            drop_down = ipw.Dropdown(description=self.label, value=key,
                                     tooltip=self.tooltip, options=list_keys)
            drop_down.observe(self._item_selection_changed,'value')
            self.instance_pane = ipw.VBox(self._render_instance(key))
            return ipw.VBox([drop_down, self.instance_pane])

    def _render_instance(self, key):
        app_window = self.controller.app_window
        view_model = self._values[key]
        instance_controller = view_model.get_controller(app_window=app_window)
        model_editor = instance_controller.model_editor
        return [model_editor]

    def _item_selection_changed(self, event):
        key = event['new']
        self.instance_pane.children = self._render_instance(key)
