import inspect
import threading
import copy
from typing import Tuple


class Definition:
    """ defines how note instantiation takes place """

    #
    # this is only used by the editor
    thread_local = threading.local()
    thread_local.map_definition = None

    def __init__(self, node_type, identifier=None, children=None, **kwargs):
        self.node_type = node_type
        self.identifier = identifier
        self.kwargs = {key: value for key, value in kwargs.items()}
        self.parent: Definition = None
        self._children = children
        if self._children is None:
            self._children = []
        for child in self._children:
            child.parent = self

    @staticmethod
    def create(node_type, identifier=None) -> 'Definition':
        """ e.g. creates a more specific Definition that only needs kwargs """
        return lambda **kwargs: Definition(node_type, identifier, **kwargs)

    def make_copy(self):
        """ create a deep copy """
        result = Definition(node_type=self.node_type, identifier=self.identifier, kwargs=copy.deepcopy(self.kwargs))
        for child in self.children:
            result.add(child.make_copy())
        return result

    @staticmethod
    def is_template_class(cls):
        """ check if a given class node_type is a template node_type """
        return inspect.isclass(cls) and hasattr(cls, 'Definition') and cls.Definition.node_type in inspect.getmro(cls)

    def contains(self, node_type, recursive=True):
        if any([child.node_type == node_type for child in self.children]):
            return True
        if recursive:
            for child in self.children:
                if child.contains(node_type):
                    return True
        return False

    def remove(self):
        if self.parent is not None:
            self.parent._children.remove(self)
            self.parent.modified = True
            self.parent = None

    @property
    def class_name(self):
        """ get class name of the node_type defined by this instance """
        return self.node_type.__name__

    def iterate_identifiers(self) -> Tuple[str, type]:
        """ iterates all named nodes and it's types """
        if self.identifier:
            yield self.identifier, self.node_type
        for child in self.children:
            for identifier, cls in child.iterate_identifiers():
                yield identifier, cls

    @property
    def children(self):
        """ get all child definitions """
        return self._children

    @children.setter
    def children(self, value):
        """ probably this will never happen"""
        self._children = value

    def add(self, definition_node):
        """ add child definition """
        self.children.append(definition_node)
        definition_node.parent = self

    def instantiate_for(self, template_instance):
        """ this is used internally to instantiate recursively """
        #
        # recursively instantiate subtree (depth first)
        if self.children:
            instance = self.node_type(**self.kwargs, children=[
                child.instantiate_for(template_instance) for child in self.children
            ])
        else:
            instance = self.node_type(**self.kwargs)
        #
        # register to named
        if self.identifier:
            setattr(template_instance.named, self.identifier, instance)
        #
        # register this node as being an instance of this def and map it to the node proxy
        if hasattr(self.thread_local, 'on_create_defined_node'):
            self.thread_local.on_create_defined_node(instance, self)
        return instance

    def derive_kwargs_for(self, template_instance):
        """ derive kwargs that can be passed to super() in the generated code """
        kwargs = copy.deepcopy(self.kwargs)
        kwargs['children'] = [
            definition.instantiate_for(template_instance) for definition in self.children
        ]
        return kwargs

    @property
    def is_component(self):
        return hasattr(self.node_type, 'Definition')
