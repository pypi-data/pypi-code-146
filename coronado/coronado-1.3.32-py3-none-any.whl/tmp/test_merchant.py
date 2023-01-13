import uuid
import pytest

from coronado import TripleObject
from coronado.address import Address
from coronado.auth import Auth, loadConfig
from coronado.exceptions import CallError, InvalidPayloadError
from coronado.merchant import Merchant, MerchantLocation, Mid, MidType, SERVICE_PATH, SERVICE_PATH_LOCATIONS
from tests.test_address import _ADDRESS


# *** globals ***

_config = loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])
_merchant = None

Merchant.initialize(_config['serviceURL'], SERVICE_PATH, _auth)
MerchantLocation.initialize(_config['serviceURL'], SERVICE_PATH_LOCATIONS, _auth)

testAddress = Address({
    'city': 'Austin',
    'countryCode': 'US',
    'countrySubdivisionCode': 'TX',
    'latitude': '',
    'longitude': '',
    'postalCode': '78702',
    'streetAddress': '12754 W Union Way',
})

# +++ tests +++


def test_Merchant_create():
    global _merchant

    # Happy path test
    merchant = Merchant.create(
        extMerchantID = uuid.uuid4().hex,
        address = testAddress,
        assumedName = 'Walmart Stores %s' % uuid.uuid4().hex,
        logoURL = 'https://cime.net/images/CIMEwhite-logo.png',
        merchantCategoryCode = '7998')
    assert isinstance(merchant, Merchant)
    _merchant = merchant # For later use

    # Remove the logo URL, should create a new item fine:
    merchant = Merchant.create(
        extMerchantID = uuid.uuid4().hex,
        address = testAddress,
        assumedName = 'Walmart Stores %s' % uuid.uuid4().hex,
        merchantCategoryCode = '7998')
    assert isinstance(merchant, Merchant)

    # Remove a required field - I think this is supposed to return a CallError
    with pytest.raises(TypeError):
        Merchant.create(
            extMerchantID = uuid.uuid4().hex,
            assumedName = 'Walmart Stores %s' % uuid.uuid4().hex,
            logoURL = 'https://cime.net/images/CIMEwhite-logo.png',
            merchantCategoryCode = '7998')

    # Give an invalid MCC:
    with pytest.raises(CallError):
        merchant = Merchant.create(
            extMerchantID = uuid.uuid4().hex,
            address = testAddress,
            assumedName = 'Walmart Stores %s' % uuid.uuid4().hex,
            merchantCategoryCode = "XXXX")

    # Test that StrictAddress raises error with invalid inputs
    testAddress.postalCode = ''
    with pytest.raises(InvalidPayloadError):
        merchant = Merchant.create(
            extMerchantID = uuid.uuid4().hex,
            address = testAddress,
            assumedName = 'Walmart Stores %s' % uuid.uuid4().hex,
            merchantCategoryCode = "7998")

    testAddress.postalCode = '123456789123456789'
    with pytest.raises(InvalidPayloadError):
        merchant = Merchant.create(
            extMerchantID = uuid.uuid4().hex,
            address = testAddress,
            assumedName = 'Walmart Stores %s' % uuid.uuid4().hex,
            merchantCategoryCode = "7998")

    #reset
    testAddress.postalCode = '78702'
    testAddress.countryCode = ''
    with pytest.raises(InvalidPayloadError):
        merchant = Merchant.create(
            extMerchantID = uuid.uuid4().hex,
            address = testAddress,
            assumedName = 'Walmart Stores %s' % uuid.uuid4().hex,
            merchantCategoryCode = "7998")

    testAddress.countryCode = 'USA'
    with pytest.raises(InvalidPayloadError):
        merchant = Merchant.create(
            extMerchantID = uuid.uuid4().hex,
            address = testAddress,
            assumedName = 'Walmart Stores %s' % uuid.uuid4().hex,
            merchantCategoryCode = "7998")

    #reset
    testAddress.countryCode = 'US'
    testAddress.streetAddress = ''
    with pytest.raises(InvalidPayloadError):
        merchant = Merchant.create(
            extMerchantID = uuid.uuid4().hex,
            address = testAddress,
            assumedName = 'Walmart Stores %s' % uuid.uuid4().hex,
            merchantCategoryCode = "7998")

    #reset
    testAddress.streetAddress = '12754 W Union Way'


def test_Merchant_list():
    merchants = Merchant.list()

    assert isinstance(merchants, list)

    if len(merchants):
        merchant = merchants[0]
        assert isinstance(merchant, TripleObject)
        assert merchant.objID

    #Test with a specific ID to verify the list method works with limited scope
    merchants = Merchant.list(externalMerchantID = _merchant.externalID)
    assert isinstance(merchants,list)
    assert len(merchants) == 1

    #Test some non-existent IDs
    assert not Merchant.list(externalMerchantID = 'not_real')

#     merchants = Merchant.list(cardAccountExternalID = KNOWN_CARD_ACCT_EXT_ID)
#     assert merchants[0].matchingStatus == MatchingStatus.NO_ACTIVE_OFFER
#
#     merchants = Merchant.list(cardProgramExternalID = KNOWN_CARD_PROG_EXT_ID)
#     assert merchants[0].matchingStatus == MatchingStatus.NO_ACTIVE_OFFER
#
#     # TODO:  Not implemented, no end dates known
# #     merchants = Merchant.list(endDate = KNOWN_CARD_PROG_EXT_ID)
# #     assert merchants[0].matchingStatus == MatchingStatus.NO_ACTIVE_OFFER
#
#     merchants = Merchant.list(matched = True)
#     if len(merchants):
#         assert merchants[0].matchingStatus == MatchingStatus.NO_ACTIVE_OFFER
#
#     merchants = Merchant.list(matched = False)
#     if len(merchants):
#         assert merchants[0].matchingStatus == MatchingStatus.NO_ACTIVE_OFFER
#
#     # TODO:  Not implemented, no start dates known
# #     merchants = Merchant.list(startDate = KNOWN_CARD_PROG_EXT_ID)
# #     assert merchants[0].matchingStatus == MatchingStatus.NO_ACTIVE_OFFER
#
#     merchants = Merchant.list(transactionExternalID = KNOWN_TRANSACTION_EXTERNAL_ID)
#     assert merchants[0].matchingStatus == MatchingStatus.NO_ACTIVE_OFFER


def test_Merchant_byID():
    result = Merchant.byID(_merchant.objID)
    assert isinstance(result, Merchant)

    assert not Merchant.byID({ 'bogus': 'test'})
    assert not Merchant.byID(None)
    assert not Merchant.byID('bogus')


def test_Merchant_update():
    merchant = Merchant.byID(_merchant.objID)
    merchName = merchant.assumedName
    payload = { 'assumed_name' : 'new_name', }
    result = Merchant.updateWith(_merchant.objID, payload)
    assert result.assumedName == 'new_name'
    # Reset:
    payload['assumed_name'] = merchName
    Merchant.updateWith(_merchant.objID, payload)

    #Tests that an error is returned by triple when ID does not exist
    payload = { 'assumed_name' : 'new_name', }
    with pytest.raises(InvalidPayloadError):
        result = Merchant.updateWith('this_id_does_not_exist', payload)

    #Tests changing a nested address parameter
    merchant = Merchant.byID(_merchant.objID)
    merchPostalCode = merchant.address.postalCode

    payload = {
        'address': {'postal_code': '15212',},
    }
    result = Merchant.updateWith(_merchant.objID, payload)
    assert result.address.postalCode == '15212'

    # Reset:
    payload['address']['postal_code'] = merchPostalCode
    Merchant.updateWith(_merchant.objID, payload)


def test_Mid():

    testMid = Mid({'mid':'123', 'midType':'VISA_VMID'})
    assert isinstance(testMid, Mid)


def test_MerchantLocation_create():
    global _merchantLocation
    # Happy path test for in person location
    testMidStr = {'mid':'123', 'mid_type':'VISA_VMID'}
    merchantLocation = MerchantLocation.create(
        extMerchantLocationID = uuid.uuid4().hex,
        isOnline = False,
        parentMerchantExternalID = '19113',
        processorMerchantIDs = [testMidStr],
        address = testAddress
    )
    assert isinstance(merchantLocation, MerchantLocation)

    #Create location including all optional fields
    testMidStr2 = {'mid':'234','mid_type':'VISA_VMID'}
    merchantLocation = MerchantLocation.create(
        extMerchantLocationID = uuid.uuid4().hex,
        isOnline = False,
        parentMerchantExternalID = '19113',
        processorMerchantIDs = [testMidStr,testMidStr2],
        address = testAddress,
        email = 'bogus@bogus.com',
        locationName = 'Site ABC',
        locationWebsite = 'https://www.URLforMerchantLocation.com',
        phoneNumber = '412-867-5309'
    )
    assert isinstance(merchantLocation, MerchantLocation)
    _merchantLocation = merchantLocation # For later use

    # Online location with address
    merchantLocation = MerchantLocation.create(
        extMerchantLocationID = uuid.uuid4().hex,
        isOnline = True,
        parentMerchantExternalID = '19113',
        processorMerchantIDs = [testMidStr],
        address = testAddress,
        locationWebsite = 'https://www.URLforMerchantLocation.com'
    )
    assert isinstance(merchantLocation, MerchantLocation)

    # Online location without address
    merchantLocation = MerchantLocation.create(
        extMerchantLocationID = uuid.uuid4().hex,
        isOnline = True,
        parentMerchantExternalID = '19113',
        processorMerchantIDs = [testMidStr],
        locationWebsite = 'https://www.URLforMerchantLocation.com'
    )
    assert isinstance(merchantLocation, MerchantLocation)

    #InvalidPayloadError for in person merchant location with no Address
    with pytest.raises(InvalidPayloadError):
        MerchantLocation.create(
            extMerchantLocationID = uuid.uuid4().hex,
            isOnline = False,
            parentMerchantExternalID = '19113',
            processorMerchantIDs = [testMidStr]
        )

    #InvalidPayloadError for online merchant location with no website
    with pytest.raises(InvalidPayloadError):
        MerchantLocation.create(
            extMerchantLocationID = uuid.uuid4().hex,
            isOnline = True,
            parentMerchantExternalID = '19113',
            processorMerchantIDs = [testMidStr]
        )


def test_MerchantLocation_list():
    merchantLocations = MerchantLocation.list()

    assert isinstance(merchantLocations, list)

    if len(merchantLocations):
        merchantLocation = merchantLocations[0]
        assert isinstance(merchantLocation, TripleObject)
        assert merchantLocation.objID

    #Test with a specific ID to verify the list method works with limited scope
    merchantLocations = MerchantLocation.list(extMerchantLocationID = _merchantLocation.externalID)
    assert isinstance(merchantLocations, list)
    assert len(merchantLocations) == 1

    merchantLocations = MerchantLocation.list(parentMerchantExternalID = _merchantLocation.parentMerchantExternalID)
    assert isinstance(merchantLocations, list)
    assert len(merchantLocations)

    merchantLocations = MerchantLocation.list(parentMerchantExternalID = _merchantLocation.parentMerchantExternalID, page = 1, pageSize = 3)
    assert isinstance(merchantLocations, list)
    assert len(merchantLocations) <= 3


    #Test some non-existent ID
    assert not MerchantLocation.list(extMerchantLocationID = 'not_real')


def test_MerchantLocation_byID():
    result = MerchantLocation.byID(_merchantLocation.objID)
    assert isinstance(result, MerchantLocation)

    assert not MerchantLocation.byID({ 'bogus': 'test'})
    assert not MerchantLocation.byID(None)
    assert not MerchantLocation.byID('bogus')


def test_MerchantLocation_update():
    merchantLocation = MerchantLocation.byID(_merchantLocation.objID)
    locName = merchantLocation.locationName
    payload = { 'location_name' : 'new_name', }
    result = MerchantLocation.updateWith(_merchantLocation.objID, payload)
    assert result.locationName == 'new_name'
    # Reset:
    payload['location_name'] = locName
    MerchantLocation.updateWith(_merchantLocation.objID, payload)

    #Tests that an error is returned by triple when ID does not exist
    payload = { 'location_name' : 'new_name', }
    with pytest.raises(InvalidPayloadError):
        result = MerchantLocation.updateWith('this_id_does_not_exist', payload)


def test_merchantLocation_delete():
    msg = MerchantLocation.delete(_merchantLocation.objID)
    assert msg == 'The resource was deleted successfully.'

    #TODO: Uncomment when fixed.  Delete of non-existent MerchantLocation returns success message.
    #with pytest.raises(InvalidPayloadError):
    #    MerchantLocation.delete('bogus')

