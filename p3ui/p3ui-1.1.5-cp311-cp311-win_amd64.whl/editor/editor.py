import asyncio
import gc
import importlib
import inspect
import sys
import types
from types import ModuleType, SimpleNamespace
from p3ui import Node, Definition, Layout
from ._config import emphasize_color
from .add_icon_dialog import AddIconDialog
from .add_node_dialog import AddNodeDialog
from .editor_highlighting import EditorHighlighting
from .attribute_editor import AttributeEditor
from .template_list_controller import TemplateListController
from .module_proxy import ModuleProxy
from .editor_template import EditorTemplate
from .template_tree_controller import TemplateTreeController


async def stress(tpl):
    while True:
        try:
            tpl.eval()
        except Exception as e:
            print(e)
        await asyncio.sleep(0)


class Editor(ModuleProxy.Observer):

    def __init__(self, window):
        self.window = window
        self._root_node = EditorTemplate()
        self._eval = self.root_node.eval
        self._root_node.eval = self.eval
        self._root_node.unique.save_button.on_click = self.save

        #
        # keep track of edited module by using proxy
        self._module: ModuleType = None
        self._module_proxy: ModuleProxy = None

        AddIconDialog.Instance = AddIconDialog()
        self._root_node.add(AddIconDialog.Instance)

        AddNodeDialog.Instance = AddNodeDialog(self)
        self._root_node.add(AddNodeDialog.Instance)

        #
        # if you like heat:
        #  asyncio.get_event_loop().create_task(stress(self._root_node))
        #  asyncio.get_event_loop().create_task(stress(self._root_node))
        #  asyncio.get_event_loop().create_task(stress(self._root_node))
        #  asyncio.get_event_loop().create_task(stress(self._root_node))

        #
        # on resize, highlighting needs to be updated
        self._root_node.on_resize = self._on_resize

        #
        # currently selected template and it's instantiation
        self._selected_template: Node = None
        self._node_tree: Node = None
        #
        # active and selected node of the instantiated template
        self._active_node: Node = None
        self._selected_node: Node = None
        self._editor_highlighting = EditorHighlighting(self)

        self._clipboard_node: 'NodyProxy' = None
        self._clipboard_is_cut: bool = False

        #
        # code behind (the editor template)
        self._template_list: TemplateListController = TemplateListController(
            template=self.root_node.unique.template_list,
            editor=self
        )
        self._template_tree_controller: TemplateTreeController = TemplateTreeController(
            template=self.root_node.unique.template_tree_template,
            editor=self
        )
        self._node_attribute_controller: AttributeEditor = AttributeEditor(
            template=self.root_node.unique.node_attribute_template,
            editor=self
        )

    @property
    def root_node(self):
        return self._root_node

    @property
    def selected_template(self):
        return self._selected_template

    @property
    def node_tree(self):
        return self._node_tree

    @property
    def active_node(self):
        return self._active_node

    @active_node.setter
    def active_node(self, node):
        self._active_node = node
        self._editor_highlighting.update()
        self._root_node.eval()
        gc.collect()
        print('node count', self.module_proxy.node_count, ' ', Node.node_count)

    @property
    def selected_node(self):
        return self._selected_node

    @property
    def selected_node_proxy(self):
        if self.selected_node is None:
            return None
        return self.module_proxy.proxy_for_node(self.selected_node)

    @selected_node.setter
    def selected_node(self, node):
        self._selected_node = node
        self._editor_highlighting.update()
        self._root_node.eval()

    @property
    def module(self):
        return self._module

    @module.setter
    def module(self, module: types.ModuleType):
        self._module = module
        self._module_proxy = ModuleProxy(module=module, observer=self)
        if len(self.module_proxy.templates) > 0:
            self.select(self.module_proxy.templates[0])

        self._template_list.eval()

    @property
    def module_proxy(self):
        return self._module_proxy

    def _reset_selection(self):
        if self._selected_template:
            self.module_proxy.release_all_node_instances()
            self.selected_node = None
            self.active_node = None
            self._root_node.unique.view_panel.remove(self._node_tree)
            self._node_tree = None
            self._selected_template = None

    def reload(self):
        self.select(self._selected_template)

    def select(self, template):
        self._reset_selection()
        if template is None:
            return
        #
        # instantiate tree, module instance will register all created instances
        self._selected_template = template
        self._node_tree = template()
        #
        # fix: root node not registered yet
        self.module_proxy.on_create_defined_node(self._node_tree, self._node_tree.Definition)
        #
        # make it visible, update / eval view state
        self._root_node.unique.view_panel.add(self._node_tree)
        self._root_node.eval()
        self._template_list.eval()
        gc.collect()
        self.selected_node = self._node_tree

        async def update():
            """ the highlight needs absolute coordinates which are only available after a frame was rendered """
            await asyncio.sleep(0)
            self._editor_highlighting.update()

        asyncio.create_task(update())

    def _on_resize(self, _):
        self._editor_highlighting.update()

    def load_module(self, module_path):
        module = importlib.import_module(module_path)

        # init = inspect.getsourcelines(module.init)
        module.init(self.window.user_interface, self.window.dpi, 13)
        self.module = module

    def create_template(self, name):
        #
        # we have to pass the new class node_type to "super":
        # https://stackoverflow.com/questions/70132199/dynamic-inheritance-with-type-and-super
        def init(self, **kwargs):
            nonlocal new_class
            self.unique = SimpleNamespace()
            super(new_class, self).__init__(**{**self.Definition.derive_kwargs_for(self), **kwargs})

        new_class = type(f'{name}', (Layout,), {
            "__init__": init,
            "Definition": Definition.create(Layout)(children=[])
        })
        #
        # register template to runtime
        self.module_proxy.add_template(new_class)
        #
        # update visuals
        self.root_node.eval()

    def move_selected_node_up(self):
        if self.selected_node_proxy is None:
            return
        self.selected_node_proxy.move_up_as_sibling()

    def move_selected_node_down(self):
        if self.selected_node_proxy is None:
            return
        self.selected_node_proxy.move_down_as_sibling()

    def remove_selected_node(self):
        proxy = self.selected_node_proxy
        if proxy is None:
            return
        self.selected_node = None
        proxy.remove()

    def on_value_changed(self):
        if self.root_node:
            self.root_node.eval()

        async def update():
            self._editor_highlighting.update()

        asyncio.get_event_loop().create_task(update())

    def on_composition_changed(self):
        if self.root_node:
            self.root_node.eval()

        async def update():
            self._editor_highlighting.update()

        asyncio.get_event_loop().create_task(update())

    def eval(self):
        self._root_node.unique.save_button.disabled = not self.module_proxy.modified
        self._root_node.unique.save_button.background_color = emphasize_color if self.module_proxy.modified else None
        self._root_node.unique.save_button.color = 'black' if self.module_proxy.modified else None
        self._eval()

    def save(self):
        self.module_proxy.save()
        self.root_node.eval()

    @property
    def clipboard_node(self):
        return self._clipboard_node

    def cut_selected(self):
        self._clipboard_node = self.selected_node_proxy
        self._clipboard_is_cut = True
        self.on_value_changed()

    def copy_selected(self):
        self._clipboard_node = self.selected_node_proxy
        self._clipboard_is_cut = False
        self.on_value_changed()

    def paste_selected(self):
        if self._clipboard_node is None:
            return
