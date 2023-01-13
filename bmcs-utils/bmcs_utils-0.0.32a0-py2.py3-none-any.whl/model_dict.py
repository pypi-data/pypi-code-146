
from .model import Model
from .trait_types.dict_type import Dict
import traits.api as tr
from .view import View

class ModelDict(Model):

    items = Dict({})

    def __setitem__(self, key, value):
        old_value = self.items.get(key, None)
        if old_value:
            old_value.parents.remove(self)
        value.name = str(key)
        self.items[key] = value
        value.parents.add(self)
        self.notify_graph_change('Notification from child %s' % 'item')

    def __delitem__(self, key):
        value = self.items[key]
        value.parents.remove(self)
        del self.items[key]
        self.notify_graph_change('Notification from child %s' % 'item')

    def __getitem__(self, key):
        return self.items[key]

    tree = tr.Property
    def _get_tree(self):
        return list(self.items)

    tree_submodels = tr.Property(depends_on='graph_changed')
    @tr.cached_property
    def _get_tree_submodels(self):
        return [self.items[key] for key in self.tree]

    def values(self):
        return self.items.values()

    def keys(self):
        return self.items.keys()