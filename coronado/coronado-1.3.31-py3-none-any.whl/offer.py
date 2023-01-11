# vim: set fileencoding=utf-8:


from coronado import TripleEnum
from coronado import TripleObject
from coronado.baseobjects import BASE_CARDHOLDER_OFFER_DETAILS_DICT
from coronado.baseobjects import BASE_OFFER_DICT
from coronado.baseobjects import BASE_OFFER_SEARCH_RESULT_DICT


# +++ constants +++

_SERVICE_PATH = 'partner/publishers'


# *** classes and objects ***


class MarketingFeeType(TripleEnum):
    """
    Offer fees may be expressed as percentages or fixed.
    """
    FIXED = 'FIXED'
    PERCENTAGE = 'PERCENTAGE'


class OfferCategory(TripleEnum):
    """
    High-level offer categories.  May be database-based in future
    implementations.
    """
    AUTOMOTIVE = 'AUTOMOTIVE'
    CHILDREN_AND_FAMILY = 'CHILDREN_AND_FAMILY'
    ELECTRONICS = 'ELECTRONICS'
    ENTERTAINMENT = 'ENTERTAINMENT'
    FINANCIAL_SERVICES = 'FINANCIAL_SERVICES'
    FOOD = 'FOOD'
    HEALTH_AND_BEAUTY = 'HEALTH_AND_BEAUTY'
    HOME = 'HOME'
    OFFICE_AND_BUSINESS = 'OFFICE_AND_BUSINESS'
    RETAIL = 'RETAIL'
    TRAVEL = 'TRAVEL'
    UTILITIES_AND_TELECOM = 'UTILITIES_AND_TELECOM'


class OfferDeliveryMode(TripleEnum):
    """
    Offer delivery mode.
    """
    IN_PERSON = 'IN_PERSON'
    IN_PERSON_AND_ONLINE = 'IN_PERSON_AND_ONLINE'
    ONLINE = 'ONLINE'


class OfferType(TripleEnum):
    """
    Offer type definitions.
    """
    AFFILIATE = 'AFFILIATE'
    CARD_LINKED = 'CARD_LINKED'
    CATEGORICAL = 'CATEGORICAL'


class Offer(TripleObject):
    """
    The parent abstract class for all Coronado offer classes.
    """

    requiredAttributes = [
        'activationRequired',
        'currencyCode',
        'effectiveDate',
        'expirationDate',
        'headline',
        'isActivated',
        'minimumSpend',
        'rewardType',
        'type',
    ]
    allAttributes = TripleObject(BASE_OFFER_DICT).listAttributes()

    def __init__(self, obj = BASE_OFFER_DICT):
        """
        Create a new Offer instance.

        spec:

        ```
        {
            'lorem': 'ipsum',
        }
        ```
        """
        TripleObject.__init__(self, obj)


class OfferSearchResult(Offer):
    """
    Offer search result.  Search results objects are only produced
    when executing a call to the `forQuery()` method.  Each result represents
    an offer recommendation based on the caller's geolocation, transaction
    history, and offer interactions.

    OfferSearchResult objects can't be instantiated by themselves, and are
    always the result from running a query against the triple API.
    """

    # *** public ***

    requiredAttributes = [
        'objID',
        'activationRequired',
        'currencyCode',
        'effectiveDate',
        'externalID',
        'headline',
        'isActivated',
        'offerMode',
        'score',
        'type',
    ]
    allAttributes = TripleObject(BASE_OFFER_SEARCH_RESULT_DICT).listAttributes()


    def __init__(self, obj = BASE_OFFER_SEARCH_RESULT_DICT):
        """
        Create a new OfferSearchResult instance.  Objects of this class should
        not be instantiated via constructor in most cases.  Use the `forQuery()`
        method to query the system for valid results.
        """
        TripleObject.__init__(self, obj)


    @classmethod
    def create(klass, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def byID(klass, objID: str) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def updateWith(klass, objID: str, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def list(klass, paramMap = None, **args) -> list:
        """
        **Disabled for this class.**
        """
        None


class CardholderOfferDetails(TripleObject):
    """
    Object representation of the offer details and associated merchant
    locations for an offer.
    """

    # --- private ---

    @classmethod
    def _forIDwithSpec(klass, objID: str, spec: dict, includeLocations: bool) -> object:
        endpoint = '/'.join([ klass._serviceURL, 'partner/offer-display/details', objID, ])
        response = requests.request('POST', endpoint, headers = klass.headers, json = spec)

        if response.status_code == 200:
            result = _assembleDetailsFrom(response.content)
        elif response.status_code == 404:
            result = None
        else:
            e = errorFor(response.status_code, response.text)
            log.error(e)
            raise e

        return result


    # +++ public +++

    requiredAttributes = [
        'offer',
    ]
    allAttributes = TripleObject(BASE_CARDHOLDER_OFFER_DETAILS_DICT).listAttributes()

    def __init__(self, obj = BASE_CARDHOLDER_OFFER_DETAILS_DICT):
        """
        Create a new CLOffer instance.
        """
        TripleObject.__init__(self, obj)


    @classmethod
    def forID(klass, offerID: str, **args) -> object:
        """
        Get the details and merchant locations for an offer.

        Arguments
        ---------
            offerID
        A known, valid offer ID

            cardAccountID
        A valid, known card account ID registered with the system

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

            includeLocations
        Set to `True` to include the merchant locations in the response.

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
                'cardAccountID',
                'latitude',
                'longitude',
                'radius',
            ]
        else:
            requiredArgs = [
                'cardAccountID',
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
            'proximity_target': {
                'country_code': args.get('countryCode', None),
                'latitude': args.get('latitude', None),
                'longitude': args.get('longitude', None),
                'postal_code': args.get('postalCode', None),
                'radius': args['radius'],
            },
            'card_account_identifier': {
                'card_account_id': args['cardAccountID'],
            },
        }

        return klass._forIDwithSpec(offerID, spec, args.get('includeLocations', False))


    @classmethod
    def create(klass, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def byID(klass, objID: str) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def updateWith(klass, objID: str, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def list(klass, paraMap = None, **args) -> list:
        """
        **Disabled for this class.**
        """
        None


class CardholderOffer(Offer):
    """
    CLOffer presents a detailed view of a card linked offer (CLO) with all the
    relevant details.

    Offer objects represent offers from brands and retaliers linked to a payment
    provider like a debit or credit card.  The offer is redeemed by the consumer
    when the linked payment card is used at a point-of-sale.  Offer instances
    connect on-line advertising campaings with concrete purchases.
    """

    requiredAttributes = [
        'activationRequired',
        'currencyCode',
        'effectiveDate',
        'headline',
        'isActivated',
        'merchantID',
        'merchantName',
        'minimumSpend',
        'category',
        'offerMode',
        'rewardType',
        'type',
    ]
    allAttributes = TripleObject(BASE_CARDHOLDER_OFFER_DETAILS_DICT).listAttributes()

    def __init__(self, obj = BASE_CARDHOLDER_OFFER_DETAILS_DICT):
        """
        Create a new OfferSearchResult instance.  Objects of this class should
        not be instantiated via constructor in most cases.  Use the `forQuery()`
        method to query the system for valid results.
        """
        TripleObject.__init__(self, obj)


    @classmethod
    def create(klass, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def byID(klass, objID: str) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def updateWith(klass, objID: str, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def list(klass, paraMap = None, **args) -> list:
        """
        **Disabled for this class.**
        """
        None

