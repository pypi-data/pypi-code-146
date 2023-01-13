# vim: set fileencoding=utf-8:


from coronado import TripleEnum
from coronado import TripleObject
from coronado.address import Address
from coronado.baseobjects import BASE_TRANSACTION_DICT
from coronado.exceptions import CallError
from coronado.merchantcodes import MerchantCategoryCode

import json


SERVICE_PATH = 'partner/transactions'
"""
The default service path associated with Transaction operations.

Usage:

```
Transaction.initialize(serviceURL, SERVICE_PATH, auth)
```

Users are welcome to initialize the class' service path from regular strings.
This constant is defined for convenience.
"""


# +++ classes +++

class MatchingStatus(TripleEnum):
    HISTORIC_TRANSACTION = 'HISTORIC_TRANSACTION'
    QUEUED = 'QUEUED'
    NOT_APPLICABLE = 'NOT_APPLICABLE'
    NOT_ENROLLED = 'NOT_ENROLLED'
    NO_ACTIVE_OFFER = 'NO_ACTIVE_OFFER'
    MATCHED = 'MATCHED'


class ProcessorMIDType(TripleEnum):
    AMEX_SE_NUMBER = 'AMEX_SE_NUMBER'
    DISCOVER_MID = 'DISCOVER_MID'
    MC_AUTH_ACQ_ID = 'MC_AUTH_ACQ_ID'
    MC_AUTH_ICA = 'MC_AUTH_ICA'
    MC_AUTH_LOC_ID = 'MC_AUTH_LOC_ID'
    MC_CLEARING_ACQ_ID = 'MC_CLEARING_ACQ_ID'
    MC_CLEARING_ICA = 'MC_CLEARING_ICA'
    MC_CLEARING_LOC_ID = 'MC_CLEARING_LOC_ID'
    MERCHANT_PROCESSOR = 'MERCHANT_PROCESSOR'
    NCR = 'NCR'
    VISA_VMID = 'VISA_VMID'
    VISA_VSID = 'VISA_VSID'


class TransactionType(TripleEnum):
    CHECK = 'CHECK'
    DEPOSIT = 'DEPOSIT'
    FEE = 'FEE'
    PAYMENT = 'PAYMENT'
    PURCHASE = 'PURCHASE'
    REFUND = 'REFUND'
    TRANSFER = 'TRANSFER'
    WITHDRAWAL = 'WITHDRAWAL'


class Transaction(TripleObject):
    """
    Transaction instances represent exchanges between buyers and sellers that
    may have a linked offer.
    """

    requiredAttributes = [
        'amount',
        'cardAccountID',
        'cardBIN',
        'cardLast4',
        'createdAt',
        'currencyCode',
        'debit',
        'description',
        'externalID',
        'matchingStatus',
        'merchantAddress',
        'timestamp',
        'transactionType',
        'updatedAt',
    ]
    allAttributes = TripleObject(BASE_TRANSACTION_DICT).listAttributes()

    def __init__(self, obj = BASE_TRANSACTION_DICT):
        TripleObject.__init__(self, obj)


    # TODO:  Update the docstring to link to Rewards and reward details when
    #        that code is implemented by the back-end and Coronado.
    @classmethod
    def list(klass: object, paramMap = None, **args) -> list:
        """
        List all transactions that match any of the criteria set by the
        arguments to this method.

        Arguments
        ---------
            cardAccountExternalID
        String, 1-50 characters partner-provided external ID

            cardProgramExternalID
        String, 1-50 characters partner-provided external ID

            endDate
        A string date - includes only transactions that start from the date in
        format:  YYYY-mm-dd

            matched
        A Boolean flag; if True, includes only the transactions matched to an
        active offer.  See Reward Details for more information.
            publisherExternalID
        String, 1-50 characters partner-provided external ID

            startDate
        A string date - includes only transactions that start from the date in
        format:  YYYY-mm-dd

            transactionExternalID
        String, 1-50 characters partner-provided external ID

        Returns
        -------
            list
        A list of Transaction objects; can be `None`.
        """
        paramMap = {
            'cardAccountExternalID': 'card_account_external_id',
            'cardProgramExternalID': 'card_program_external_id',
            'endDate': 'end_date',
            'matched': 'matched',
            'startDate': 'start_date',
            'transactionExternalID': 'transaction_external_id',
        }
        response = super().list(paramMap, **args)
        result = [ Transaction(obj) for obj in json.loads(response.content)['transactions'] ]

        for transaction in result:
            transaction.matchingStatus = MatchingStatus(transaction.matchingStatus)
            transaction.merchantCategory = MerchantCategoryCode(transaction.merchantCategory)

        return result

    @classmethod
    def create(klass,
               amount: float,
               extCardAccountID: str,
               extCardProgramID: str,
               debit: bool,
               description: str,
               extTXID: str,
               merchantCategoryCode: str,
               merchantAddress: Address,
               processorMID: str,
               processorMIDType: ProcessorMIDType,
               timestamp: str,
               transactionType: TransactionType,
               cardBIN: str,
               cardLast4: str,
               currencyCode: str = 'USD',
               extPublisherID: str = None) -> object:
        """
        Creates a new Transaction instance.  Important notes:

        - _Do not submit authorizations as purchases_
        - The amount of a purchase transaction _should not include cash back_ if
          it was part of the transaction
        - Transactions must be submitted _within 3 days_ of when they took place

        Arguments
        ---------
            amount
        The amount of the transaction.

            extCardAccountID
        External card account ID.

            extCardProgramID
        External card program ID.

            debit
        A Boolean that indicates if the transaction was made from a debit (`True`)
        or credit (`False`) payment card.

            description
        The transaction description, often includes or is only the merchant
        name.

            extTXID
        The external transaction ID reported by the payment processor.

            merchantCategoryCode
        The 4-digit MCC code associated with the merchant and purchase.  See:
        `coronado.merchantcodes.MerchantCategoryCode` for details.

            merchantAddress
        The merchant's real world address.  See:  `coronado.address.Address` for
        object format.

            processorMID
        The processor-assigned merchant ID.

            processorMIDType
        The payment card processor network.  See:  `coronado.Transaction.ProcessorMIDType`
        for details.

            timestamp
        Reported RFC-3339 datetime used for the creation and modification times.

            transactionType
        The transaction type.  See:  `coronado.Transaction.TransactionType` for
        details.

            cardBIN
        The payment card Bank Identification Number.

            cardLast4
        The payment card's last 4 digits.

            currencyCode
        3-character ISO-4217 currency code.  Defaults to `USD`.

            extPublisherID
        Partner-provided external publisher ID, if available.

        Returns
        -------
        An instance of a Transaction.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        spec = {
            'amount': amount,
            'card_account_external_id': extCardAccountID,
            'card_bin': cardBIN,
            'card_last_4': cardLast4,
            'card_program_external_id': extCardProgramID,
            'currency_code': currencyCode,
            'debit': debit,
            'description': description,
            'external_id': extTXID,
            'merchant_category_code': merchantCategoryCode,
            'merchant_address': merchantAddress.asSnakeCaseDictionary(),
            'processor_mid': processorMID,
            'processor_mid_type': str(processorMIDType),
            'publisher_external_id': extPublisherID,
            'timestamp': timestamp,
            'transaction_type': str(transactionType),
        }
        if not cardBIN or not str(cardBIN).isnumeric():
            raise CallError('Provide a valid cardBIN.')
        if len(cardLast4) < 4 or not str(cardLast4).isnumeric():
            raise CallError('Provde a valid value for last 4 digits of card.')
        transaction = Transaction(super().create(spec))
        transaction.merchantAddress = Address(transaction.merchantAddress)
        if transaction.merchantCategory:
            transaction.merchantCategory = MerchantCategoryCode(transaction.merchantCategory)
        if transaction.processorMIDType:
            transaction.processorMIDType = ProcessorMIDType(transaction.processorMIDType)
        transaction.transactionType = TransactionType(transaction.transactionType)

        return transaction


    @classmethod
    def byID(klass, objID: str) -> object:
        """
        Return the transaction associated with objID.

        Arguments
        ---------
            objID : str
        The transaction ID associated with the resource to fetch

        Returns
        -------
        The transaction associated with objID or None

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        transaction = Transaction(super().byID(objID))
        transaction.merchantAddress = Address(transaction.merchantAddress)
        if transaction.merchantCategory:
            transaction.merchantCategory = MerchantCategoryCode(transaction.merchantCategory)
        if transaction.processorMIDType:
            transaction.processorMIDType = ProcessorMIDType(transaction.processorMIDType)
        transaction.transactionType = TransactionType(transaction.transactionType)

        return transaction

