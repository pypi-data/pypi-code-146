import time
import os
import datetime

from django.db.models import Q
from django.db.models import F
from rest_framework.response import Response

from xj_user.models import *
from xj_finance.models import *

from decimal import Decimal


class FinanceTransactListService:

    def __init__(self):
        pass

    # 检查账号余额是否正确
    @staticmethod
    def get(param=None):
        
        
        return 1

