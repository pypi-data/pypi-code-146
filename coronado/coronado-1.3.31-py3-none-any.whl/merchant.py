# vim: set fileencoding=utf-8:


from coronado import TripleObject, TripleEnum
from coronado.address import Address, StrictAddress
from coronado.baseobjects import BASE_MID_DICT
from coronado.baseobjects import BASE_MERCHANT_DICT
from coronado.baseobjects import BASE_MERCHANT_LOCATION_DICT
from coronado.exceptions import InvalidPayloadError
from coronado.merchantcodes import MerchantCategoryCode

import json
import logging

# +++ constants +++

SERVICE_PATH = 'partner/merchants'
SERVICE_PATH_LOCATIONS = 'partner/merchant-locations'
"""
The default service path associated with Merchant operations.

Usage:

```python
Merchant.initialize(serviceURL, SERVICE_PATH, auth)
```

Users are welcome to initialize the class' service path from regular strings.
This constant is defined for convenience.
"""


# *** classes and objects ***


# --- globals ---

log = logging.getLogger(__name__)


class MidType(TripleEnum):
    """
    Availble Merchant ID Types
    """
    AMEX_SE_NUMBER = "AMEX_SE_NUMBER"
    DISCOVER_MID = "DISCOVER_MID"
    MC_AUTH_LOC_ID = "MC_AUTH_LOC_ID"
    MC_AUTH_ACQ_ID = "MC_AUTH_ACQ_ID"
    MC_AUTH_ICA = "MC_AUTH_ICA"
    MC_CLEARING_LOC_ID = "MC_CLEARING_LOC_ID"
    MC_CLEARING_ACQ_ID = "MC_CLEARING_ACQ_ID"
    MC_CLEARING_ICA = "MC_CLEARING_ICA"
    VISA_VMID = "VISA_VMID"
    VISA_VSID = "VISA_VSID"
    MERCHANT_PROCESSOR = "MERCHANT_PROCESSOR"
    NCR = "NCR"

class Mid(TripleObject):
    """
    A merchant ID and associated MidType
    """

    def __init__(self, obj = BASE_MID_DICT):
        """
        Create a new instance of a merchant ID.  `obj` must correspond to a
        valid, existing object ID if it's not a collection or JSON.

        Arguments
        ---------
            obj
        An object used for building a valid card program.  The object can
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


class MerchantLocation(TripleObject):
    """
    A merchant's business adddress, whether physical or on-line.

    See `coronado.address.Address`
    """

    requiredAttributes = [
        'isOnline',
        'parentMerchantExternalID',
        'processorMerchantIDs',
    ]

    def __init__(self, obj = BASE_MERCHANT_LOCATION_DICT):
        """
        Create a new instance of a merchant location.  `obj` must correspond to a
        valid, existing object ID if it's not a collection or JSON.

        Arguments
        ---------
            obj
        An object used for building a valid card program.  The object can
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
    def create(klass,
        extMerchantLocationID: str,
        isOnline: bool,
        parentMerchantExternalID: str,
        processorMerchantIDs: list[str],
        address: Address = None,
        email: str = None,
        locationName: str = None,
        locationWebsite: str = None,
        phoneNumber: str = None) -> object:
        """
        Creates a merchant location.

        For full details see `coronado.TripleObject.create()`.

        Arguments
        ---------
            extMerchantLocationID
        Partner provided external merchant location ID.

        External IDs are assumed to be stable and never **sensitive**.  External
        IDs need not be unique across publishers, but we encourage the use of
        UUIDs whenever possible.

        External IDs may not match the nnn-nn-nnnn format of US tax
        IDs to prevent accidental inclusion of sensitive information.

            isOnline
        Boolean value indicating whether the location is physical (False) or online (True).

            parentMerchantExternalID
        The external ID associated with the Merchant to which the location belongs.

            processorMerchantIDs
        Processor assigned merchant IDs.

            address
        Physical address of the location.  Optional, as online locations do not have a physical address.

            email
        Email address for the location.

            locationName
        Name of the location.  Optional, Merchant name will be used if not provided. 

            locationWebsite
        Website for the location.  Optional.

            phoneNumber
        Phone number for the location.  Optional.

        Returns
        -------
        An instance of `MerchantLocation`.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        
        spec = {
                'external_id': extMerchantLocationID,
                'is_online': isOnline,
                'parent_merchant_external_id': parentMerchantExternalID,
                'processor_merchant_ids': processorMerchantIDs,
                'address': address,
                'email': email,
                'location_name': locationName,
                'location_website': locationWebsite,
                'phone_number': phoneNumber,
            }
        
        #A location that is not online requires an address
        if not isOnline and not address:
            raise InvalidPayloadError('An address must be provided for an in person location.')

        #An online location requires a website
        if isOnline and not locationWebsite:
            raise InvalidPayloadError('A website must be provided for an online location.')

        
        if address:
            StrictAddress(address).validate()
            spec['address'] = address.asSnakeCaseDictionary()

        
        merchantLocation = MerchantLocation(super().create(spec))

        #Convert TripleObject to Address
        if merchantLocation.address:
            merchantLocation.address = Address(merchantLocation.address)

        #Convert TripleObject to Processor MIDs
        merchantLocation.processorMerchantIDs = [Mid(obj) for obj in merchantLocation.processorMerchantIDs] 

        return merchantLocation


    @classmethod
    def byID(klass, objID: str) -> object:
        """
        return a merchant location by the object internal ID
        """
        merchantLocation = super().byID(objID)
        if not merchantLocation:
            return None
        # Convert TripleObject to Address
        if merchantLocation.address:
            merchantLocation.address = Address(merchantLocation.address) 
        # Convert TripleObject to Processor MIDs
        merchantLocation.processorMerchantIDs = [Mid(obj) for obj in merchantLocation.processorMerchantIDs] 
        return merchantLocation


    @classmethod
    def updateWith(klass, objID: str, spec: dict) -> object:
        """
        updates a MerchantLocation
        """
        merchantLocation = super().updateWith(objID,spec)
        if not merchantLocation:
            raise InvalidPayloadError('The specified Merchant Location cannot be found to update')
        #Convert TripleObject to Address
        if merchantLocation.address:
            merchantLocation.address = Address(merchantLocation.address)
        # Convert TripleObject to MerchantCategoryCode
        merchantLocation.processorMerchantIDs = [Mid(obj) for obj in merchantLocation.processorMerchantIDs] 
        return merchantLocation


    @classmethod
    def list(klass, paramMap = None, **args) -> list:
        """
        Return a list of merchant locations.

        Arguments
        ---------
            extMerchantLocationID
        An external merchant location ID; optional

            page
        The page of results to return; optional

            pageSize
        The number of results to return per page; optional

            parentMerchantExternalID
        The external ID of the parent merchant object; optional


        Returns
        -------
            list
        A list of MerchantLocation objects

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        paramMap = {
            'extMerchantLocationID': 'merchant_location_external_id',
            'page': 'page',
            'pageSize': 'page_size',
            'parentMerchantExternalID': 'parent_merchant_external_id',
        }

        response = super().list(paramMap, **args)
        result = [ MerchantLocation(obj) for obj in json.loads(response.content)['locations'] ]

        return result

    @classmethod
    def delete(klass, objID: str) -> object:
        """
        return a merchant location by the object internal ID
        """
        successMsg = super().delete(objID)
        if not successMsg:
            raise InvalidPayloadError('No MerchantLocation to delete')
        
        return successMsg


class Merchant(TripleObject):
    """
    Merchant is a company or person involved in trade, most often retail, that
    processes card payments as a result of that trade.
    """
    requiredAttributes = [
        'address',
        'assumedName',
        'createdAt',
        'merchantCategory',
        'updatedAt',
    ]
    allAttributes = TripleObject(BASE_MERCHANT_DICT).listAttributes()


    def __init__(self, obj = BASE_MERCHANT_DICT):
        """
        Create a new Merchant instance.
        """
        TripleObject.__init__(self, obj)


    @classmethod
    def create(klass, 
                address: Address,
                assumedName: str,
                merchantCategoryCode: str,
                extMerchantID: str,
                logoURL: str = None) -> object:
        """
        Creates a merchant and returns an instance of the new object.

        Arguments
        ---------

            extMerchantID: str
        The external, non-triple merchant ID

            address: Address
        An instance of `coronado.address.Address` initialized to the merchant's
        physical address

            assumedName: str
        The merchant's assumed name

            logoURL: string
        A URL to the merchant's logo.

            merchantCategoryCode: MerchantCategoryCode
        The 4-digit standardized merchant category code (MCC).  See
        `coronado.merchantcodes.MerchantCategoryCode` for a full list.

        Returns
        -------

        An instance of `Merchant` if it was created by the triple back-end,, or
        `None`.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """

        StrictAddress(address).validate()

        spec = {
            'address': address.asSnakeCaseDictionary(),
            'assumed_name': assumedName,
            'external_id': extMerchantID,
            'logo_url': logoURL,
            'merchant_category_code': merchantCategoryCode,
        }
        merchant = super().create(spec)
        #Convert TripleObject to Address
        merchant.address = Address(merchant.address) 
        #Convert TripleObject to MerchantCategoryCode
        merchant.merchantCategory = MerchantCategoryCode(merchant.merchantCategory) 
        return merchant
        #return Merchant(super().create(spec))

    @classmethod
    def list(klass: object, paramMap = None, **args) -> list:
        """
        List all merchants that match any of the criteria set by the
        arguments to this method.

        Arguments
        ---------
            externalMerchantID
        String, 1-50 characters partner-provided external ID

        Returns
        -------
            list
        A list of Merchant objects; can be `None`.
        """
        paramMap = {
            'externalMerchantID': 'merchant_external_id',
            'page': 'page',
            'pageSize': 'page_size',
        }
        response = super().list(paramMap, **args)
        result = [ Merchant(obj) for obj in json.loads(response.content)['merchants'] ]
        return result


    @classmethod
    def byID(klass, objID: str) -> object:
        merchant = super().byID(objID)
        # Convert TripleObject to Address
        if not merchant:
            return None
        merchant.address = Address(merchant.address) 
        # Convert TripleObject to MerchantCategoryCode
        merchant.merchantCategory = MerchantCategoryCode(merchant.merchantCategory) 
        return merchant


    @classmethod
    def updateWith(klass, objID : str, spec : dict) -> object:
        merchant = super().updateWith(objID,spec)
        if not merchant:
            raise InvalidPayloadError('The specified Merchant cannot be found to update')
        # Convert TripleObject to Address
        merchant.address = Address(merchant.address) 
        # Convert TripleObject to MerchantCategoryCode
        merchant.merchantCategory = MerchantCategoryCode(merchant.merchantCategory) 
        return merchant


    @classmethod
    def delete(klass, objID: str) -> object:
        """
        delete merchant, identified by internal ID
        """
        successMsg = super().delete(objID)
        if not successMsg:
            raise InvalidPayloadError('No Merchant to delete')
        
        return successMsg

