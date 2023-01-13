import os

import googlemaps

from utils import timex
from utils.cache import cache

CACHE_NAME, CACHE_TIMEOUT = 'GoogleMaps', timex.SECONDS_IN.YEAR


def get_api_key():
    return os.environ['GOOGLE_API_KEY']


class GoogleMaps:
    def __init__(self):
        gmaps_api_key = get_api_key()
        self.api = googlemaps.Client(key=gmaps_api_key)

    def __get_geocode__(self, address):
        @cache(CACHE_NAME, CACHE_TIMEOUT)
        def get_geocode_inner(address):
            return self.api.geocode(address)

        return get_geocode_inner(address)

    def __get_reverse_geocode__(self, latlng):
        @cache(CACHE_NAME, CACHE_TIMEOUT)
        def get_reverse_geocode_inner(latlng):
            return self.api.reverse_geocode(latlng)

        return get_reverse_geocode_inner(latlng)

    def get_latlng(self, address):
        geocode = self.__get_geocode__(address)
        location = geocode[0]['geometry']['location']
        return [location['lat'], location['lng']]

    def get_address(self, latlng):
        rev_geocode = self.__get_reverse_geocode__(latlng)
        return rev_geocode[0]['formatted_address']

    def get_address_details(self, latlng):
        rev_geocode = self.__get_reverse_geocode__(latlng)
        if not rev_geocode:
            return None
        first_rev_geocode_item = rev_geocode[0]

        street_number = None
        street = None
        sub_city = None
        city = None
        postal_code = None
        district = None
        country = None
        plus_code = None

        for ac in first_rev_geocode_item['address_components']:
            ac_types = ac['types']
            if 'street_number' in ac_types:
                street_number = ac['long_name']
            if 'route' in ac_types:
                street = ac['long_name']
            if 'sublocality' in ac_types:
                sub_city = ac['long_name']
            if 'locality' in ac_types:
                city = ac['long_name']
            if 'postal_code' in ac_types:
                postal_code = ac['long_name']

            if 'administrative_area_level_2' in ac_types:
                district = ac['long_name']
            if 'administrative_area_level_1' in ac_types:
                province = ac['long_name']
            if 'country' in ac_types:
                country = ac['long_name']

            if 'plus_code' in ac_types:
                plus_code = ac['long_name']

        details = dict(
            street_number=street_number,
            plus_code=plus_code,
            street=street,
            sub_city=sub_city,
            city=city,
            postal_code=postal_code,
            district=district,
            province=province,
            country=country,
            formatted_address=first_rev_geocode_item['formatted_address'],
        )
        return details
