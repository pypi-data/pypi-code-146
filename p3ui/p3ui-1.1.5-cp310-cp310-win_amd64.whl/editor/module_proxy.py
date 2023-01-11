import abc
import importlib
import inspect
import types
from pathlib import Path
from typing import Dict, List

from p3ui import Node
from . import write_template

from .definition import Definition
from .node_proxy import NodeProxy


class Version:

    def __init__(self, major: int, minor: int, patch: int):
        self.major, self.minor, self.patch = major, minor, patch

    def __repr__(self):
        return f'{self.major}.{self.minor}.{self.patch}'

    def from_string(self, version_string):
        self.major, self.minor, self.patch = [int(x) for x in version_string.split('.')]


class ModuleProxy:
    class Observer(abc.ABC):

        @abc.abstractmethod
        def on_composition_changed(self):
            pass

        @abc.abstractmethod
        def on_value_changed(self):
            pass

    """
    this loads/manages a module and creates (exactly) one proxy for each definition found in any component.
    if a node is about to be created it is also assigned to the proxy tree in `on_create_defined_node`.

    """

    def __init__(self, module, observer: Observer = None):
        if isinstance(module, str):
            module = importlib.import_module(module)
        self.module: types.ModuleType = module
        self.observer: Observer = observer

        self._templates = None

        self._map_definition_to_proxy: Dict[Definition, NodeProxy] = dict()
        self._map_node_to_proxy: Dict[Node, NodeProxy] = dict()
        #
        # register for node creation
        Definition.thread_local.on_create_defined_node = self.on_create_defined_node
        self.reload(reload_module=False)

    @property
    def node_count(self):
        return len(self._map_node_to_proxy)

    def add_template(self, template):
        self._templates.append(template)
        definition = template.Definition
        proxy = NodeProxy(
            module_proxy=self,
            definition=definition,
            children=[self._create_proxy(child) for child in definition.children]
        )
        proxy.modified = True
        self._map_definition_to_proxy[definition] = proxy

    def make_proxy(self, definition, modified=True):
        proxy = NodeProxy(
            module_proxy=self,
            definition=definition,
            children=[self._create_proxy(child) for child in definition.children]
        )
        self._map_definition_to_proxy[definition] = proxy
        return proxy

    def _create_proxy(self, definition):
        """ recursively wolk down one definition tree and create proxies"""
        if self.proxy_for_definition(definition) is not None:
            raise RuntimeError('malformed proxy structure')
        print('def: ', definition.node_type)
        return self.make_proxy(definition, modified=False)

    def reload(self, reload_module=True):
        if reload_module:
            importlib.reload(self.module)
        self._map_definition_to_proxy.clear()
        self._map_node_to_proxy.clear()
        self._templates = list(self.list_template_types())
        #
        # create one proxy for each definition
        for template in self._templates:
            self._create_proxy(template.Definition)
        #
        # todo: log this
        for type in self._templates:
            print(f'using "{type.__name__}" from "{self.path_to_type(type)}"')

    def on_create_defined_node(self, node, definition):
        """ insert node into the proxy structure """
        proxy = self._map_definition_to_proxy.get(definition, None)
        self._map_node_to_proxy[node] = proxy
        proxy.add_instance(node)
        #
        # although not visible, we also add the node to the root proxy
        if hasattr(proxy.definition.node_type, 'Definition') and proxy.parent is not None:
            self.proxy_for_definition(proxy.definition.node_type.Definition).add_instance(node)

    def release_all_node_instances(self):
        for definition, proxy in self._map_definition_to_proxy.items():
            proxy.clear_instances()
        self._map_node_to_proxy.clear()

    def proxy_for_definition(self, definition: Definition):
        """ lookup proxy for a given definition """
        return self._map_definition_to_proxy.get(definition, None)

    def proxy_for_node(self, node: Node):
        """ lookup proxy for a given node """
        return self._map_node_to_proxy.get(node, None)

    @staticmethod
    def path_to_type(cls):
        return Path(inspect.getfile(cls))

    def list_template_types(self):
        """ iterate template classes / types """
        if self.module is None:
            return
        for name, obj in inspect.getmembers(self.module):
            if inspect.isclass(obj) and issubclass(obj, Node):
                if hasattr(obj, 'Definition') and isinstance(obj.Definition, Definition):
                    yield obj

    @property
    def templates(self):
        return self._templates

    @property
    def modified(self):
        return any([self._map_definition_to_proxy[template.Definition].modified for template in self._templates])

    @property
    def filename(self):
        """ get the proxied filename """
        return self.module.__file__

    def save(self):
        print('saving ', self.module.__file__)

        if hasattr(self.module, 'init'):
            #
            # get from module source
            init_source_lines = inspect.getsourcelines(self.module.init)[0]
        else:
            #
            # default to ..
            init_source_lines = [
                'def init(user_interface: UserInterface, dpi: float, font_size: int = 24):',
                '    pass'
            ]

        version = Version(1, 0, 0)

        with open(self.filename, 'w') as f:
            f.write(
                f'#\n'
                f'# this file is partially generated. edit width:\n'
                f'#    python -m p3ui.editor {self.module.__name__}\n'
                f'\n'
                f'from p3ui import *\n'
                f'from p3ui.editor import Definition\n'
                f'\n'
                f'version = \'{str(version)}\'\n'
                '\n\n'
            )
            f.writelines(init_source_lines)
            import functools

            def cmp(left, right):
                if left.Definition.contains(right):
                    return 1
                if right.Definition.contains(left):
                    return -1
                return 0

            sorted_templates = sorted(self._templates, key=functools.cmp_to_key(cmp))
            for template in sorted_templates:
                f.write(write_template(template))

        for proxy in self._map_definition_to_proxy.values():
            proxy.modified = False

    def on_composition_changed(self):
        if self.observer is None:
            return
        self.observer.on_composition_changed()

    def on_value_changed(self):
        if self.observer is None:
            return
        self.observer.on_value_changed()
