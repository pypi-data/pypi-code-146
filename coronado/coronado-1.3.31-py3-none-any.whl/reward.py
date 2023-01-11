"""
## Important note for this module - using the EMPTY_DATABASE environment
variable

Set the environment variable `EMPTY_DATABASE` for special testing situations
where the testing database is empty and tests must be skipped.  Validation tests
run only during the initial merge of a pull request into the master development
branch, to validate that both Coronado and back-end code perform the correct
logic.  Branches are merged and exercised GitHub Actions.  The `EMPTY_DATABASE`
environment variable must be set in the GitHub Action script that runs the
Coronado tests, and **only** in environments other than dev.

    EMPTY_DATABASE
Set to `False` if the environment variable equals `"0"`, `"False"`, `"false"`,
`"FALSE"` or any character combination that spells "False".  Any other other
value set for the `EMPTY_DATABASE` environment variable will set this constant
to `True`.  The implementation uses the `bool()` built-in for value resolution.
"""


from coronado import TripleEnum
from coronado import TripleObject
from coronado.baseobjects import BASE_REWARD_DICT
from coronado.daterange import DateRange
from coronado.exceptions import CallError
from coronado.exceptions import errorFor

import json
import logging

import requests


# +++ constants +++

SERVICE_PATH = '/partner/rewards'
"""
The default service path associated with Reward operations.

Usage:

```
Reward.initialize(serviceURL, SERVICE_PATH, auth)
```

Users are welcome to initialize the class' service path from regular strings.
This constant is defined for convenience.
"""


# --- globals ---

log = logging.getLogger(__name__)


# --- functions ---

def _assembleDetailsFrom(payload):
    result = json.loads(payload)

    if isinstance(result, dict):
        result = result['ok']
    elif isinstance(result, list):
        result = [ TripleObject(x) for x in result ]

    return result


# *** classes and objects ***

class RewardStatus(TripleEnum):
    DENIED_BY_MERCHANT = 'DENIED_BY_MERCHANT'
    """
    The merchant or content provider denied the reward.  The `Reward.rewardDetails
    field will include information about the denial.
    """

    DISTRIBUTED_TO_CARDHOLDER = 'DISTRIBUTED_TO_CARDHOLDER'
    """
    The publisher has reported that the reward was given to the cardholder.
    """

    DISTRIBUTED_TO_PUBLISHER = 'DISTRIBUTED_TO_PUBLISHER'
    """
    Reward funds have been sent to the publisher.
    """

    PENDING_MERCHANT_APPROVAL = 'PENDING_MERCHANT_APPROVAL'
    """
    The transaction awaits for the merchant or content provider to approve or
    deny the reward.
    """

    PENDING_MERCHANT_FUNDING = 'PENDING_MERCHANT_FUNDING'
    """
    The reward was approved and awaits funding by the merchant.
    """

    PENDING_REVIEW = "PENDING_REVIEW"
    """
    The Transaction is pending a manual review. The reward may be deleted if it is
    determined to be an invalid match to this merchant's offer.
    """

    PENDING_TRANSFER_TO_PUBLISHER = 'PENDING_TRANSFER_TO_PUBLISHER'
    """
    The reward is funded and funds await distribution to the publisher.
    """

    REJECTED = 'REJECTED'
    """
    The transaction did not meet the offer terms.
    """


class RewardType(TripleEnum):
    """
    Reward types may be expressed as percentags or fixed.
    """
    FIXED = 'FIXED'
    PERCENTAGE = 'PERCENTAGE'


class Reward(TripleObject):
    """
    Reward instances represent exchanges between buyers and sellers that
    may have a linked offer.
    """

    requiredAttributes = [
        'merchantName',
        'offerID',
        'status',
        'transactionAmount',
        'transactionCurrencyCode',
        'transactionID'
        'transactionTimestamp',
    ]
    allAttributes = TripleObject(BASE_REWARD_DICT).listAttributes()

    def __init__(self, obj = BASE_REWARD_DICT):
        TripleObject.__init__(self, obj)


    @classmethod
    def list(klass: object, paramMap = None, **args) -> list:
        """
        List all rewards that match any of the criteria set by the
        arguments to this method.

        Arguments
        ---------
            status
        A `coronado.reward.RewardStatus` instance.  May be blank for a list of
        everything.


        Returns
        -------
            list
        A list of Reward objects; can be `None`.
        """
        paramMap = {
            'status': 'status',
        }
        if 'status' in args:
            if not isinstance(args['status'], RewardStatus):
                e = CallError('invalid type for status - use RewardStatus objects')
                log.error(e)
                raise e
            args['status'] = str(args['status'])

        response = super().list(paramMap, **args)
        result = [ TripleObject(obj) for obj in json.loads(response.content)['rewards'] ]
        for r in result:
            r.status = RewardStatus(r.status)

        return result


    @classmethod
    def _action(klass, transactionID: str, offerID: str, notes:str = None, action:str = 'approve') -> object:
        if action not in ( 'approve', 'deny'):
            e = CallError('invalid type for status - use RewardStatus objects')
            log.error(e)
            raise e

        spec = {
            'transaction_id': transactionID,
            'offer_id': offerID,
        }
        if notes:
            spec['notes'] = notes

        if None == notes and 'deny' == action:
            e = CallError('invalid type for status - use RewardStatus objects')
            log.error(e)
            raise e

        if '' == notes and 'deny' == action:
            e = CallError('invalid type for status - use RewardStatus objects')
            log.error(e)
            raise e

        endpoint = '/'.join([ klass._serviceURL, 'partner/rewards.%s' % action ])
        response = requests.request('POST', endpoint, headers = klass.headers, json = spec)

        if response.status_code == 200:
            result = _assembleDetailsFrom(response.content)
        elif response.status_code == 404:
            result = False
        else:
            e = errorFor(response.status_code, response.text)
            log.error(e)
            raise e
        return result


    @classmethod
    def approve(klass, transactionID: str, offerID: str) -> object:
        """
        Transition a reward status from `PENDING_MERCHANT_APPROVAL` to
        `PENDING_MERCHANT_FUNDING`.

        Arguments
        ---------
            transactionID
        The transaction to which the reward applied

            offerID
        The offer associated with the reward

        Returns
        -------
            Boolean || list || str
        A free from object that may contain one of:

        - a sequence of TripleObject instances; OR
        - one or more strings; OR
        - a string with an informative message
        - a Boolean value when the operation is successful

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        return klass._action(transactionID, offerID, action = 'approve')



    @classmethod
    def deny(klass, transactionID: str, offerID: str, notes: str) -> object:
        """
        Transition a reward from PENDING_MERCHANT_APPROVAL to DENIED_BY_MERCHANT
        status.

        Arguments
        ---------
            transactionID
        The transaction to which the reward applied

            offerID
        The offer associated with the reward

            notes
        Additional information about why the merchant rejected the offer.  This
        field is not intended for display to cardholders.

        Returns
        -------
            Boolean || list || str
        A free from object that may contain one of:

        - a sequence of TripleObject instances; OR
        - one or more strings; OR
        - a string with an informative message
        - a Boolean value when a reward is denied successfully

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        return klass._action(transactionID, offerID, notes, action = 'deny')


    @classmethod
    def updateStatus(klass, transactionID: str, offerID: str, status: str) -> object:
        """
        Allow publisher to update the status of a reward.

        Arguments
        ---------
            transactionID
        The transaction to which the reward applied

            offerID
        The offer associated with the reward

            status
        Status to which the RewardStatus is to be changed.

        Returns
        -------
            Boolean || list || str
        A free from object that may contain one of:

        - a sequence of TripleObject instances; OR
        - one or more strings; OR
        - a string with an informative message
        - a Boolean value when a reward is denied successfully

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """

        spec = {
            'transaction_id': transactionID,
            'offer_id': offerID,
            'status': status,
        }

        endpoint = '/'.join([ klass._serviceURL, 'partner/rewards.update_status' ])
        response = requests.request('POST', endpoint, headers = klass.headersImpersonation, json = spec)

        if response.status_code == 200:
            result = _assembleDetailsFrom(response.content)
        elif response.status_code == 404:
            result = False
        else:
            e = errorFor(response.status_code, response.text)
            log.error(e)
            raise e
        return result


    @classmethod
    def aggregateByPublisher(klass,
                  dateRangeTemplate: DateRange,
                  endDate: str = None,
                  extPublisherID: str = None,
                  startDate: str = None) -> object:
        """
        Aggregate rewards by publisher between a date range for either:

        Specify the date range using the DateRange object.  Set `dateRangeTemplate`
        to `CUSTOM` to define  custom date range using the `startDate` and
        `endDate` propoerties.

        Arguments
        ---------
            dateRangeTemplate: coronado.daterange.DateRange
        An enumeration for selecting the right date query template.

            endDate
        The period end date for a `CUSTOM` search.

            extPublisherID
        Partner-provided, external publisher ID.

            startDate
        The period start date for a `CUSTOM` search.

        Returns
        -------
        An tactical TripleObject with a reference to an S3 bucket holding the
        rewards aggregate data, and an expiration date.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """

        spec = {
            'date_range_template': str(dateRangeTemplate),
            'end_date': endDate,
            'publisher_external_id': extPublisherID,
            'start_date': startDate,
        }
        endpoint = '/'.join([ klass._serviceURL, 'partner/rewards.aggregate-by-publisher' ])
        response = requests.request('POST', endpoint, headers = klass.headers, json = spec)

        if response.status_code == 200:
            result = TripleObject(json.loads(response.content))
        else:
            raise errorFor(response.status_code, response.text)

        return result


    @classmethod
    # def aggregateByAccount(klass,
    def aggregateByCardProgram(klass,
                  dateRangeTemplate: DateRange,
                  extCardProgramID: str,
                  endDate: str = None,
                  extPublisherID: str = None,
                  startDate: str = None) -> object:
        """
        Aggregate rewards by publisher between a date range for either:

        Specify the date range using the DateRange object.  Set `dateRangeTemplate`
        to `CUSTOM` to define  custom date range using the `startDate` and
        `endDate` propoerties.

        Arguments
        ---------
            dateRangeTemplate: coronado.daterange.DateRange
        An enumeration for selecting the right date query template.

            extCardProgramID
        Partner-provided, external card program ID.

            endDate
        The period end date for a `CUSTOM` search.

            extPublisherID
        Partner-provided, external publisher ID.

            startDate
        The period start date for a `CUSTOM` search.

        Returns
        -------
        An tactical TripleObject with a reference to an S3 bucket holding the
        rewards aggregate data, and an expiration date.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """

        spec = {
            'card_program_external_id': extCardProgramID,
            'date_range_template': str(dateRangeTemplate),
            'end_date': endDate,
            'publisher_external_id': extPublisherID,
            'start_date': startDate,
        }
        endpoint = '/'.join([ klass._serviceURL, 'partner/rewards.aggregate-by-card-program' ])
        response = requests.request('POST', endpoint, headers = klass.headers, json = spec)

        if response.status_code == 200:
            result = TripleObject(json.loads(response.content))
        else:
            raise errorFor(response.status_code, response.text)

        return result


    @classmethod
    def aggregateByCardAccount(klass,
                  dateRangeTemplate: DateRange,
                  extCardAccountID: str,
                  extCardProgramID: str,
                  endDate: str = None,
                  extPublisherID: str = None,
                  startDate: str = None) -> object:
        """
        Aggregate rewards by publisher between a date range for either:

        Specify the date range using the DateRange object.  Set `dateRangeTemplate`
        to `CUSTOM` to define  custom date range using the `startDate` and
        `endDate` propoerties.

        Arguments
        ---------
            dateRangeTemplate: coronado.daterange.DateRange
        An enumeration for selecting the right date query template.

            extCardProgramID
        Partner-provided, external card program ID.

            endDate
        The period end date for a `CUSTOM` search.

            extPublisherID
        Partner-provided, external publisher ID.

            startDate
        The period start date for a `CUSTOM` search.

        Returns
        -------
        An tactical TripleObject with a reference to an S3 bucket holding the
        rewards aggregate data, and an expiration date.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """

        spec = {
            'card_account_external_id': extCardAccountID,
            'card_program_external_id': extCardProgramID,
            'date_range_template': str(dateRangeTemplate),
            'end_date': endDate,
            'publisher_external_id': extPublisherID,
            'start_date': startDate,
        }
        endpoint = '/'.join([ klass._serviceURL, 'partner/rewards.aggregate-by-card-account' ])
        response = requests.request('POST', endpoint, headers = klass.headers, json = spec)

        if response.status_code == 200:
            result = TripleObject(json.loads(response.content))
        else:
            raise errorFor(response.status_code, response.text)

        return result
