from dataclasses import dataclass
from typing import List
from etsy_apiv3.utils import EtsySession, Response
from etsy_apiv3.models import Payment, PaymentAccountLedgerEntry

@dataclass
class PaymentResource:
    
    session: EtsySession
    
    def get_shop_payments(self, shop_id: int, payment_ids: List[int]) -> Response[Payment]:
        endpoint = f"shops/{shop_id}/payments"
        params = {
            "payment_ids": payment_ids
        }
        response = self.session.request(endpoint, params=params)
        return Response[Payment](**response)
    
    def get_payment_by_receipt_id(self, shop_id: int, receipt_id: int) -> Payment:
        endpoint = f"shops/{shop_id}/receipts/{receipt_id}/payments"
        response = self.session.request(endpoint)
        return Payment(**response)
    
    def get_payment_by_account_ledger_entry_ids(self, shop_id: int, ledger_entry_ids: List[int]) -> Response[Payment]:
        endpoint = f"shops/{shop_id}/payment-account/ledger-entries/payments"
        params = {
            "ledger_entry_ids": ledger_entry_ids
        }
        response = self.session.request(endpoint, params=params)
        return Response[Payment](**response)
    
    def get_shop_payment_account_ledger_entry(self, shop_id: int, ledger_entry_id: int) -> PaymentAccountLedgerEntry:
        endpoint = f"shops/{shop_id}/payment-account/ledger-entries/{ledger_entry_id}"
        response = self.session.request(endpoint)
        return PaymentAccountLedgerEntry(**response)
    
    def get_shop_payment_account_ledger_entries(self, shop_id: int, min_created: int, max_created: int, limit: int = 25, offset: int = 0) -> Response[PaymentAccountLedgerEntry]:
        endpoint = f"shops/{shop_id}/payment-account/ledger-entries"
        response = self.session.request(endpoint)
        return Response[PaymentAccountLedgerEntry](**response)
    
    
    