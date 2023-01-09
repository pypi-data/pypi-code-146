from ..models.roles import Leader
from .base import BaseIndex


class LeaderIndex(BaseIndex):

    def get_model(self):
        return Leader
