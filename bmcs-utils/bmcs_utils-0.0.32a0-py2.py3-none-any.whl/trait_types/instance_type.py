
from .trait_types import TraitBase
import traits.api as tr
from bmcs_utils.editors import InstanceEditor

class Instance(TraitBase, tr.Instance):
    editor_factory = InstanceEditor

    def get_sub_nodes(self):
        return []

    def set(self, obj, name, value):
        self.pre_setattr(obj, name)
        self.set_value(obj, name, value)
        self.post_setattr(obj, name, value)

    def pre_setattr(self, object, name):
        if name in object.depends_on:
            old_value = getattr(object, name + '_', None)
            if old_value:
                old_value.parents.remove(object)

    def init_setattr(self, object, name, value):
        value.parents.add(object)
        object.notify_graph_change('Notification from child %s' % value)

    def post_setattr(self, object, name, value):
        if value and name in object.depends_on:
            value.parents.add(object)
            object.notify_graph_change('Notification from child %s' % value)

    def get(self, obj, name):
        val = self.get_value(obj, name)
        if val is None:
            val = self.default_value
        return val

