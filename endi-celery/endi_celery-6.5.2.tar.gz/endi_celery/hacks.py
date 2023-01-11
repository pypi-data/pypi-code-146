"""
endi related hacks used to ensure code compatibility from within celery tasks
"""
from pyramid_layout.config import create_layout_manager
from endi.views.render_api import Api


class DummyEvent:
    def __init__(self, request, context):
        self.request = request
        self.request.context = context
        self.context = context


def setup_rendering_hacks(request, context):
    event = DummyEvent(request, context)
    create_layout_manager(event)
    request.api = Api(context, request)
