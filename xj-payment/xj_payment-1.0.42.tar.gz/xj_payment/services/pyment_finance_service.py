from xj_finance.services.finance_transact_service import FinanceTransactService

from ..models import PaymentOrder


class PaymentFinanceService:
    @staticmethod
    def post(out_trade_no):
        """
        their_account_id 对方账户ID
        platform 平台
        amount 金额
        currency 币种
        pay_mode 支付方式
        summary 摘要
        :return:
        """
        payment_message = PaymentOrder.objects.first(order_no=out_trade_no).first()
        data = {
            'platform_order_id': payment_message['order_no'],
            'total_amout':payment_message['total_amout'],
            # 'platform_id'
        }
        FinanceTransactService.create(data)

