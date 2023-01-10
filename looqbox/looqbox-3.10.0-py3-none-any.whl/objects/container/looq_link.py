from looqbox.objects.container.abstract_container import AbstractContainer
from looqbox.render.abstract_render import BaseRender


class ObjLink(AbstractContainer):

    def __init__(self, *children, question, **properties):
        """
        :param children: Children to be contained.
        :param question: Question or external link to redirect the user.
        :param properties: properties derived from parent:  --value
                                                            --render_condition
                                                            --tab_label
                                                            --css_options
        """
        super().__init__(*children, **properties)
        self.question = question

    def to_json_structure(self, visitor: BaseRender):
        return visitor.link_render(self)
