from p3ui import Definition


class AttributeProxy:

    def __init__(self, node_proxy: 'NodeProxy'):
        object.__setattr__(self, "node_proxy", node_proxy)

    def __getattr__(self, key):
        if len(self.node_proxy.instances) == 0:
            return None
        return getattr(self.node_proxy.instances[0], key)

    def __setattr__(self, key, value):
        for instance in self.node_proxy.instances:
            setattr(instance, key, value)
        self.node_proxy.definition.kwargs[key] = value
        self.node_proxy.mark_modified()
        self.node_proxy.module_proxy.on_value_changed()


class NodeProxy:
    """ one proxy per definition which links the definition to the instantiated tree """

    def __init__(self, module_proxy: 'ModuleProxy', definition=None, children=[]):
        self.module_proxy = module_proxy
        self.definition = definition
        self.attributes = AttributeProxy(self)
        self.modified = False
        self.children = children
        self.parent = None
        for child in children:
            child.parent = self
        self._node_instances = []

    @property
    def identifier(self):
        return self.definition.identifier

    @identifier.setter
    def identifier(self, value):
        self.definition.identifier = value
        self.mark_modified()
        self.module_proxy.on_value_changed()

    @property
    def instances(self):
        return self._node_instances

    def add_instance(self, node):
        self._node_instances.append(node)

    def remove_instance(self, node):
        self._node_instances.remove(node)

    def clear_instances(self):
        self._node_instances.clear()

    def attribute_is_set(self, name):
        """ check if attribute is set in the definition """
        return name in self.definition.kwargs

    def make_default_value(self, name):
        """ get default attribute for any attribute, used for reset """
        return getattr(self.definition.node_type(), name)

    def set_attribute_enabled(self, name, yes):
        if yes:
            #
            # get the actual value (which should be the default value) and write it to the definition
            if name == 'identifier':
                self.definition.kwargs['identifier'] = ''
            else:
                self.definition.kwargs[name] = getattr(self.attributes, name)  # self.make_default_value()
        else:
            #
            # set actual state of all instantiated nodes to default, then remove from definition
            if name != 'identifier':
                setattr(self.attributes, name, self.make_default_value(name))
            self.definition.kwargs.pop(name)
        self.mark_modified()
        self.module_proxy.on_value_changed()

    @property
    def can_move_up_as_sibling(self):
        definition = self.definition
        if definition.parent is None:
            return False
        return definition.parent.children.index(definition) > 0

    @property
    def can_move_down_as_sibling(self):
        definition = self.definition
        if definition.parent is None:
            return False
        return definition.parent.children.index(definition) < len(definition.parent.children) - 1

    def remove(self):
        """ remove self from parent """
        if self.definition.parent is None:
            return
        while len(self.instances) > 0:
            instance = self.instances[0]
            self.remove_instance(instance)
            instance.remove()
        self.mark_modified()
        self.definition.remove()
        self.module_proxy.on_composition_changed()

    @property
    def index(self):
        if self.definition.parent is None:
            return -1
        return self.definition.parent.children.index(self.definition)

    def move_as_sibling(self, offset):
        index = self.index
        for instance in self.instances:
            parent = instance.parent
            instance.remove()
            parent.insert(index + offset, instance)
        children = self.definition.parent.children
        children.insert(index + offset, children.pop(index))
        self.mark_modified()
        self.module_proxy.on_composition_changed()

    def move_up_as_sibling(self):
        if not self.can_move_up_as_sibling:
            return
        self.move_as_sibling(-1)

    def move_down_as_sibling(self):
        if not self.can_move_down_as_sibling:
            return
        self.move_as_sibling(+1)

    def mark_modified(self):
        it = self
        while it:
            it.modified = True
            it = it.parent

    def mark_clean(self):
        self.modified = False
        for child in self.children:
            child.mark_clean()

    @property
    def template_proxy(self):
        """ gets the root node proxy (the template proxy) of this node proxy """
        it = self
        while it is not None:
            if it.definition.is_component:
                return it
            it = it.parent
        return None

    def add_child(self, node_type, identifier=''):
        """ adds a -new- child definition """
        child_definition = Definition(node_type, identifier)

        target_proxy = self
        target_definition: Definition = self.definition
        #
        # if the target definition is a component,
        # the definition to be added must be "transcluded" there
        if target_definition.is_component:
            target_definition = target_definition.node_type.Definition
            target_proxy = self.module_proxy.proxy_for_definition(target_definition)

        target_definition.add(child_definition)
        child = self.module_proxy.make_proxy(child_definition)
        self.children.append(child)
        child.parent = self
        for instance in target_proxy.instances:
            instance.add(child_definition.instantiate_for(None))

        self.mark_modified()
        self.module_proxy.on_composition_changed()

    def can_contain(self, proxy):
        return True  # todo
