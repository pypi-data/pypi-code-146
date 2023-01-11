#!/usr/bin/env python
# -*- coding: utf-8 -*-

from comapsmarthome_public_api.comap_smart_home import ComapSmartHome


class ParkServiceClient(ComapSmartHome):
    service_url_suffix = "park"

    def get_housings(self):
        """Get a list of user's existing housings"""
        url = "{}/housings".format(self.base_url)
        return self.get_request(url=url, headers=self.request_header)

    def get_housing(self, housing_id):
        """Get housing details"""
        params = {"add_user_info": False}
        url = "{}/housings/{}".format(self.base_url, housing_id)
        return self.get_request(url=url, headers=self.request_header, params=params)

    def get_housing_connected_objects(self, housing_id):
        """Get a list of all objects in the specified housing"""
        url = "{}/housings/{}/connected-objects".format(self.base_url, housing_id)
        return self.get_request(url=url, headers=self.request_header)

    def get_connected_object(self, serial):
        """Get object details"""
        url = "{}/connected-objects/{}".format(self.base_url, serial)
        return self.get_request(url=url, headers=self.request_header)


if __name__ == '__main__':
    from comapsmarthome_public_api.client_auth import ClientAuth

    auth = ClientAuth()
    park = ParkServiceClient(auth)

    housings = park.get_housings()
