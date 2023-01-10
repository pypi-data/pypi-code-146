import googlemaps

from . import Geocode, Geotype, Location, Point, Viewport


class Client(googlemaps.Client):
    """Extend the Google Maps Client to format the response in a more usable format, which only
    includes data we care about, namely the viewport and the location type.
    """

    def geocode(self, search, country=None):
        """Force the search query to use the ISO country code as a component filter, to ensure the
        results are biased towards the country we know we are looking in.

        Returns a Geocode instance.
        """
        try:
            if country:
                response = super(Client, self).geocode(
                    search, components={"country": country}
                )
            else:
                response = super(Client, self).geocode(search)
        except googlemaps.exceptions.TransportError:
            # This exception is known to be raised when the connection is severed, which will
            # happen if the publication takes too long and the job gets killed.
            # When that happens, we just return None and move on, silencing the error.
            return None

        if not response:
            return None

        result = response[0]
        geotype = Geotype[result["geometry"]["location_type"]]
        southwest = Point(
            latitude=result["geometry"]["viewport"]["southwest"]["lat"],
            longitude=result["geometry"]["viewport"]["southwest"]["lng"],
        )
        northeast = Point(
            latitude=result["geometry"]["viewport"]["northeast"]["lat"],
            longitude=result["geometry"]["viewport"]["northeast"]["lng"],
        )
        viewport = Viewport(southwest=southwest, northeast=northeast)

        return Geocode(
            location=result.get("formatted_address", "N/A"),
            location_type=geotype,
            viewport=viewport,
        )

    def reverse_geocode(self, latlon):
        """Reverse-geocode the given latlon pair.

        The pair is provided as a (lat, lon) tuple.

        Returns a Geocode instance.
        Raise ValueError on failure.
        """
        try:
            response = super(Client, self).reverse_geocode(latlon)
        except googlemaps.exceptions.TransportError:
            # This exception is known to be raised when the connection is severed, which will
            # happen if the publication takes too long and the job gets killed.
            # When that happens, we just return None and move on, silencing the error.
            return None

        if not response:
            return None

        try:
            area = self._lookup("administrative_area_level_2", response)["long_name"]
            country = self._lookup("country", response)["short_name"]
            postal_code = self._lookup("postal_code", response)["long_name"]
            postal_town = self._lookup("postal_town", response)["long_name"]
        except ValueError as e:
            raise ValueError(f'Failed to resolve {latlon} - "{e}"')

        return Location(
            city=postal_town,
            country=country,
            formatted_address=response[0]["formatted_address"],
            place_id=response[0]["place_id"],
            postcode=postal_code,
            region=area,
        )

    def _lookup(self, field, response):
        """Loop through all addresses in the response to find the field we are after.

        When all fails, raise a ValueError.
        """
        for result in response:
            try:
                return [
                    address_component
                    for address_component in result["address_components"]
                    if field in address_component["types"]
                ][0]
            except IndexError:
                continue

        raise ValueError(field)
