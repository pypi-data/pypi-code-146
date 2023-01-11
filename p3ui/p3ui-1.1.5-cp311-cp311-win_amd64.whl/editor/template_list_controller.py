from p3ui import *
from ._config import *
from ..element import Icons


class AddTemplateDialog(Dialog):

    def __init__(self, editor):
        super().__init__(
            label='Create Template',
            content=Column(
                padding=(2 | em, 2 | em),
                children=[
                    input := InputText(
                        width=(20 | em, 0, 0), label='name',
                        on_change=self.eval
                    ),
                    Button(
                        disabled=lambda: len(input.value) == 0,
                        label='create template',
                        on_click=self._on_create
                    ),
                ]
            )
        )
        self.editor = editor
        self.input = input

    def _on_create(self):
        self.editor.create_template(self.input.value)
        self.close()


class TemplateListController:

    def __init__(self, template, editor):
        self.add_template_dialog = AddTemplateDialog(editor)
        editor.root_node.add(self.add_template_dialog)
        editor.root_node.unique.add_template_button.on_click = self.add_template_dialog.show

        self.template = template
        self.editor = editor

        class Item(Row):

            def __init__(self):
                self.template = None
                self._text = Text('xxx')
                self._info_text = Text('', color=emphasize_color)
                super().__init__(
                    padding=(0.618 | em, 0.618 | em),
                    children=[
                        self._text,
                        self._info_text
                    ],
                    on_mouse_down=lambda _: editor.select(self.template),
                    on_mouse_enter=lambda _: template.eval(),
                    on_mouse_leave=lambda _: template.eval()
                )

            def eval(self):
                if self.hover:
                    self.background_color = active_color
                elif editor.selected_template == self.template:
                    self.background_color = selected_color
                else:
                    self.background_color = list_background_color_even if model.index % 2 == 0 else list_background_color_odd
                self.color = 'black' if self.hover else None
                modified = editor.module_proxy.proxy_for_definition(self.template.Definition).modified
                if modified:
                    self._info_text.value = 'modified'
                else:
                    self._info_text.value = ''

            def init(self, index, template):
                self.template = template
                self._text.value = f'{Icons.Layers} {self.template.__name__}'

        self.repeater = Repeater(
            target_container=template,
            delegate=Item,
            delegate_init=lambda index, item, target: target.init(index, item)
        )
        self._eval = template.eval
        template.eval = self.eval
        self.eval()

    def _on_select(self):
        self.editor.select(Repeater.data)

    def clear(self):
        while len(self.template.content.children) > 0:
            self.template.content.remove(self.template.content.children[0])

    def eval(self):
        if self.editor.module_proxy:
            self.repeater.eval(self.editor.module_proxy.templates)
        else:
            self.repeater.eval([])
        self._eval()
