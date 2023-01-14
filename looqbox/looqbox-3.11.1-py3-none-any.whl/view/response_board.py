from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject


class ResponseBoard(LooqObject):

    def __init__(self, content=None, action=None, dispose=None):
        super().__init__()
        if action is None:
            action = []
        if content is None:
            content = []
        self.content = content
        self.action = action
        self.dispose = dispose

    def to_json_structure(self, visitor: BaseRender):
        return visitor.response_board_render(self)
