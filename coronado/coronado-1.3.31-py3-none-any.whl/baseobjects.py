# vim: set fileencoding=utf-8:


import json


# If you copy/paste the JSON spec here, remember to escape the \n to prevent
# JSON parser errros.
# Notes:


# * See ISO-3166-2 for country subdivision codes; can be 2 or more letters
# * Street address became a multi-line field, free form
# * The complete address is optional AND assembled by the implementing classes,
#   not by the service
BASE_ADDRESS_JSON = """
{
    "city": "PITTSBURGH",
    "country_code": "US",
    "country_subdivision_code": "PA",
    "latitude": 40.440624,
    "longitude": -79.995888,
    "postal_code": "15206",
    "street_address": "7370 BAKER ST\\nSUITE 42"
}
"""
"""
Base Address object specification, from the triple API JSON payload.
"""

"""
Base Address object specification, a `dict` representation of the triple API
JSON payload.
"""
BASE_ADDRESS_DICT = json.loads(BASE_ADDRESS_JSON)


BASE_CARD_ACCOUNT_JSON = """
{
  "id": "triple-abc-123",
  "card_program_id": "triple-abc-123",
  "created_at": "2021-12-01T01:59:59.000Z",
  "default_country_code": "US",
  "default_postal_code": "15206",
  "external_id": "string",
  "status": "ENROLLED",
  "updated_at": "2021-12-01T01:59:59.000Z"
}
"""
BASE_CARD_ACCOUNT_DICT = json.loads(BASE_CARD_ACCOUNT_JSON)


BASE_CARD_ACCOUNT_IDENTIFIER_JSON = """{
  "publisher_external_id": "string",
  "card_program_external_id": "string",
  "external_id": "string",
  "status": "ENROLLED"
}"""
BASE_CARD_ACCOUNT_IDENTIFIER_DICT = json.loads(BASE_CARD_ACCOUNT_IDENTIFIER_JSON)


BASE_CARD_PROGRAM_JSON = """
{
  "id": "triple-abc-123",
  "card_bins": [
    "444789"
  ],
  "created_at": "2021-12-01T01:59:59.000Z",
  "default_country_code": "US",
  "default_postal_code": "15206",
  "description": "string",
  "loyalty_unit": "POINTS",
  "loyalty_conversion_rate": 100,
  "external_id": "string",
  "loyalty_unit": "POINTS",
  "loyalty_conversion_rate": "100",
  "name": "string",
  "program_currency": "USD",
  "publisher_id": "triple-abc-123",
  "updated_at": "2021-12-01T01:59:59.000Z"
}
"""
BASE_CARD_PROGRAM_DICT = json.loads(BASE_CARD_PROGRAM_JSON)


BASE_HEALTHCHECK_JSON = """
{
    "api_version": "0.0.0",
    "build": "blah-xxx-yyyy-nnnn"
}
"""
BASE_HEALTHCHECK_DICT = json.loads(BASE_HEALTHCHECK_JSON)


BASE_MERCHANT_CATEGORY_CODE_JSON = """{
    "code": "7998",
    "description": "Aquaria, Dolphinaria, Seaquaria, and Zoos"
}"""
BASE_MERCHANT_CATEGORY_CODE_DICT = json.loads(BASE_MERCHANT_CATEGORY_CODE_JSON)


BASE_MID_JSON = """{
    "mid": "string",
    "mid_type": "VISA_VMID"
}"""
BASE_MID_DICT = json.loads(BASE_MID_JSON)


BASE_MERCHANT_JSON = """
{
  "address": {
    "city": "PITTSBURGH",
    "complete": "7370 BAKER ST, STE 100\\nPITTSBURGH, PA 15206",
    "country_code": "US",
    "country_subdivision_code": "PA",
    "latitude": 40.440624,
    "longitude": -79.995888,
    "postal_code": "15206",
    "street_address": "7370 BAKER ST, STE 100\\n"
  },
  "assumed_name": "string",
  "created_at": "2021-12-01T01:59:59.000Z",
  "external_id": "string",
  "id": "triple-abc-123",
  "logo_url": "string",
  "merchant_category": {
    "code": "7998",
    "description": "Aquariums, Dolphinariums, Seaquariums, and Zoos"
  },
  "updated_at": "2021-12-01T01:59:59.000Z"
}
"""
BASE_MERCHANT_DICT = json.loads(BASE_MERCHANT_JSON)


BASE_MERCHANT_LOCATION_JSON = """{
  "address": {
    "city": "PITTSBURGH",
    "country_code": "US",
    "country_subdivision_code": "PA",
    "latitude": 40.440624,
    "longitude": -79.995888,
    "postal_code": "15206",
    "street_address": "7370 BAKER ST\\nSUITE 42"
    },
  "email": "string",
  "external_id": "triple-abc-123",
  "id": "123",
  "is_online": true,
  "location_name": "string",
  "location_website": "string",
  "phone_number": "string",
  "processor_merchant_ids": [{
    "mid": "string",
    "mid_type": "DISCOVER_MID"
    }],
  "parent_merchant_external_id": "123"
}
"""
BASE_MERCHANT_LOCATION_DICT = json.loads(BASE_MERCHANT_LOCATION_JSON)


BASE_OFFER_JSON = """
{
  "activation_duration_in_days": 0,
  "activation_required": true,
  "category": "AUTOMOTIVE",
  "category_tags": "string",
  "currency_code": "USD",
  "description": "string",
  "effective_date": "2021-12-01",
  "excluded_dates": [
    "2021-12-25"
  ],
  "expiration_date": "2021-12-31",
  "external_id": "string",
  "headline": "string",
  "id": "triple-abc-123",
  "is_activated": false,
  "marketing_fee": 0,
  "marketing_fee_currency_code": "USD",
  "marketing_fee_type": "FIXED",
  "max_redemptions": "1/3M",
  "maximum_reward_cumulative": 0,
  "maximum_reward_per_transaction": 0,
  "merchant_category": [
    {
      "code": "7998",
      "description": "Aquariums, Dolphinariums, Seaquariums, and Zoos"
    }
  ],
  "merchant_id": "triple-abc-123",
  "merchant_website": "string",
  "minimum_spend": 0,
  "offer_mode": "ONLINE",
  "reward_rate": 0,
  "reward_type": "FIXED",
  "reward_value": 0,
  "terms_and_conditions": "string",
  "type": "CARD_LINKED",
  "valid_day_parts": {
    "sunday": {
      "times": [
        "00:30-13:30"
      ]
    },
    "monday": {
      "times": [
        "00:30-13:30"
      ]
    },
    "tuesday": {
      "times": [
        "00:30-13:30"
      ]
    },
    "wednesday": {
      "times": [
        "00:30-13:30"
      ]
    },
    "thursday": {
      "times": [
        "00:30-13:30"
      ]
    },
    "friday": {
      "times": [
        "00:30-13:30"
      ]
    },
    "saturday": {
      "times": [
        "00:30-13:30"
      ]
    }
  },
  "logo_url": "string"
}
"""
BASE_OFFER_DICT = json.loads(BASE_OFFER_JSON)


BASE_CARDHOLDER_OFFER_DETAILS_JSON = """
{
  "offer": {
    "id": "triple-abc-123",
    "activation_required": true,
    "activation_duration_in_days": 0,
    "activate_at": "2022-07-15T15:56:36+0000",
    "activation_expires_on": "2022-07-15T15:56:36+0000",
    "category": "AUTOMOTIVE",
    "category_tags": "string",
    "currency_code": "USD",
    "description": "string",
    "effective_date": "2021-12-01",
    "excluded_dates": [
      "2021-12-25"
    ],
    "expiration_date": "2021-12-31",
    "headline": "string",
    "is_activated": false,
    "max_redemptions": "1/3M",
    "maximum_reward_cumulative": 0,
    "maximum_reward_per_transaction": 0,
    "merchant_category": {
      "code": "7998",
      "description": "Aquariums, Dolphinariums, Seaquariums, and Zoos"
    },
    "merchant_id": "triple-abc-4269",
    "merchant_name": "string",
    "merchant_logo_url": "string",
    "merchant_website": "string",
    "minimum_spend": 0,
    "offer_mode": "ONLINE",
    "reward_rate": 0,
    "reward_type": "FIXED",
    "reward_value": 0,
    "terms_and_conditions": "string",
    "type": "CARD_LINKED",
    "valid_day_parts": {
      "sunday": {
        "times": [
          "00:30-13:30"
        ]
      },
      "monday": {
        "times": [
          "00:30-13:30"
        ]
      },
      "tuesday": {
        "times": [
          "00:30-13:30"
        ]
      },
      "wednesday": {
        "times": [
          "00:30-13:30"
        ]
      },
      "thursday": {
        "times": [
          "00:30-13:30"
        ]
      },
      "friday": {
        "times": [
          "00:30-13:30"
        ]
      },
      "saturday": {
        "times": [
          "00:30-13:30"
        ]
      }
    }
  },
  "merchant_locations": [
    {
      "id": "triple-abc-123",
      "location_name": "string",
      "is_online": true,
      "email": "string",
      "phone_number": "string",
      "address": {
            "city": "PITTSBURGH",
            "country_code": "US",
            "country_subdivision_code": "PA",
            "latitude": 40.440624,
            "longitude": -79.995888,
            "postal_code": "15206",
            "street_address": "7370 BAKER ST\\nSUITE 42"
      }
    }
  ]
}
"""
BASE_CARDHOLDER_OFFER_DETAILS_DICT = json.loads(BASE_CARDHOLDER_OFFER_DETAILS_JSON)


BASE_OFFER_SEARCH_RESULT_JSON = """
{
  "activation_required": true,
  "external_id": "string",
  "category": "AUTOMOTIVE",
  "category_tags": "string",
  "currency_code": "USD",
  "effective_date": "2021-12-01",
  "expiration_date": "2021-12-31",
  "headline": "string",
  "id": "triple-abc-123",
  "is_activated": true,
  "max_redemptions": "1/3M",
  "maximum_reward_per_transaction": 0,
  "merchant_id": "triple-abc-123",
  "merchant_logo_url": "string",
  "merchant_name": "string",
  "merchant_website": "string",
  "minimum_spend": 0,
  "nearest_location": {
    "address": {
      "city": "PITTSBURGH",
      "complete": "7370 BAKER ST, STE 100\\nPITTSBURGH, PA 15206",
      "country_code": "US",
      "country_subdivision_code": "PA",
      "latitude": 40.440624,
      "longitude": -79.995888,
      "postal_code": "15206",
      "street_address": "7370 BAKER ST, STE 100\\n"
    },
    "id": "triple-abc-123",
    "is_in_radius": true,
    "location_name": "Peter Piper's Pizza - South Evermore",
    "url": "string"
  },
  "offer_mode": "ONLINE",
  "reward_rate": 0,
  "reward_type": "FIXED",
  "reward_value": 0,
  "score": 0,
  "type": "CARD_LINKED"
}
"""
BASE_OFFER_SEARCH_RESULT_DICT = json.loads(BASE_OFFER_SEARCH_RESULT_JSON)


BASE_CARDHOLDER_OFFER_LOCATION_JSON = """{
    "id": "triple-abc-123",
    "location_name": "string",
    "is_online": true,
    "email": "string",
    "phone_number": "string",
    "address": {
        "city": "PITTSBURGH",
        "country_code": "US",
        "country_subdivision_code": "PA",
        "latitude": 40.440624,
        "longitude": -79.995888,
        "postal_code": "15206",
        "street_address": "7370 BAKER ST\\nSUITE 42"
    }
}"""
BASE_CARDHOLDER_OFFER_LOCATION_DICT = json.loads(BASE_CARDHOLDER_OFFER_LOCATION_JSON)


BASE_OFFER_DISPLAY_RULES_JSON = """{ "id": "triple-abc-123",
    "description": "string",
    "enabled": true,
    "scope":
    {

        "level": "PORTFOLIO_MANAGER",
        "id": "triple-abc-123",
        "name": "string"

    },
    "type": "MERCHANT_NAME_EQUAL_TO",
    "value": "string",
    "action": "EXCLUDE"
}"""
BASE_OFFER_DISPLAY_RULES_DICT = json.loads(BASE_OFFER_DISPLAY_RULES_JSON)


BASE_PUBLISHER_JSON = """{
  "id": "triple-abc-123",
  "portfolio_manager_id": "triple-abc-123",
  "external_id": "string",
  "assumed_name": "string",
  "address": {
    "city": "PITTSBURGH",
    "complete": "7370 BAKER ST, STE 100\\nPITTSBURGH, PA 15206",
    "country_code": "US",
    "country_subdivision_code": "PA",
    "latitude": 40.440624,
    "longitude": -79.995888,
    "postal_code": "15206",
    "street_address": "7370 BAKER ST, STE 100\\n"
  },
  "revenue_share": 1.125,
  "created_at": "2021-12-01T01:59:59.000Z",
  "updated_at": "2021-12-01T01:59:59.000Z"
}"""
BASE_PUBLISHER_DICT = json.loads(BASE_PUBLISHER_JSON)


BASE_REWARD_JSON = """
{
  "card_bin": "444789",
  "card_last_4": "0001",
  "merchant_name": "string",
  "merchant_complete_address": "7370 BAKER ST, STE 100\\nPITTSBURGH, PA 15206",
  "offer_external_id": "string",
  "offer_headline": "string",
  "offer_id": "triple-abc-123",
  "reward_amount": 0,
  "reward_currency_code": "USD",
  "status": "REJECTED",
  "transaction_amount": 12,
  "transaction_currency_code": "USD",
  "transaction_timestamp": "2022-05-31T15:34:22-0400",
  "transaction_id": "triple-abc-123"
}
"""
BASE_REWARD_DICT = json.loads(BASE_REWARD_JSON)


BASE_TRANSACTION_JSON = """
{
  "amount": 12,
  "card_account_id": "triple-abc-123",
  "card_bin": "000001",
  "card_last_4": "1234",
  "created_at": "2021-12-01T01:59:59.000Z",
  "currency_code": "USD",
  "debit": true,
  "description": "Pittsburgh Zoo",
  "external_id": "string",
  "id": "triple-abc-123",
  "matching_status": "HISTORIC_TRANSACTION",
  "merchant_address": {
    "city": "PITTSBURGH",
    "complete": "7370 BAKER ST, STE 100\\nPITTSBURGH, PA 15206",
    "country_code": "US",
    "country_subdivision_code": "PA",
    "latitude": 40.440624,
    "longitude": -79.995888,
    "postal_code": "15206",
    "street_address": "7370 BAKER ST, STE 100\\n"
  },
  "merchant_category": {
    "code": "7998",
    "description": "Aquariums, Dolphinariums, Seaquariums, and Zoos"
  },
  "processor_mid": "9000012345",
  "processor_mid_type": "VISA_VMID",
  "reward_details": [
    {
      "amount": 0,
      "currency_code": "USD",
      "notes": "string",
      "offer_id": "triple-abc-123",
      "rejection": "PURCHASE_AMOUNT_TOO_LOW",
      "status": "REJECTED"
    }
  ],
  "timestamp": "2021-12-01T01:59:59.000Z",
  "transaction_type": "PURCHASE",
  "updated_at": "2021-12-01T01:59:59.000Z"
}
"""
BASE_TRANSACTION_DICT = json.loads(BASE_TRANSACTION_JSON)

