from mrkutil.responses import ResponseHelper
from mrkutil.base import BaseHandler
import logging

logger = logging.getLogger(__name__)


class ExampleHandler(BaseHandler):

    @staticmethod
    def name():
        return 'test_method'

    def process(self, data, corr_id):
        self.data = data.get("request", None)
        logger.info("Handle example")
        return ResponseHelper.get_response(200, f"example response from service with request data={data}")
