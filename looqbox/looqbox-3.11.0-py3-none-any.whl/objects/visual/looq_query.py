from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject


class ObjQuery(LooqObject):

    def __init__(self, queries, total_time):
        super().__init__()
        self.queries = queries
        self.total_time = total_time

    def to_json_structure(self, visitor: BaseRender):
        return visitor.query_render(self)
