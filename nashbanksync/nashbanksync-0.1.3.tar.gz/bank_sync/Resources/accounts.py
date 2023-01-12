from bank_sync.Resources.resource import Resource
from bank_sync.APIs.utils.generate_code import get_code
from datetime import datetime
from datetime import date
import json
try:
    from django.conf import settings
except Exception as e:
    pass

import logging
logger = logging.getLogger(__name__)


class Accounts(Resource):

    urls = {}
    bank_sync_call_back = {}

    try:
        bank_sync_call_back = getattr(
            settings, 'BANK_SYNC_CALL_BACK_URLS', bank_sync_call_back)
    except Exception as e:
        pass

    def set_bank_id(self, bank_id):
        # This is done to help with URL standardization in the operations and resource classes
        super().set_action(action='accounts')
        return super().set_bank_id(bank_id)

    def forex_rate(self, payload=None):

        return super().read(payload=payload)

    def balance(self, payload=None):

        return super().read(payload=payload)

    def mini_statement(self, payload=None):

        return super().read(payload=payload)

    def full_statement(self, payload=None):

        return super().read(payload=payload)

    def account_validation(self, payload=None):

        return super().read(payload=payload)

    def account_transactions(self, payload=None):

        return super().read(payload=payload)

    def pdf_to_json(self, payload=None):
        self.register_callback()
        return super().read(payload=payload)

    def get_pdf_json(self, payload=None):

        return super().read(payload=payload)

    def serialize(self, payload=None, operation=None):
        # Set the Operation being executed
        # Set the Original request sent before serialization
        super().set_operation(operation).set_request(payload)
        data = {}

        if operation in [super().PDF_TO_JSON]:
            data.update({
                "bank_id": super().get_bank_id(),
                "type": super().get_operation(),
                "bank_sync_call_back": self.bank_sync_call_back.get("payments", ""),
            })

        if operation is None:
            return "Specify the operation: Resource.BALANCE, Resource.MINI_STATEMENT, Resource.FULL_STATEMENT, Resource.ACCOUNT_VALIDATION or Resource.ACCOUNT_TRANSACTIONS"

        if operation == super().BALANCE or operation == super().MINI_STATEMENT or operation == super().ACCOUNT_VALIDATION:

            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                data.update({
                    "MessageReference": f'{get_code(length=14)}',
                    "AccountNumber": f'{payload.get("account_number", "")}'
                })
            # If bank_id is EQUITY
            elif super().get_bank_id() == super().EQUITY:
                data.update({
                    "country_code": payload.get("country_code", ""),
                    "account_number": payload.get("account_number", "")
                })
            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:
                pass
            # If bank_id is UBA
            elif super().get_bank_id() == super().UBA:
                data.update({
                    "PROCESSING_CODE": 31,
                    "COUNTRY_CODE": payload.get("country_code", ""),
                    "DR_ACCT_NUM": payload.get("account_number", "")
                })
            # If bank_id is DTB
            elif super().get_bank_id() == super().DTB:
                if operation == super().ACCOUNT_VALIDATION:
                    data.update({
                        "account_number": payload.get("account_number", "")
                    })
            # If bank_id is THIRD_PARTY_BANKING
            elif super().get_bank_id() in super().THIRD_PARTY_BANKING.keys():
                data.update({
                    "businessCode": payload.get("business_code", ""),
                    "accountIds": [payload.get("account_number", "")]
                })

        elif operation == super().FULL_STATEMENT:
            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                data.update({
                    "MessageReference": f'{get_code(length=14)}'
                })
                data.update({
                    "AccountNumber": f'{payload.get("account_number", "")}'
                })
                data.update({
                    "StartDate": payload.get("start_date", "")
                })
                data.update({
                    "EndDate": payload.get("end_date", "")
                })
            # If bank_id is EQUITY
            elif super().get_bank_id() == super().EQUITY:
                data.update({
                    "country_code": payload.get("country_code", "")
                })
                data.update({
                    "account_number": f'{payload.get("account_number", "")}'
                })
                data.update({
                    "start_date": payload.get("start_date", "")
                })
                data.update({
                    "end_date": payload.get("end_date", "")
                })
                data.update({
                    "limit": payload.get("limit", 3)
                })
            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:
                pass
            # If bank_id is UBA
            elif super().get_bank_id() == super().UBA:
                data.update({
                    "PROCESSING_CODE": 93,
                    "COUNTRY_CODE": payload.get("country_code", ""),
                    "DR_ACCT_NUM": payload.get("account_number", ""),
                    "TRAN_CRNCY_CODE": payload.get("currency_code", ""),
                    "STMT_QUERY_PARAMS": {
                        "START_DATE": payload.get("start_date", date.today().strftime('%Y%m%d')).replace("-", ""),
                        "END_DATE": payload.get("end_date", date.today().strftime('%Y%m%d')).replace("-", ""),
                        "NUM_TRANS": payload.get("limit", 5)
                    }
                })

        elif operation == super().ACCOUNT_TRANSACTIONS:
            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                data.update({
                    "MessageReference": f'{get_code(length=14)}',
                    "AccountNumber": f'{payload.get("account_number", "")}',
                    "NoOfTransactions": f'{payload.get("limit", 1)}'
                })
            # If bank_id is EQUITY
            elif super().get_bank_id() == super().EQUITY:
                pass

            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:
                pass
            # If bank_id is THIRD_PARTY_BANKING
            elif super().get_bank_id() in super().THIRD_PARTY_BANKING.keys():
                data.update({
                    "businessCode": payload.get("business_code", ""),
                    "narration": payload.get("narration", ""),
                    "type": payload.get("type", ""),
                    "paginate": payload.get("paginate", True),
                    "startDate": payload.get("start_date", ""),
                    "endDate": payload.get("end_date", ""),
                    "limit": payload.get("limit", 1),
                    "total": payload.get("total", 0),
                    "offset": payload.get("offset", 0),
                    "accountIds": [payload.get("account_number", "")],

                })

        elif operation == super().PDF_TO_JSON or operation == super().GET_JSON_PDF:
            # data = payload
            data.update(payload)
            if payload.get("callback_url", None) is None or payload.get("callback_url", '') == '':
                data['bank_sync_call_back'] = payload.get("callback_url", None)

        elif operation == super().FOREX_RATE:
            if super().get_bank_id() == super().EQUITY:
                data.update({
                    "accountNumber": payload.get("account_number", ""),
                    "countryCode": payload.get("country_code", ""),
                    "currencyCode": payload.get("currency_code", ""),
                    "toCurrency": payload.get("to_currency", ""),
                    "amount": round(float(payload.get("amount", 0)), 2),
                })

        data.update(payload.get("additional_properties", {}))

        return data

    def response(self):

        data = {}

        response_data = super().response()

        if super().get_operation() == super().BALANCE:

            if super().get_bank_id() == super().COOP:

                data["message"] = response_data.get("MessageDescription", "")
                data["code"] = response_data.get("MessageCode", "-111111")
                data["balance"] = response_data.get("AvailableBalance", "")
                data["account_type"] = response_data.get("ProductName", "")
                data["cleared_balance"] = response_data.get("ClearedBalance", "")
                data["booked_balance"] = response_data.get("BookedBalance", "")
                data["blocked_balance"] = response_data.get("BlockedBalance", "")
                data["arrears_amount"] = response_data.get("ArrearsAmount", "")
                data["branch_name"] = response_data.get("BranchName", "")
                data["branch_code"] = response_data.get("BranchSortCode", "")
                data["average_balance"] = response_data.get("AverageBalance", "")
                data["uncleared_balance"] = response_data.get("UnclearedBalance", "")
                data["over_draft_limit"] = response_data.get("ODLimit", "")
                data["credit_limit"] = response_data.get("CreditLimit", "")

            elif super().get_bank_id() == super().EQUITY:

                data["message"] = response_data.get("message", "")
                data["code"] = response_data.get("code", -111111)
                data["balance"] = 0

                balances=response_data.get("data", {}).get("balances", [])
                if bool(balances):
                    if balances[0].get('type','')=='Available':
                        data["balance"] = balances[0].get("amount", -1)
                    if balances[1].get('type','')=='Current':
                        data["cleared_balance"] = balances[1].get("amount", -1)

                data["account_type"] = response_data.get("ProductName", "")
                # data["cleared_balance"] = response_data.get("ClearedBalance", "")
                data["booked_balance"] = response_data.get("BookedBalance", "")
                data["blocked_balance"] = response_data.get("BlockedBalance", "")
                data["arrears_amount"] = response_data.get("ArrearsAmount", "")
                data["branch_name"] = response_data.get("BranchName", "HQ")
                data["branch_code"] = response_data.get("BranchSortCode", "")
                data["average_balance"] = response_data.get("AverageBalance", "")
                data["uncleared_balance"] = response_data.get("UnclearedBalance", "")
                data["over_draft_limit"] = response_data.get("ODLimit", "")
                data["credit_limit"] = response_data.get("CreditLimit", "")
            # If bank_id is UBA
            elif super().get_bank_id() == super().UBA:

                data["message"] = ''
                data["code"] = int(float(response_data.get("sendTransactionResponse", {}).get(
                    "return", {}).get("C24TRANRES", {}).get("ACTION_CODE", "-111111")))
                data["balance"] = float(response_data.get("sendTransactionResponse", {}).get(
                    "return", {}).get("C24TRANRES", {}).get("AVAILABLE_BALANCE", -1))
                if data["code"]:
                    data["message"] = "Transaction Failed"
                else:
                    data["message"] = "Success"

        elif super().get_operation() == super().MINI_STATEMENT or super().get_operation() == super().ACCOUNT_TRANSACTIONS:

            if super().get_bank_id() == super().COOP:

                data["message"] = response_data.get("MessageDescription", "")
                data["code"] = response_data.get("MessageCode", "-111111")
                data["transactions"] = []

                transactions = response_data.get("Transactions", [])

                for i in range(len(transactions)):
                    transaction = {
                        "currency_code": "KES",
                        "date": transactions[i].get("TransactionDate", ""),
                        "description": transactions[i].get("Narration", ""),
                        "reference": transactions[i].get("TransactionReference", "")
                    }

                    if transactions[i].get("TransactionType", "") == "D":
                        transaction["amount"] = transactions[i].get(
                            "DebitAmount", "")
                        transaction["type"] = "Debit"

                    elif transactions[i].get("TransactionType", "") == "C":
                        transaction["amount"] = transactions[i].get(
                            "CreditAmount", "")
                        transaction["type"] = "Credit"

                    data["transactions"].append(transaction)

            if super().get_operation() == super().MINI_STATEMENT:

                if super().get_bank_id() == super().EQUITY:

                    data["message"] = response_data.get("message", "")
                    data["code"] = f'{response_data.get("code", -111111)}'
                    data["transactions"] = []

                    transactions = response_data.get(
                        "data", {}).get("transactions", [])

                    for i in range(len(transactions)):

                        transaction = {
                            "currency_code": response_data.get("data", {}).get("currency", "KES"),
                            "date": datetime.fromisoformat(
                                transactions[i].get(
                                    "postedDateTime", "") + '+00:00'
                            ).strftime('%Y-%m-%d %H:%M:%S'),
                            "description": transactions[i].get("description", ""),
                            "amount":  transactions[i].get("amount", ""),
                            "type":  transactions[i].get("type", "")
                        }

                        data["transactions"].append(transaction)

        elif super().get_operation() == super().ACCOUNT_VALIDATION:

            if super().get_bank_id() == super().COOP:

                data["message"] = response_data.get("MessageDescription", "")
                data["code"] = response_data.get("MessageCode", "-111111")
                data["account_name"] = ""

            elif super().get_bank_id() == super().EQUITY:

                data["message"] = response_data.get("message", "")
                data["code"] = f'{response_data.get("code", -111111)}'
                data["account_name"] = ""
                customer = response_data.get("data", {}).get("customer", [])
                if len(customer) > 0:
                    data["account_name"] = customer[0].get("name", "")

            # If bank_id is DTB
            elif super().get_bank_id() == super().DTB:
                if isinstance(response_data, list):
                    data["message"] = response_data[0]
                    data["code"] = -111111
                    data["account_name"] = ""
                else:
                    data["message"] = response_data.get(
                        "content", {}).get("account_description", "")
                    data["code"] = 0
                    data["account_name"] = response_data.get(
                        "content", {}).get("customer_name", "")

        elif super().get_operation() == super().FULL_STATEMENT:

            if super().get_bank_id() == super().COOP:

                data["message"] = response_data.get("MessageDescription", "")
                data["code"] = response_data.get("MessageCode", "-111111")
                data["transactions"] = []

                transactions = response_data.get("Transactions", [])

                for i in range(len(transactions)):
                    transaction = {
                        "currency_code": "KES",
                        "date": transactions[i].get("TransactionDate", ""),
                        "description": transactions[i].get("Narration", ""),
                    }

                    if transactions[i].get("TransactionType", "") == "D":
                        transaction["amount"] = transactions[i].get(
                            "DebitAmount", "")
                        transaction["type"] = "Debit"

                    elif transactions[i].get("TransactionType", "") == "C":
                        transaction["amount"] = transactions[i].get(
                            "CreditAmount", "")
                        transaction["type"] = "Credit"

                    transaction["reference"] = transactions[i].get(
                        "TransactionReference", "")
                    transaction["running_balance"] = transactions[i].get(
                        "RunningClearedBalance", "")

                    data["transactions"].append(transaction)

            elif super().get_bank_id() == super().EQUITY:

                try:
                    if isinstance(response_data, str):
                        response_data = '{}{}'.format(response_data, '"}]}}')
                        response_data = json.loads(response_data)
                except Exception as e:
                    data['error'] = e

                if isinstance(response_data, dict):
                    data["message"] = response_data.get("message", "")
                    data["code"] = f'{response_data.get("code", -111111)}'
                    data["transactions"] = []

                    transactions = response_data.get(
                        "data", {}).get("transactions", [])

                    for i in range(len(transactions)):

                        transaction = {
                            "currency_code": response_data.get("data", {}).get("currency", "KES"),
                            "date": datetime.fromisoformat(
                                transactions[i].get(
                                    "postedDateTime", "") + '+00:00'
                            ).strftime('%Y-%m-%d %H:%M:%S'),
                            "description": transactions[i].get("description", ""),
                            "amount":  f'{transactions[i].get("amount", "")}',
                            "type":  transactions[i].get("type", ""),
                            "reference":  transactions[i].get("reference", ""),
                            "running_balance":  f'{transactions[i].get("runningBalance", {}).get("amount", "")}'
                        }

                        data["transactions"].append(transaction)
                else:
                    data['response'] = response_data

            # If bank_id is UBA
            elif super().get_bank_id() == super().UBA:

                data["message"] = ''
                data["code"] = int(float(response_data.get("sendTransactionResponse", {}).get(
                    "return", {}).get("C24TRANRES", {}).get("ACTION_CODE", "-111111")))
                if data["code"]:
                    data["message"] = "Transaction Failed"
                else:
                    data["message"] = "Success"
                data["transactions"] = []

                transactions = response_data.get("sendTransactionResponse", {}).get("return", {}).get(
                    "C24TRANRES", {}).get("TRANS_INFO", {}).get("TRAN", {}).get("element", [])

                for i in range(len(transactions)):
                    transaction = {
                        "date": datetime.strptime(f'{transactions[i].get("DATE_POSTED", None)}', '%Y%d%m%H%M%S').strftime('%Y-%m-%d %H:%M:%S'),
                        "description": transactions[i].get("NARRATION", ""),
                        "amount": transactions[i].get("TRAN_AMT", -1),
                        "reference": transactions[i].get("TRAN_ID", ""),
                        "running_balance": transactions[i].get("BALANCE", -1),
                    }

                    if transactions[i].get("PART_TRAN_TYPE", "") == "D":
                        transaction["type"] = "Debit"
                    elif transactions[i].get("PART_TRAN_TYPE", "") == "C":
                        transaction["type"] = "Credit"

                    data["transactions"].append(transaction)

        elif super().get_operation() == super().PDF_TO_JSON or super().get_operation() == super().GET_JSON_PDF:
            data = self.standardize_pdf_to_json(response_data=response_data)

        elif super().get_operation() == super().FOREX_RATE:

            if isinstance(response_data, dict):
                data["message"] = response_data.get("message", "")
                data["code"] = f'{response_data.get("code", -111111)}'

                if 'data' in response_data.keys():
                    data['data'] = {
                        "converted_amount": response_data.get('data', {}).get("convertedAmount", -1),
                        "rate": response_data.get('data', {}).get("rate", -1),
                        "from_amount": response_data.get('data', {}).get("fromAmount", -1),
                        "rate_code": response_data.get('data', {}).get("rateCode", "")
                    }

            else:
                data['response'] = response_data

        elif super().get_operation() == super().JOBS_ACCOUNT_BALANCES:
            data = []
            if super().get_bank_id() == super().COOP:
                for account_balance_data in response_data.get('data', []):
                    data.append({
                        "status": account_balance_data.get("status", -1),
                        "created_at": account_balance_data.get("created_at", ''),
                        "available_balance": account_balance_data.get('account_balance_response', {}).get("AvailableBalance", ''),
                    })

                    if account_balance_data.get("status", -1) != 0:
                        data["available_balance_error"] = account_balance_data.get(
                            'account_balance_response', {})

        elif super().get_operation() == super().JOBS_ACCOUNT_STATEMENT:
            data = []
            if super().get_bank_id() == super().COOP:

                for account_statement_data in response_data.get('data', []):
                    data.append({
                        "status": account_statement_data.get("status", -1),
                        "created_at": account_statement_data.get("created_at", ''),
                        "transactions": [],
                    })

                    if account_statement_data.get("status", -1) != 0:
                        data[-1]["transaction_error"] = account_statement_data.get(
                            'account_statement_response', {})

                    else:
                        transactions_data = account_statement_data.get(
                            'account_statement_response', {}).get("Transactions", [])
                        for transaction in transactions_data:
                            transaction_data = {
                                "date": transaction.get("TransactionDate", ''),
                                "description": transaction.get("Narration", ''),
                                "reference": transaction.get("TransactionReference", ''),
                            }

                            if transaction.get("TransactionType", "") == "D":
                                transaction_data["amount"] = transaction.get(
                                    "DebitAmount", "")
                                transaction_data["type"] = "Debit"

                            elif transaction.get("TransactionType", "") == "C":
                                transaction_data["amount"] = transaction.get(
                                    "CreditAmount", "")
                                transaction_data["type"] = "Credit"

                            data[-1].get("transactions", []
                                         ).append(transaction_data)

        if bool(data):
            if isinstance(data, dict):
                if 'transactions' in data.keys() and 'code' in data.keys():
                    if len(data["transactions"]) == 0 and int(data["code"]) == -111111:
                        data['error'] = response_data
            return data
        if super().get_bank_id() in super().THIRD_PARTY_BANKING.keys():
            return response_data

        return response_data
