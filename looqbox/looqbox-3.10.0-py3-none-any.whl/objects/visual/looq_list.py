from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject


class ObjList(LooqObject):

    def __init__(self, link_list=None, title=None, tab_label=None):
        super().__init__()
        if link_list is None:
            link_list = []
        if title is None:
            title = []
        self.link_list = link_list
        self.title = title
        self.tab_label = tab_label

    def to_json_structure(self, visitor: BaseRender):
        return visitor.list_render(self)
