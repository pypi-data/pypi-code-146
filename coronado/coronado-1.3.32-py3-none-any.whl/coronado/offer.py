# vim: set fileencoding=utf-8:


from decimal import Decimal

from coronado import TripleEnum
from coronado import TripleObject
from coronado.baseobjects import BASE_CARDHOLDER_OFFER_DETAILS_DICT
from coronado.baseobjects import BASE_OFFER_DICT
from coronado.baseobjects import BASE_OFFER_SEARCH_RESULT_DICT
from coronado.exceptions import InvalidPayloadError
from coronado.reward import RewardType

import json
import logging

# +++ constants +++

SERVICE_PATH = 'partner/offers'

log = logging.getLogger(__name__)

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
        'externalID',
        'headline',
        'marketingFeeType',
        'merchantCategories',
        'minimumSpend',
        'rewardType',
        'offerType',
        'activationDurationInDays',
        'campaignEndsOn',
        'category',
        'categoryTags',
        'createdAt',
        'description',
        'excludedDates',
        'expirationDate',
        'marketingFeeCurrencyCode',
        'marketingFeeRate',
        'marketingFeeValue',
        'maxRedemptions',
        'maximumCumulativeReward',
        'maximumRewardPerTransaction',
        'merchantCategories',
        'merchantExternalID',
        'merchantWebsite',
        'mode',
        'rewardRate',
        'rewardValue',
        'terms',
        'updatedAt',
        'validDayParts',
    ]
    allAttributes = TripleObject(BASE_OFFER_DICT).listAttributes()

    def __init__(self, obj = BASE_OFFER_DICT):
        """
        Create a new instance of an Offer.  `obj` must correspond to a
        valid, existing object ID if it's not a collection or JSON.

        Arguments
        ---------
            obj
        An object used for building a valid offer.  The object can
        be one of:

        - A dictionary - a dictionary with instantiation values as described
          in the API documentation
        - A JSON string
        - A triple objectID

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        TripleObject.__init__(self, obj)


    @classmethod
    def list(klass, paramMap = None, **args) -> list:
        """
        Return a list of offers.

        Arguments
        ---------
            merchantExternalID
        An external merchant ID; optional

            externalID
        An external offer ID; optional

        Returns
        -------
            list
        A list of Offer objects

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the sepcific error condition.  The full list of
        possible errors, causes, and semantics is available in the 
        **`coronado.exceptions`** module.
        """
        None
        paramMap = {
            'externalID': 'external_id',
            'merchantExternalID': 'merchant_external_id',
            'page': 'page',
            'pageSize': 'page_size',
        }

        response = super().list(paramMap, **args)
        result = [ Offer(obj) for obj in json.loads(response.content)['offers'] ]

        return result


    @classmethod
    def create(klass,
        activationRequired: bool,
        currencyCode: str,
        effectiveDate: str,
        externalID: str,
        headline: str,
        marketingFeeType: MarketingFeeType,
        minimumSpend: Decimal,
        rewardType: RewardType,
        offerType: OfferType,
        activationDurationInDays: int = None,
        campaignEndsOn: str = None,
        category: str = None,
        categoryTags: str = None,
        description: str = None,
        excludedDates: list = [ ],
        expirationDate: str = None,
        marketingFeeCurrencyCode: str = None,
        marketingFeeRate: Decimal = None,
        marketingFeeValue: Decimal = None,
        maxRedemptions: str = None,
        maximumCumulativeReward: Decimal = None,
        maximumRewardPerTransaction: Decimal = None,
        merchantCategories: list = [ ],
        merchantExternalID: str = None,
        merchantWebsite: str = None,
        mode: OfferDeliveryMode = None,
        rewardRate: Decimal = None,
        rewardValue: Decimal = None,
        terms: str = None,
        validDayParts: list = [ ]) -> object:
        
        """
        Creates an Offer.

        For full details see `coronado.TripleObject.create()`.

        Arguments
        ---------
            activationRequired
        Boolean default False

            currencyCode
        3-character ISO-4217 currency code.  At this time only USD is supported.
        Contact triple for support of additional currencies.  
        
            effectiveDate
        String value for offer start date.  Format `YYYY-MM-DD`

            extOfferID
        External IDs are assumed to be stable and never **sensitive**.  External
        IDs need not be unique across publishers, but we encourage the use of
        UUIDs whenever possible.

        External IDs may not match the nnn-nn-nnnn format of US tax
        IDs to prevent accidental inclusion of sensitive information.

            headline
        Title for the offer

            minimumSpend
        Minimal required spend to trigger offer.  Decimal format.

            rewardType
        `FIXED` or `PERCENTAGE`. 

            offerType
        `AFFILIATE`, `CARD_LINKED`, or `CATEGORICAL`.


        Returns
        -------
        An instance of `Offer`.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        spec = {
            'activation_required': activationRequired,
            'currency_code': currencyCode,
            'effective_date': effectiveDate,
            'external_id': externalID,
            'headline': headline,
            'marketing_fee_type': marketingFeeType,
            'minimum_spend': minimumSpend,
            'reward_type': rewardType,
            'offer_type': offerType,
            'activation_duration_in_days': activationDurationInDays,
            'campaign_ends_on': campaignEndsOn,
            'category': category,
            'category_tags': categoryTags,
            'description': description,
            'excluded_dates': excludedDates,
            'expiration_date': expirationDate,
            'marketing_fee_currency_code': marketingFeeCurrencyCode,
            'marketing_fee_rate': marketingFeeRate,
            'marketing_fee_value': marketingFeeValue,
            'max_redemptions': maxRedemptions,
            'maximum_cumulative_reward': maximumCumulativeReward,
            'maximum_reward_per_transaction': maximumRewardPerTransaction,
            'merchant_categories': merchantCategories,
            'merchant_external_id': merchantExternalID,
            'merchant_website': merchantWebsite,
            'mode': mode,
            'reward_rate': rewardRate,
            'reward_value': rewardValue,
            'terms': terms,
            'valid_day_parts': validDayParts,
        }
        return Offer(super().create(spec))


    @classmethod
    def byID(klass, objID: str) -> object:
        """
        Return an Offer object from provided extOfferID.
        """
        offer = super().byID(objID)
        return offer


    @classmethod
    def updateWith(klass, objID: str, spec: dict) -> object:
        """
        Allow content provider to update details of the Offer

        Arguments
        ---------
            externalID
        The Offer to be changed

            spec
        Dictionary providing the attribute to change and the new value


        Returns
        -------
            Offer
        Updated Offer object

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        offer = super().updateWith(objID,spec)
        if not offer:
            raise InvalidPayloadError('The specified Merchant cannot be found to update')
        return offer

    
    @classmethod
    def delete(klass, objID: str) -> object:
        """
        Allow content provider to soft-delete an Offer

        Arguments
        ---------
            externalID
        The Offer to be changed

        Returns
        -------
            status message 
        `The resource was deleted successfully.`
        

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """

        offer = super().delete(objID)
        return offer


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

