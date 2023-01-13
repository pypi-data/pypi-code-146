# _*_coding:utf-8_*_
from django.urls import re_path
from django.conf.urls import static
from django.conf import settings

from .apis.finance_transacts import FinanceTransacts
from .apis.finance_transact import FinanceTransact
from .apis.finance_pay_mode import FinancePayMode
# from apps.payment.apis.finance_pay import FinancePay
# from apps.payment.apis.finance_pay_test import FinanceTestPay
from .apis.finance_currency import FinanceCurrency
from .apis.finance_sand_box import FinanceSandBox
from .apis.finance_contact_book import UserContactBook
from .apis.finance_statistic import FinanceStatistic
from .apis.finance_balance import FinanceBalance
from .apis.finance_payment_type import FinancePaymentType

urlpatterns = [
    re_path(r'^transacts/?$', FinanceTransacts.as_view(), ),
    re_path(r'^transact/?$', FinanceTransact.as_view(), ),
    re_path(r'^pay_mode/?$', FinancePayMode.as_view(), ),
    # re_path(r'^_pay/?$', FinancePay.as_view(), ),
    # re_path(r'^_pay_test/?$', FinanceTestPay.as_view(), ),
    re_path(r'^currency/?$', FinanceCurrency.as_view(), ),
    re_path(r'^sand_box/?$', FinanceSandBox.as_view(), ),
    re_path(r'^contact_book/?$', UserContactBook.as_view(), ),
    # re_path(r'^_export/?$', ExportExcel.as_view(), ),
    re_path(r'^statistic/?$', FinanceStatistic.as_view(), ),
    re_path(r'^balance/?$', FinanceBalance.as_view(), ),
    re_path(r'^distribution/?$', FinanceTransact.distribution, ),
    re_path(r'^write_off/?$', FinanceTransact.write_off, ),
    re_path(r'^payment_type/?$', FinancePaymentType.as_view(), ),

    # 该功能已使用finance_transact的POST方法代替
    # re_path(r'^_transact_add/?$', finance_transact_add.FinanceTransactAdd.as_view(), ),
    #
    # # 这里要填写/static/和/media/路径，否则django不会返回静态文件。
    # re_path(
    #     "static/(?P<path>.*)$",
    #     static.serve,
    #     {"document_root": settings.STATIC_ROOT, "show_indexes": False},
    #     "static"
    # ),
    # re_path(
    #     "media/(?P<path>.*)$",
    #     static.serve,
    #     {"document_root": settings.MEDIA_ROOT, "show_indexes": False},
    #     "media"
    # ),
]
