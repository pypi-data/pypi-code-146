from modern_treasury.objects.reference_number import ReferenceNumber
from .routing_details import RoutingDetailsResponse


class PaymentOrderResponse:
    def __init__(self, json):
        self.json = json

    @property
    def id(self):
        return self.json.get('id')

    @property
    def type(self):
        return self.json.get('type')

    @property
    def fallback_type(self):
        return self.json.get('fallback_type')

    @property
    def subtype(self):
        return self.json.get('subtype')

    @property
    def amount(self):
        return self.json.get('amount')

    @property
    def direction(self):
        return self.json.get('direction')

    @property
    def originating_account_id(self):
        return self.json.get('originating_account_id')

    @property
    def receiving_account_id(self):
        return self.json.get('receiving_account_id')

    @property
    def receiving_account(self):
        return self.json.get('receiving_account')

    @property
    def account_type(self):
        return self.json.get('account_type')

    @property
    def party_name(self):
        return self.json.get('party_name')

    @property
    def party_type(self):
        return self.json.get('party_type')

    @property
    def party_address(self):
        return self.json.get('party_address')

    @property
    def account_details(self):
        return self.json.get('account_details')

    @property
    def plaid_processor_token(self):
        return self.json.get('plaid_processor_token')

    @property
    def routing_details(self):
        result = self.json.get('routing_details')
        if result:
            return [RoutingDetailsResponse(routing_detail) for routing_detail in result ]
        return []

    @property
    def accounting_category_id(self):
        return self.json.get('accounting_category_id')

    @property
    def accounting_ledger_class_id(self):
        return self.json.get('accounting_ledger_class_id')

    @property
    def currency(self):
        return self.json.get('currency')

    @property
    def effective_date(self):
        return self.json.get('effective_date')

    @property
    def priority(self):
        return self.json.get('priority')

    @property
    def description(self):
        return self.json.get('description')

    @property
    def statement_descriptor(self):
        return self.json.get('statement_descriptor')

    @property
    def remittance_information(self):
        return self.json.get('remittance_information')

    @property
    def purpose(self):
        return self.json.get('purpose')

    @property
    def line_items(self):
        return self.json.get('line_items')

    @property
    def metadata(self):
        return self.json.get('metadata')

    @property
    def charge_bearer(self):
        return self.json.get('charge_bearer')

    @property
    def foreign_exchange_indicator(self):
        return self.json.get('foreign_exchange_indicator')

    @property
    def foreign_exchange_contract(self):
        return self.json.get('foreign_exchange_contract')

    @property
    def nsf_protected(self):
        return self.json.get('nsf_protected')

    @property
    def originating_party_name(self):
        return self.json.get('originating_party_name')

    @property
    def ultimate_originating_party_name(self):
        return self.json.get('ultimate_originating_party_name')

    @property
    def ultimate_originating_party_identifier(self):
        return self.json.get('ultimate_originating_party_identifier')

    @property
    def reference_numbers(self) -> ReferenceNumber:
        return [ReferenceNumber.create(ref_number)  for ref_number in self.json.get("reference_numbers", [])]