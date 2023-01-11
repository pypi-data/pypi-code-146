from p3ui import *
from collections import namedtuple
from ._config import *
from p3ui.element import Icons
from .attribute_editor_template import AttributeEditorTemplate

from .template_tree_template import TemplateTreeTemplate


class EditorTemplate(Row):

    def __init__(self):
        super().__init__(
            children=[
                left_column := Column(
                    padding=(0.618 | em, 0.618 | em),
                    width=(24 | em, 0, 0),
                    children=[
                        Text(
                            value='Components:'
                        ),
                        Row(
                            padding=(0 | px, 0 | px),
                            height=(1 | em, 2, 1),
                            justify_content=Justification.SpaceBetween,
                            align_items=Alignment.Stretch,
                            children=[
                                template_list := ScrolledColumn(),
                                Column(
                                    padding=(0 | px, 0 | px),
                                    width=(auto, 0, 0),
                                    height=(auto, 1, 0),
                                    justify_content=Justification.Start,
                                    children=[
                                        add_template_button := Button(
                                            width=(auto, 0, 0),
                                            height=(auto, 0, 0),
                                            label=f'{Icons.Add}'
                                        ),
                                        Spacer(height=(1 | em, 0, 0)),
                                        save_button := Button(
                                            width=(auto, 0, 0),
                                            height=(auto, 0, 0),
                                            label=f'{Icons.Save}'
                                        ),
                                        Spacer(height=(1 | em, 1, 0)),
                                        Button(
                                            width=(auto, 0, 0),
                                            height=(auto, 0, 0),
                                            label=f'{Icons.Delete}'
                                        ),
                                        Spacer(height=(1 | em, 0, 0))
                                    ]
                                )
                            ]
                        ),
                        Spacer(height=(1 | em, 0, 0)),
                        Text(value='Component Structure:'),
                        template_tree_template := TemplateTreeTemplate(),
                    ]
                ),
                Column(
                    padding=(0.618 | em, 0.618 | em),
                    children=[
                        Text('Component Instance View:'),
                        ScrollArea(
                            children=[
                                highlight_root := Row(
                                    padding=(0 | px, 0 | px),
                                    width=(auto, 0, 0),
                                    height=(auto, 0, 0),
                                    children=[
                                        view_panel := Row(
                                            width=(auto, 0, 0),
                                            height=(auto, 0, 0),
                                            padding=(0 | px, 0 | px)
                                        )
                                    ]
                                ),
                            ]
                        )
                    ]
                ),
                node_attribute_template := AttributeEditorTemplate()
            ]
        )

        self.unique = namedtuple('NamedNodes', 'left_column '
                                               'template_list '
                                               'view_panel '
                                               'add_template_button '
                                               'template_tree_template '
                                               'node_attribute_template '
                                               'save_button '
                                               'highlight_root')(
            left_column=left_column,
            template_list=template_list,
            view_panel=view_panel,
            add_template_button=add_template_button,
            template_tree_template=template_tree_template,
            node_attribute_template=node_attribute_template,
            save_button=save_button,
            highlight_root=highlight_root
        )
