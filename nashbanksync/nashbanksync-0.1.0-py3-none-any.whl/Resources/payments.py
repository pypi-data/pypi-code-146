from bank_sync.Resources.resource import Resource
from bank_sync.APIs.utils.generate_code import get_code
from datetime import date, datetime
try:
    from django.conf import settings
except Exception as e:
    pass


class Payments(Resource):

    urls = {}
    bank_sync_call_back = {}

    try:
        bank_sync_call_back = getattr(
            settings, 'BANK_SYNC_CALL_BACK_URLS', bank_sync_call_back)
    except Exception as e:
        pass

    def set_bank_id(self, bank_id):
        # This is done to help with URL standardization in the operations and resource classes
        super().set_action(action='payment')
        return super().set_bank_id(bank_id)

    def ift(self, payload=None):
        self.register_callback()
        return super().read(payload=payload)

    def eft(self, payload=None):
        self.register_callback()
        return super().read(payload=payload)

    def rtgs(self, payload=None):
        self.register_callback()
        return super().read(payload=payload)

    def swift(self, payload=None):
        self.register_callback()
        return super().read(payload=payload)

    def transaction_status(self, payload=None):

        return super().read(payload=payload)

    def mobile_wallet(self, payload=None):
        self.register_callback()
        return super().read(payload=payload)

    def pesalink_to_bank(self, payload=None):
        self.register_callback()
        return super().read(payload=payload)

    def pesalink_to_mobile(self, payload=None):
        self.register_callback()
        return super().read(payload=payload)

    # API Endpoint used by third party integrations
    def initiate_payment(self, payload=None):

        return super().read(payload=payload)

    def serialize(self, payload=None, operation=None):
        # Set the Operation being executed
        # Set the Original request sent before serialization
        super().set_operation(operation).set_request(payload)

        data = {}

        default_reference = payload.get("transfer", {}).get(
            "reference", get_code(length=14))

        if operation is None:
            return "Specify the operation: Resource.BALANCE, Resource.MINI_STATEMENT, Resource.FULL_STATEMENT, Resource.ACCOUNT_VALIDATION or Resource.ACCOUNT_TRANSACTIONS"

        if operation == super().IFT:

            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                data.update({
                    "MessageReference": f'{default_reference}'
                })
                data.update({
                    "CallBackUrl": self.bank_sync_call_back.get("payments", "")
                })
                data.update({
                    "Source": {
                        "AccountNumber": payload.get("source", {}).get("account_number", None),
                        "Amount": payload.get("source", {}).get("amount", None),
                        "TransactionCurrency": payload.get("transfer", {}).get("currency_code", None),
                        "Narration": payload.get("transfer", {}).get("description", "")
                    }
                })

                destinations = payload.get("destinations", [])

                for i in range(len(destinations)):
                    if i == 0:
                        data.update({
                            "Destinations": []
                        })

                    data["Destinations"].append(
                        {
                            "ReferenceNumber": f'{default_reference}_1',
                            "AccountNumber": destinations[i].get("account_number", None),
                            "BankCode": payload.get("transfer", {}).get("bank_code", None),
                            "BranchCode": payload.get("transfer", {}).get("branch_code", None),
                            "Amount": destinations[i].get("amount", None),
                            "TransactionCurrency": payload.get("transfer", {}).get("currency_code", None),
                            "Narration": payload.get("transfer", {}).get("description", "")
                        }
                    )
            # If bank_id is EQUITY
            elif super().get_bank_id() == super().EQUITY:
                data.update({
                    "source": {
                        "countryCode": payload.get("source", {}).get("country_code", None),
                        "name": payload.get("source", {}).get("name", None),
                        "accountNumber": payload.get("source", {}).get("account_number", None)
                    }
                })

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "destination": {
                            "type": "bank",
                            "countryCode": destination.get("country_code", None),
                            "name": destination.get("name", None),
                            "accountNumber": destination.get("account_number", None),
                        }
                    })

                    data.update({
                        "transfer": {
                            "type": "InternalFundsTransfer",
                            "amount": f'{destination.get("amount",None)}',
                            "currencyCode": payload.get("transfer", {}).get("currency_code", None),
                            "reference": payload.get("transfer", {}).get("reference", None),
                            "date": payload.get("transfer", {}).get("date", None),
                            "description": payload.get("transfer", {}).get("description", ""),
                        }
                    })
            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "BankCode": payload.get("transfer", {}).get("bank_code", None),
                        "BankSwiftCode": payload.get("transfer", {}).get("bank_swift_code", None),
                        "BranchCode": payload.get("transfer", {}).get("branch_code", None),
                        "BeneficiaryAccountName": payload.get("destination", {}).get("name", None),
                        "Country": payload.get("transfer", {}).get("country", None),
                        "Reference": f'{default_reference}',
                        "Currency": payload.get("transfer", {}).get("currency_code", None),
                        "Account": destination.get("account_number", None),
                        "Amount": destination.get("amount", None),
                        "Narration": payload.get("transfer", {}).get("description", None),
                        "Transaction Date": payload.get("transfer", {}).get("date", date.today().strftime('%Y%m%d')).replace("-", ""),
                    })
            # If bank_id is DTB
            elif super().get_bank_id() == super().DTB:
                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]
                    data.update({
                        "identifier": {
                            "xref": f'API-{payload.get("transfer", {}).get("reference", get_code())}',
                            "channel": "API",
                            "bank_code": payload.get("transfer", {}).get("bank_code", ""),
                        },
                        "content": {
                            "source_reference": payload.get("transfer", {}).get("reference", get_code()),
                            "product": "FTIN",
                            "transaction_branch": payload.get("transfer", {}).get("branch_code", ""),
                            "debit_party": payload.get("source", {}).get("account_number", ""),
                            "credit_party": destination.get("account_number", ""),
                            "debit_currency": payload.get("transfer", {}).get("currency_code", ""),
                            "credit_currency": payload.get("transfer", {}).get("currency_code", ""),
                            "exchange_rate": 1,
                            "transaction_amount": destination.get("amount", 0),
                            "transaction_date": payload.get("transfer", {}).get("date", ""),
                            "value_date": payload.get("transfer", {}).get("date", ""),
                            "narration": payload.get("transfer", {}).get("description", ""),
                            "udf": [
                                {
                                    "field_name": "ACUMEN_CODE",
                                    "field_value": "NONE"
                                }
                            ]
                        }
                    })
            # If bank_id is UBA
            elif super().get_bank_id() == super().UBA:
                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]
                    data.update({
                        "STAN": f"{datetime.now().strftime('%Y%m%d%H%M')}",
                        "TRAN_DATE_TIME": f"{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "TRAN_AMT": f'{destination.get("amount",0)}',
                        "PROCESSING_CODE": "50",
                        "TRAN_CRNCY_CODE": payload.get("transfer", {}).get("currency_code", ""),
                        "COUNTRY_CODE": destination.get("country_code", ""),
                        "VALUE_DATE": payload.get("transfer", {}).get("date", date.today().strftime('%Y%m%d')).replace("-", ""),
                        "DR_ACCT_NUM": payload.get("source", {}).get("account_number", ""),
                        "CR_ACCT_NUM": destination.get("account_number", ""),
                        "RESERVED_FLD_1": "DECLARATION DES FRAIS D IMPRESSION 3 PAGES @ 17% VAT",
                        "FEE": {
                            "ID": "1",
                            "DR_ACCT_NO": payload.get("source", {}).get("account_number", ""),
                            "CR_ACCT_NO": destination.get("account_number", ""),
                            "AMOUNT": payload.get("transfer", {}).get("transaction_fees", ""),
                        }
                    })
        elif operation == super().MOBILE_WALLET:

            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                data.update({
                    "MessageReference": f'{default_reference}'
                })
                data.update({
                    "CallBackUrl": self.bank_sync_call_back.get("payments", "")
                })
                data.update({
                    "Source": {
                        "AccountNumber": f'{payload.get("source", {}).get("account_number", None)}',
                        "Amount": payload.get("source", {}).get("amount", None),
                        "TransactionCurrency": payload.get("transfer", {}).get("currency_code", None),
                        "Narration": payload.get("transfer", {}).get("description", "")
                    }
                })

                destinations = payload.get("destinations", [])

                for i in range(len(destinations)):
                    if i == 0:
                        data.update({
                            "Destinations": []
                        })

                    data["Destinations"].append(
                        {
                            "ReferenceNumber": f'{default_reference}_1',
                            "MobileNumber": f'{destinations[i].get("mobile_number",None)}',
                            "Amount": destinations[i].get("amount", None),
                            "Narration": payload.get("transfer", {}).get("description", "")
                        }
                    )
            # If bank_id is EQUITY
            elif super().get_bank_id() == super().EQUITY:
                data.update({
                    "source": {
                        "countryCode": payload.get("source", {}).get("country_code", None),
                        "name": payload.get("source", {}).get("name", None),
                        "accountNumber": payload.get("source", {}).get("account_number", None)
                    }
                })

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "destination": {
                            "type": "mobile",
                            "countryCode": destination.get("country_code", None),
                            "name": destination.get("name", None),
                            "mobileNumber": destination.get("mobile_number", None),
                            "walletName": destination.get("wallet_name", None),
                        }
                    })

                    data.update({
                        "transfer": {
                            "type": "MobileWallet",
                            "amount": f'{destination.get("amount",None)}',
                            "currencyCode": payload.get("transfer", {}).get("currency_code", None),
                            "reference": payload.get("transfer", {}).get("reference", None),
                            "date": payload.get("transfer", {}).get("date", None),
                            "description": payload.get("transfer", {}).get("description", ""),
                            "callbackUrl": self.bank_sync_call_back.get("payments", ""),
                        }
                    })
            # If bank_id is DTB
            elif super().get_bank_id() == super().DTB:
                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "operator": destination.get("wallet_name", ""),
                        "identifier": {
                            "xref": f'API-{payload.get("transfer", {}).get("reference", get_code())}',
                            "channel": "API",
                            "bank_code": payload.get("transfer", {}).get("bank_code", ""),
                        },
                        "content": {
                            "cbs_reference": payload.get("transfer", {}).get("ift_reference", ""),
                            "transaction_amount": int(float(destination.get("amount", 0))),
                            "credit_party": payload.get("source", {}).get("account_number", ""),
                            "customer_msisdn": destination.get("mobile_number", ""),
                            "customer_name": destination.get("name", ""),
                            "account_reference": payload.get("transfer", {}).get("reference", ""),
                            "invoice_number": payload.get("transfer", {}).get("invoice_id", ""),
                            "narration": payload.get("transfer", {}).get("description", ""),
                            "transaction_type": payload.get("transfer", {}).get("type", ""),
                        }
                    })

            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "BankCode": payload.get("transfer", {}).get("bank_code", None),
                        "BankSwiftCode": payload.get("transfer", {}).get("bank_swift_code", None),
                        "BranchCode": payload.get("transfer", {}).get("branch_code", None),
                        "BeneficiaryAccountName": destination.get("name", None),
                        "Country": payload.get("transfer", {}).get("country", None),
                        "TranType": "Mpesa",
                        "Reference": f'{default_reference}',
                        "Currency": payload.get("transfer", {}).get("currency_code", None),
                        "Account": destination.get("mobile_number", None),
                        "Amount": destination.get("amount", None),
                        "Narration": payload.get("transfer", {}).get("description", None),
                        "Transaction Date": payload.get("transfer", {}).get("date", date.today().strftime('%Y%m%d')).replace("-", ""),
                        "Validation ID": f'{default_reference}',
                    })
        elif operation == super().RTGS:

            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                pass
            elif super().get_bank_id() == super().EQUITY:
                data.update({
                    "source": {
                        "countryCode": payload.get("source", {}).get("country_code", None),
                        "name": payload.get("source", {}).get("name", None),
                        "accountNumber": payload.get("source", {}).get("account_number", None),
                        "currency": payload.get("transfer", {}).get("currency_code", None),
                    }
                })

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "destination": {
                            "type": "bank",
                            "countryCode": destination.get("country_code", None),
                            "name": destination.get("name", None),
                            "bankCode": payload.get("transfer", {}).get("bank_code", None),
                            "accountNumber": f'{destination.get("account_number",None)}',
                        }
                    })

                    data.update({
                        "transfer": {
                            "type": "RTGS",
                            "amount": f'{destination.get("amount",None)}',
                            "currencyCode": payload.get("transfer", {}).get("currency_code", None),
                            "reference": payload.get("transfer", {}).get("reference", None),
                            "date": payload.get("transfer", {}).get("date", None),
                            "description": payload.get("transfer", {}).get("description", ""),
                        }
                    })
            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "BankCode": payload.get("transfer", {}).get("bank_code", None),
                        "BankSwiftCode": payload.get("transfer", {}).get("bank_swift_code", None),
                        "BranchCode": payload.get("transfer", {}).get("branch_code", None),
                        "BeneficiaryAccountName": destination.get("name", None),
                        "Country": payload.get("transfer", {}).get("country", None),
                        "TranType": "RTGS",
                        "Reference": f'{default_reference}',
                        "Currency": payload.get("transfer", {}).get("currency_code", None),
                        "Account": destination.get("account_number", None),
                        "Amount": destination.get("amount", None),
                        "Narration": payload.get("transfer", {}).get("description", None),
                        "Transaction Date": payload.get("transfer", {}).get("date", date.today().strftime('%Y%m%d')).replace("-", ""),
                    })
        elif operation == super().SWIFT:

            # If bank_id is COOP
            if super().get_bank_id() == super().EQUITY:
                data.update({
                    "source": {
                        "countryCode": payload.get("source", {}).get("country_code", None),
                        "name": payload.get("source", {}).get("name", None),
                        "accountNumber": payload.get("source", {}).get("account_number", None),
                        "sourceCurrency": payload.get("source", {}).get("currency_code", None),
                    }
                })

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "destination": {
                            "type": "bank",
                            "countryCode": destination.get("country_code", None),
                            "name": destination.get("name", None),
                            "bankBic": destination.get("bank_bic", None),
                            "accountNumber": f'{destination.get("account_number",None)}',
                            "addressline1": f'{destination.get("address",None)}',
                            "currency": destination.get("currency_code", None),
                        }
                    })

                    data.update({
                        "transfer": {
                            "type": "SWIFT",
                            "amount": f'{destination.get("amount",None)}',
                            "currencyCode": payload.get("transfer", {}).get("currency_code", None),
                            "reference": payload.get("transfer", {}).get("reference", None),
                            "date": payload.get("transfer", {}).get("date", None),
                            "description": payload.get("transfer", {}).get("description", ""),
                            "chargeOption": "SELF"
                        }
                    })
        elif operation == super().EFT:

            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                pass
            elif super().get_bank_id() == super().EQUITY:
                pass
            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "BankCode": payload.get("transfer", {}).get("bank_code", None),
                        "BankSwiftCode": payload.get("transfer", {}).get("bank_swift_code", None),
                        "BranchCode": payload.get("transfer", {}).get("branch_code", None),
                        "BeneficiaryAccountName": destination.get("name", None),
                        "BeneficiaryName": destination.get("name", None),
                        "Country": payload.get("transfer", {}).get("country", None),
                        "Reference": f'{default_reference}',
                        "Currency": payload.get("transfer", {}).get("currency_code", None),
                        "Account": destination.get("account_number", None),
                        "Amount": f'{destination.get("amount", None)}',
                        "Narration": payload.get("transfer", {}).get("description", None),
                        "Transaction Date": payload.get("transfer", {}).get("date", date.today().strftime('%Y%m%d')).replace("-", ""),
                    })
        elif operation == super().PESALINK_TO_BANK:

            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                data.update({
                    "MessageReference": f'{default_reference}'
                })
                data.update({
                    "CallBackUrl": self.bank_sync_call_back.get("payments", "")
                })
                data.update({
                    "Source": {
                        "AccountNumber": payload.get("source", {}).get("account_number", None),
                        "Amount": payload.get("source", {}).get("amount", None),
                        "TransactionCurrency": payload.get("transfer", {}).get("currency_code", None),
                        "Narration": payload.get("transfer", {}).get("description", "")
                    }
                })

                destinations = payload.get("destinations", [])

                for i in range(len(destinations)):
                    if i == 0:
                        data.update({
                            "Destinations": []
                        })

                    data["Destinations"].append(
                        {
                            "ReferenceNumber": f'{default_reference}_1',
                            "AccountNumber": destinations[i].get("account_number", None),
                            "BankCode": payload.get("transfer", {}).get("bank_code", None),
                            "Amount": destinations[i].get("amount", None),
                            "TransactionCurrency": payload.get("transfer", {}).get("currency_code", None),
                            "Narration": payload.get("transfer", {}).get("description", "")
                        }
                    )
            # If bank_id is EQUITY
            elif super().get_bank_id() == super().EQUITY:
                data.update({
                    "source": {
                        "countryCode": payload.get("source", {}).get("country_code", None),
                        "name": payload.get("source", {}).get("name", None),
                        "accountNumber": payload.get("source", {}).get("account_number", None)
                    }
                })

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "destination": {
                            "type": "bank",
                            "countryCode": destination.get("country_code", None),
                            "name": destination.get("name", None),
                            "mobileNumber": destination.get("mobile_number", None),
                            "accountNumber": destination.get("account_number", None),
                            "bankCode": payload.get("transfer", {}).get("bank_code", None),
                        }
                    })

                    data.update({
                        "transfer": {
                            "type": "PesaLink",
                            "amount": f'{destination.get("amount",None)}',
                            "currencyCode": payload.get("transfer", {}).get("currency_code", None),
                            "reference": payload.get("transfer", {}).get("reference", None),
                            "date": payload.get("transfer", {}).get("date", None),
                            "description": payload.get("transfer", {}).get("description", ""),
                        }
                    })
            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "BankCode": payload.get("transfer", {}).get("bank_code", None),
                        "BankSwiftCode": payload.get("transfer", {}).get("bank_swift_code", None),
                        "BranchCode": payload.get("transfer", {}).get("branch_code", None),
                        "BeneficiaryAccountName": destination.get("name", None),
                        "Country": payload.get("transfer", {}).get("country", None),
                        "Reference": f'{default_reference}',
                        "Currency": payload.get("transfer", {}).get("currency_code", None),
                        "Account": destination.get("account_number", None),
                        "Amount": destination.get("amount", None),
                        "Narration": payload.get("transfer", {}).get("description", None),
                        "Transaction Date": payload.get("transfer", {}).get("date", date.today().strftime('%Y%m%d')).replace("-", ""),
                    })
        elif operation == super().PESALINK_TO_MOBILE:

            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                data.update({
                    "MessageReference": f'{default_reference}'
                })
                data.update({
                    "CallBackUrl": self.bank_sync_call_back.get("payments", "")
                })
                data.update({
                    "Source": {
                        "AccountNumber": payload.get("source", {}).get("account_number", None),
                        "Amount": payload.get("source", {}).get("amount", None),
                        "TransactionCurrency": payload.get("transfer", {}).get("currency_code", None),
                        "Narration": payload.get("transfer", {}).get("description", "")
                    }
                })

                destinations = payload.get("destinations", [])

                for i in range(len(destinations)):
                    if i == 0:
                        data.update({
                            "Destinations": []
                        })

                    data["Destinations"].append(
                        {
                            "ReferenceNumber": f'{default_reference}_1',
                            "PhoneNumber": destinations[i].get("mobile_number", None),
                            "Amount": destinations[i].get("amount", None),
                            "TransactionCurrency": payload.get("transfer", {}).get("currency_code", None),
                            "Narration": payload.get("transfer", {}).get("description", "")
                        }
                    )
            # If bank_id is EQUITY
            elif super().get_bank_id() == super().EQUITY:
                data.update({
                    "source": {
                        "countryCode": payload.get("source", {}).get("country_code", None),
                        "name": payload.get("source", {}).get("name", None),
                        "accountNumber": payload.get("source", {}).get("account_number", None)
                    }
                })

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "destination": {
                            "type": "mobile",
                            "countryCode": destination.get("country_code", None),
                            "name": destination.get("name", None),
                            "mobileNumber": destination.get("mobile_number", None),
                            "bankCode": payload.get("transfer", {}).get("bank_code", None),
                        }
                    })

                    data.update({
                        "transfer": {
                            "type": "PesaLink",
                            "amount": f'{destination.get("amount",None)}',
                            "currencyCode": payload.get("transfer", {}).get("currency_code", None),
                            "reference": payload.get("transfer", {}).get("reference", None),
                            "date": payload.get("transfer", {}).get("date", None),
                            "description": payload.get("transfer", {}).get("description", ""),
                        }
                    })
            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:
                pass
        elif operation == super().TRANSACTION_STATUS:

            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                data.update({
                    "MessageReference": payload.get("reference", None)
                })
            # If bank_id is EQUITY
            elif super().get_bank_id() == super().EQUITY:
                data.update({
                    "reference": payload.get("reference", None)
                })
            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:
                data.update({
                    "reference_number": payload.get("reference", None),
                    "country": payload.get("country", None)
                })
            # If bank_id is DTB
            elif super().get_bank_id() == super().DTB:
                data.update({
                    "identifier": {
                        "xref": get_code(),
                        "channel": "API",
                        "bank_code": payload.get("bank_code", ""),
                    },
                    "content": {
                        "source_reference": get_code(),
                        "transaction_branch": payload.get("branch_code", ""),
                        "txn_source_reference": payload.get("reference", ""),
                    }
                })
        elif operation == super().INITIATE_PAYMENT:

            if super().get_bank_id() in super().THIRD_PARTY_BANKING.keys():
                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    if super().get_bank_id() in [super().STITCH, super().PLAID]:
                        data = {
                            "secret": payload.get("transfer", {}).get("secret", ""),
                            "clientId": payload.get("transfer", {}).get("client_id", ""),
                            "receiptName": destination.get("name", ""),
                            "targetAccount": destination.get("account_number", ""),
                            "sortCode": payload.get("transfer", {}).get("sort_code", ""),
                            "currency": payload.get("transfer", {}).get("currency_code", ""),
                            "value": destination.get("amount", 0),
                            "referenceID": payload.get("transfer", {}).get("reference", ""),
                            "referenceMetaData": payload.get("transfer", {}).get("reference", ""),
                            "type":  payload.get("transfer", {}).get("type", ""),
                            "description": payload.get("transfer", {}).get("description", ""),
                            "nickname": destination.get("name", ""),
                            "country": payload.get("transfer", {}).get("country", ""),
                            "branchAddress": payload.get("transfer", {}).get("branch_address", ""),
                            "branchName": payload.get("transfer", {}).get("branch_name", ""),
                            "swiftCode": payload.get("transfer", {}).get("bank_swift_code", ""),
                            "iban": payload.get("transfer", {}).get("iban", ""),
                            "bankName": payload.get("transfer", {}).get("bank_name", ""),
                        }
                    elif super().get_bank_id() == super().MONO:
                        data = {
                            "userID": payload.get("transfer", {}).get("user_id", ""),
                        }
                    elif super().get_bank_id() == super().DAPI:
                        data = {
                            "appSecret": payload.get("transfer", {}).get("app_secret", ""),
                            "sortCode": payload.get("transfer", {}).get("sort_code", ""),
                            "userSecret": payload.get("transfer", {}).get("user_secret", ""),
                        }
        elif operation == super().STK_PUSH:
            # If bank_id is DTB
            if super().get_bank_id() == super().DTB:
                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "operator": destination.get("wallet_name", ""),
                        "identifier": {
                            "xref": f'API-{payload.get("transfer", {}).get("reference", get_code())}',
                            "channel": "API",
                            "bank_code": payload.get("transfer", {}).get("bank_code", ""),
                        },
                        "content": {
                            "timestamp": payload.get("transfer", {}).get("timestamp", ""),
                            "transaction_amount": int(float(destination.get("amount", 0))),
                            "credit_party": payload.get("source", {}).get("account_number", ""),
                            "debit_party": destination.get("mobile_number", ""),
                            "customer_msisdn": destination.get("mobile_number", ""),
                            "customer_name": destination.get("name", ""),
                            "account_reference": payload.get("transfer", {}).get("reference", ""),
                            "narration": payload.get("transfer", {}).get("description", ""),
                            "transaction_type": "CustomerPayBillOnline",
                        }
                    })

        data.update(payload.get("additional_properties", {}))
        data.update({
            "bank_id": super().get_bank_id(),
            "type": super().get_operation(),
            "bank_sync_call_back": self.bank_sync_call_back.get("payments", ""),
            "reference": default_reference
        })

        return data

    def response(self):
        return self.standardize_response(response_data=super().response())

    def standardize_response(self, response_data):

        data = {
            "bank_id": super().get_bank_id(),
            "type": super().get_operation()
        }

        if not isinstance(response_data,dict):
            data["response"]=response_data

        if super().get_bank_id() == super().COOP:

            data["message"] = response_data.get("MessageDescription", "")
            data["code"] = int(response_data.get("MessageCode", -1111111))

            if 'MessageDescription' in response_data.keys():
                if response_data.get("MessageDescription", "") == "Full Success":
                    data["message"] = "success"
                else:
                    data["message"] = response_data.get(
                        "MessageDescription", "")

            if 'MessageCode' in response_data.keys():
                data["code"] = int(response_data.get("MessageCode", -1111111))

            if 'Destinations' in response_data.keys():
                if response_data.get("Destinations", [{}]) is not None:

                    data["transaction_id"] = response_data.get(
                        "Destinations", [{}])[0].get("TransactionID", "")

            if 'MessageDateTime' in response_data.keys():
                data["date"] = response_data.get(
                    "MessageDateTime", date.today().strftime('%d/%m/%y %H:%M:%S'))

            if 'messageDescription' in response_data.keys():
                if response_data.get("messageDescription", "") == "Full Success":
                    data["message"] = "success"
                else:
                    data["message"] = response_data.get(
                        "messageDescription", "")

            if 'messageCode' in response_data.keys():
                data["code"] = int(response_data.get("messageCode", -1111111))

            if 'destination' in response_data.keys():
                if response_data.get("destination", {}) is not None:
                    data["transaction_id"] = response_data.get(
                        "destination", {}).get("transactionID", "")

            if 'messageDateTime' in response_data.keys():
                data["date"] = response_data.get(
                    "messageDateTime", date.today().strftime('%d/%m/%y %H:%M:%S'))

        elif super().get_bank_id() == super().EQUITY:
            data["message"] = response_data.get("message", "")
            data["code"] = response_data.get("code", -1111111)
            if 'mobileMoneyInfo' in response_data.keys():
                data["transaction_id"] = response_data.get(
                    "mobileMoneyInfo", {}).get("ThirdPartyTranID", "")
            else:
                data["transaction_id"] = response_data.get(
                    "data", {}).get("transactionId", response_data.get("transactionId", response_data.get("transactionId ", "")))
            data["date"] = response_data.get(
                "date", date.today().strftime('%d/%m/%y %H:%M:%S'))
        # If bank_id is DTB
        elif super().get_bank_id() == super().DTB:
            if super().get_operation() == super().IFT:
                data["message"] = response_data.get("message", "")
                data["code"] = int(float(response_data.get(
                    "content", {}).get("response_code", -1111111)))
                data["transaction_id"] = response_data.get(
                    "identifier", {}).get("trace_audit_number", "")
                data["transaction_reference"] = response_data.get(
                    "content", {}).get("transaction_reference", "")
                data["date"] = date.today().strftime('%d/%m/%y %H:%M:%S')
                if data["code"]:
                    data["message"] = "Transaction Failed"
                else:
                    data["message"] = "Success"
            elif super().get_operation() == super().MOBILE_WALLET:
                data["message"] = response_data.get(
                    "content", {}).get("response_description", "")
                data["code"] = int(float(response_data.get(
                    "content", {}).get("response_code", -1111111)))
                data["transaction_id"] = response_data.get(
                    "content", {}).get("conversation_id", "")
                data["transaction_reference"] = response_data.get(
                    "content", {}).get("service_reference", "")
            elif super().get_operation() == super().STK_PUSH:
                data["message"] = response_data.get(
                    "content", {}).get("response_description", "")
                data["code"] = int(float(response_data.get(
                    "content", {}).get("response_code", -1111111)))
                data["transaction_id"] = response_data.get(
                    "content", {}).get("merchant_request_id", "")
                data["transaction_reference"] = response_data.get(
                    "content", {}).get("service_reference", "")
        # If bank_id is UBA
        elif super().get_bank_id() == super().UBA:
            if super().get_operation() == super().IFT:
                resp_object = response_data.get("sendTransactionResponse", {}).get(
                    "return", {}).get("C24TRANRES", {})
                data["code"] = int(
                    float(resp_object.get("ACTION_CODE", -1111111)))
                data["transaction_id"] = resp_object.get("STAN", "")
                data["transaction_reference"] = resp_object.get("STAN", "")
                data["date"] = datetime.strptime(
                    f'{resp_object.get("TRAN_DATE_TIME", None)}', '%Y%m%d%H%M%S').strftime('%d/%m/%y %H:%M:%S')
                if data["code"]:
                    data["message"] = "Transaction Failed"
                else:
                    data["message"] = "Success"

        if bool(data):
            # save the data returned to be sent back to a callback
            self.simulate_callback(response=data)
            return data

        return super().response()
