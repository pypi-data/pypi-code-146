from copy import deepcopy

from coronado import TripleEnum
from coronado import TripleObject
from coronado.address import Address
from coronado.auth import Auth
from coronado.baseobjects import BASE_CARD_ACCOUNT_DICT, BASE_CARDHOLDER_OFFER_LOCATION_DICT
from coronado.exceptions import CallError
from coronado.exceptions import InvalidPayloadError
from coronado.exceptions import errorFor
from coronado.merchantcodes import MerchantCategoryCode as MCC
from coronado.offer import CardholderOffer
from coronado.offer import CardholderOfferDetails
from coronado.offer import OfferCategory
from coronado.offer import OfferDeliveryMode
from coronado.offer import OfferSearchResult
from coronado.offer import OfferType

import inspect
import json
import logging

import requests


SERVICE_PATH = 'partner/card-accounts'
"""
The default service path associated with CardAccount operations.

Usage:

```
CardAccount.initialize(serviceURL, SERVICE_PATH, auth)
```

Users are welcome to initialize the class' service path from regular strings.
This constant is defined for convenience.
"""


# --- globals ---

log = logging.getLogger(__name__)


# *** clases and objects ***

class CardholderOfferLocation(TripleObject):
    """
    A merchant's business adddress, whether physical or on-line.

    See `coronado.address.Address`
    """

    requiredAttributes = [
        'address',
        'objID',
    ]

    def __init__(self, obj = BASE_CARDHOLDER_OFFER_LOCATION_DICT):
        """
        Create a new MerchantLocation instance.
        """
        TripleObject.__init__(self, obj)


class CardAccountStatus(TripleEnum):
    """
    Account status object.
    See:  https://api.partners.dev.tripleupdev.com/docs#operation/createCardAccount
    """
    CLOSED = 'CLOSED'
    ENROLLED = 'ENROLLED'
    NOT_ENROLLED = 'NOT_ENROLLED'


class CardAccount(TripleObject):
    """
    Card accounts represent a cardholder's account association between triple and
    the payment card issuer's unique account ID.
    """
    requiredAttributes = [
       'objID',
       'cardProgramID',
       'createdAt',
       'externalID',
       'status',
       'updatedAt',
    ]
    allAttributes = TripleObject(BASE_CARD_ACCOUNT_DICT).listAttributes()


    def __init__(self, obj = BASE_CARD_ACCOUNT_DICT):
        TripleObject.__init__(self, obj)


    @classmethod
    def list(klass: object, paramMap = None, **args) -> list:
        """
        Return a list of card accounts.  The list is a sequential query from the
        beginning of time if no query parameters are passed:

        Arguments
        ---------
            pubExternalID : str
        A publisher external ID
            cardProgramExternalID : str
        A card program external ID
            cardAccountExternalID : str
        A card account external ID

        Returns
        -------
            list
        A list of TripleObjects objects with some card account attributes:

        - `objID`
        - `externalID`
        - `status`
        """
        paramMap = {
            'cardAccountExternalID': 'card_account_external_id',
            'cardProgramExternalID': 'card_program_external_id',
            'pubExternalID': 'publisher_external_id',
        }
        response = super().list(paramMap, **args)
        result = [ CardAccount(obj) for obj in json.loads(response.content)['card_accounts'] ]
        return result


    def offerActivations(self, includeExpired: bool = False, page:int = 0) -> list:
        """
        Get the activated offers associated with a cardAccountID.

        Arguments
        ---------
            includeExpired: bool
        When `True`, the results include activations up to 90 days old
        for expired offers along with all active offers; default = `False`

            page : int
        A page offset in the activations list; a page contains <= 1,000
        activations

        Returns
        -------
            aList : list
        The offer activation details objects associated with the card account
        details in the call.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        spec = {
            'include_expired': includeExpired,
            'page': page,
        }
        frame = inspect.currentframe()
        obj = frame.f_locals[frame.f_code.co_varnames[0]]
        thisMethod = getattr(obj, frame.f_code.co_name)

        endpoint = '/'.join([ self.__class__._serviceURL, self.__class__._servicePath, self.objID, thisMethod.action, ])
        response = requests.request('GET', endpoint, headers = self.__class__.headers, params = spec)

        # TODO:  Remove this test if you see this comment and Coronado version >= 1.4.0:
        if response.status_code == 200:
            result = [ CardholderOffer(activatedOffer) for activatedOffer in json.loads(response.content)['activated_offers'] ]
        elif response.status_code == 404:
            result = None
        else:
            raise errorFor(response.status_code, response.text)

        return result


    @classmethod
    def _error(klass, someErrorClass, explanation):
        e = someErrorClass(explanation)
        log.error()
        raise e


    def activateFor(self, offerIDs: list = None, offerCategory: object = None) -> list:
        """
        Activate the offers listed or by category for the receiver.

        Arguments
        ---------
            offerIDs: list
        A list of offer ID strings to activate

            offerCategory: OfferCategory
        An `coronado.offer.OfferCategory` instance.

        Only one of `offerIDs` list or `offerCategory` are required for
        activation.  This call will raise an error if both are provided in the
        same call.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        if offerIDs and offerCategory or not offerIDs and not offerCategory:
            raise CallError('Provide a value for offerIDs or offerCategory, not both set or both None')

        spec = dict()
        if offerCategory:
            spec['offer_category'] = str(offerCategory)
        if offerIDs:
            spec['offer_ids'] = offerIDs

        frame = inspect.currentframe()
        obj = frame.f_locals[frame.f_code.co_varnames[0]]
        thisMethod = getattr(obj, frame.f_code.co_name)

        endpoint = '/'.join([ self.__class__._serviceURL, self.__class__._servicePath, self.objID, thisMethod.action, ])
        response = requests.request('POST', endpoint, headers = self.__class__.headers, json = spec)

        print(response.content)
        if response.status_code == 200:
            result = [ CardholderOffer(item) for item in json.loads(response.content)['activated_offers'] ]
        elif response.status_code == 404:
            result = None
        else:
            e = errorFor(response.status_code, response.text)
            raise e

        return result


    def _queryWith(self, spec, action, auth):
        if auth:
            headers = deepcopy(self.__class__.headers)
            headers['Authorization'] = ' '.join([ auth.tokenType, auth.token, ])
        else:
            headers = self.__class__.headers
        endpoint = '/'.join([
            self.__class__._serviceURL,
            self.__class__._servicePath,
            self.objID,
            action,
        ])
        response = requests.request('POST', endpoint, headers = headers, json = spec)

        if response.status_code == 200:
            result = [json.loads(response.content)['total'],[OfferSearchResult(offer) for offer in json.loads(response.content)['offers']]]
        elif response.status_code == 404:
            result = None
        else:
            e = errorFor(response.status_code, response.text)
            log.error(e)
            raise e

        return result


    def findOffers(self, **args):
        """
        Search for offers that meet the query search criteria.  The underlying
        service allows for parameterized search and plain text searches.  The
        **<a href='https://api.tripleup.dev/docs' target='_blank'>Search Offers</a>**
        endpoint offers a full description of the object search capabilities.

        Arguments
        ---------
            countryCode
        The 2-letter ISO code for the country (e.g. US, MX, CA)

            filterCategory
        An offer category type filter; see coronado.offer.OfferType for details;
        valid values:  AUTOMOTIVE, CHILDREN_AND_FAMILY, ELECTRONICS,
        ENTERTAINMENT, FINANCIAL_SERVICES, FOOD, HEALTH_AND_BEAUTY, HOME,
        OFFICE_AND_BUSINESS, RETAIL, TRAVEL, UTILITIES_AND_TELECOM

            filterDeliveryMode
        An offer mode; see coronado.offer.OfferDeliveryMode for details; valid
        values:  IN_PERSON, IN_PERSON_AND_ONLINE, ONLINE,

            filterType
        An offer type filter; see coronado.offer.OfferType for details; valid
        values: AFFILIATE, CARD_LINKED, CATEGORICAL

            latitude
        The Earth latitude in degrees, with a whole and decimal part, e.g.
        40.46; relative to the equator

            longitude
        The Earth longitude in degrees, with a whole and decimal part, e.g.
        -79.92; relative to Greenwich

            pageSize
        The number of search results to return

            pageOffset
        The offset from the first result (inclusive) where to start fetching
        results for this query

            postalCode
        The postalCode associated with the cardAccountID

            radius
        The radius, in meters, to find offers with merchants established
        within that distance to the centroid of the postal code

            textQuery
        A text query to assist the back-end in further refinement of the query;
        free form text is allowed


        Returns
        -------
            list of OfferSearchResult
        A list of offer search results.  The list may be empty/zero-length,
        or `None`.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        if any(arg in args.keys() for arg in [ 'latitude', 'longitude', ]):
            requiredArgs = [
                'latitude',
                'longitude',
                'radius',
            ]
        else:
            requiredArgs = [
                'countryCode',
                'postalCode',
                'radius',
            ]

        if not all(arg in args.keys() for arg in requiredArgs):
            missing = set(requiredArgs)-set(args.keys())
            e = CallError('argument%s %s missing during instantiation' % ('' if len(missing) == 1 else 's', missing))
            log.error(e)
            raise e

        filters = dict()
        if 'filterCategory' in args:
            isinstance(args['filterCategory'], OfferCategory) \
                or CardAccount._error(CallError, 'filterCategory must be an instance of %s' % OfferCategory)
            filters['category'] = str(args['filterCategory'])
        if 'filterMode' in args:
            isinstance(args['filterMode'], OfferDeliveryMode) \
                or CardAccount._error(CallError, 'filterMode must be an instance of %s' % OfferDeliveryMode)
            filters['mode'] = str(args['filterMode'])
        if 'filterType' in args:
            isinstance(args['filterType'], OfferType) \
                or CardAccount._error(CallError, 'filterType must be an instance of %s' % OfferType)
            filters['type'] = str(args['filterType'])

        if 'viewAuth' in args and not isinstance(args['viewAuth'], Auth):
            e = InvalidPayloadError('%s is not instance of Auth; type = %s' % (args['viewAuth'], type(args['viewAuth'])))
            log.error(e)
            raise (e)

        try:
            spec = {
                'proximity_target': {
                    'country_code': args.get('countryCode', None),
                    'latitude': args.get('latitude', None),
                    'longitude': args.get('longitude', None),
                    'postal_code': args.get('postalCode', None),
                    'radius': args['radius'],
                },
                'text_query': args.get('textQuery', '').lower(),
                'page_size': args['pageSize'],
                'page_offset': args['pageOffset'],
                'apply_filter': filters,
            }
        except KeyError as e:
            e = CallError(str(e))
            log.error(e)
            raise e

        frame = inspect.currentframe()
        obj = frame.f_locals[frame.f_code.co_varnames[0]]
        thisMethod = getattr(obj, frame.f_code.co_name)

        return self._queryWith(spec, thisMethod.action, args.get('viewAuth', None))


    def _assembleDetailsFrom(self, payload):
        # payload ::= JSON
        d = json.loads(payload)

        if 'offer' not in d:
            e = CallError('offer attribute not found')
            log.error(e)
            raise e

        offer = CardholderOffer(d['offer'])
        offer.merchantCategory = MCC(offer.merchantCategory)
        offer.category = OfferCategory(offer.category)
        offer.offerMode = OfferDeliveryMode(offer.offerMode)
        offer.type = OfferType(offer.type)

        merchantLocations = [ CardholderOfferLocation(l) for l in d['merchant_locations'] ]

        for location in merchantLocations:
            location.address = Address(location.address)

        d['offer'] = offer
        d['merchant_locations'] = merchantLocations

        offerDetails = CardholderOfferDetails(d)

        return offerDetails


    def _forIDwithSpec(self, objID: str, spec: dict, action: object, auth: object) -> object:
        if auth:
            headers = deepcopy(self.__class__.headers)
            headers['Authorization'] = ' '.join([ auth.tokenType, auth.token, ])
        else:
            headers = self.__class__.headers

        endpoint = '/'.join([
            self.__class__._serviceURL,
            self.__class__._servicePath,
            self.objID,
            action,
        ])
        response = requests.request('POST', endpoint, headers = headers, json = spec)

        if response.status_code == 200:
            result = self._assembleDetailsFrom(response.content)
        elif response.status_code == 404:
            result = None
        else:
            e = errorFor(response.status_code, response.text)
            log.error(e)
            raise e

        return result


    def fetchOffer(self, offerID, **args) -> object:
        """
        Get the details and merchant locations for an offer.

        Arguments
        ---------
            offerID
        A known, valid offer ID

            countryCode
        The 2-letter ISO code for the country (e.g. US, MX, CA)

            latitude
        The Earth latitude in degrees, with a whole and decimal part, e.g.
        40.46; relative to the equator

            longitude
        The Earth longitude in degrees, with a whole and decimal part, e.g.
        -79.92; relative to Greenwich

            postalCode
        The postalCode associated with the cardAccountID

            radius
        The radius, in meters, to find offers with merchants established
        within that distance to the centroid of the postal code


        Returns
        -------
            CLOfferDetails
        An offer details instance if offerID is valid, else `None`.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        if any(arg in args.keys() for arg in [ 'latitude', 'longitude', ]):
            requiredArgs = [
                'latitude',
                'longitude',
                'radius',
            ]
        else:
            requiredArgs = [
                'countryCode',
                'postalCode',
                'radius',
            ]


        if not all(arg in args.keys() for arg in requiredArgs):
            missing = set(requiredArgs)-set(args.keys())
            e = CallError('argument%s %s missing during instantiation' % ('' if len(missing) == 1 else 's', missing))
            log.error(e)
            raise e

        spec = {
            'offer_id': offerID,
            'proximity_target': {
                'country_code': args.get('countryCode', None),
                'latitude': args.get('latitude', None),
                'longitude': args.get('longitude', None),
                'postal_code': args.get('postalCode', None),
                'radius': args['radius'],
            },
        }

        frame = inspect.currentframe()
        obj = frame.f_locals[frame.f_code.co_varnames[0]]
        thisMethod = getattr(obj, frame.f_code.co_name)

        return self._forIDwithSpec(offerID, spec, thisMethod.action, args.get('viewAuth', None))


    @classmethod
    def byExternalID(klass: object, externalID: str, **args) -> object:
        """
        Returns a card account instance using one or more its associated
        external IDs:

        - external card account ID (required)
        - external card program ID
        - external publisher ID

        The receiver returns the same object as instantiationd `CardAccount(someID)`
        using the ID that was assigned to the account when created in the
        triple system.

        Arguments
        ---------
            externalID: str
        The external card account ID (e.g. the one used by an FI) associated
        with the account to fetch.

            externalCardProgramID: str
        The external card program ID for the account associated with externalID

            externalPublisherID: str
        The external publisher ID for the external program associated with the
        externalID



        Returns
        -------
        A valid instance of CardAccount if one exists, None if the combination
        of external IDs doesn't yield one.  `None` if no object matches the
        combination of external IDs passed to the method.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full
        list of possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        if not externalID:
            raise CallError('externalID cannot be None')

        spec = {
            'card_account_external_id': externalID,
            'card_program_external_id': args.get('externalCardProgramID', None),
            'card_publisher_external_id': args.get('externalCardPublisherID', None),
        }
        action = 'partner/card-account.by-ids'
        endpoint = '/'.join([ klass._serviceURL, action, ])
        if 'viewAuth' in args:
            headers = deepcopy(klass.headers)
            headers['Authorization'] = ' '.join([ args['viewAuth'].tokenType, args['viewAuth'].token, ])
        else:
            headers = klass.headers

        response = requests.request('POST', endpoint, headers = headers, json = spec)

        if response.status_code == 200:
            account = CardAccount(json.loads(response.content))
        elif response.status_code == 422:
            account = None  # 404 - the ID isn't associated with an existing resource
        else:
            raise errorFor(response.status_code, response.text)

        return account


    @classmethod
    def create(klass,
               extCardAccountID: str,
               extCardProgramID: str,
               defaultCountryCode: str = 'US',
               defaultPostalCode: str = None,
               extPublisherID: str = None,
               status: CardAccountStatus = CardAccountStatus.ENROLLED) -> object:
        """
        Create a new CardAccount instance.

        For full details see `coronado.TripleObject.create()`.

        Arguments
        ---------
            extCardAccountID
        Partner-provided, external ID associated with a card account.  External
        IDs should be stable and never sensitive.

            extCardProgramID
        Partner provided external card program ID.

        External IDs are assumed to be stable and never **sensitive**.  External
        IDs need not be unique across publishers, but we encourage the use of
        UUIDs whenever possible.

        External publisher IDs may not match the nnn-nn-nnnn format of US tax
        IDs to prevent accidental inclusion of sensitive information.

            defaultCountryCode
        2-letter ISO-3166 country code.  Defaults to `US`.

            defaultPostalCode
        The postal code for the associated program.

            extPublisherID
        Partner-provided external publisher ID, if available.

            status
        Account enrollment status.  See:  `coronado.cardaccount.CardAccountStatus`
        for a list of possible values.  Defaults to `CardAccount.ENROLLED`.

        Returns
        -------

        An instance of CardAccount.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        spec = {
            'card_program_external_id': extCardProgramID,
            'default_country_code': defaultCountryCode,
            'default_postal_code': defaultPostalCode,
            'external_id': extCardAccountID,
            'publisher_external_id': extPublisherID,
            'status': str(status),
        }
        return CardAccount(super().create(spec))


CardAccount.activateFor.action = 'offers.activate'
CardAccount.offerActivations.action = 'offers.activations'
CardAccount.findOffers.action = 'offers.search'
CardAccount.fetchOffer.action = 'offers.details'

