#!/usr/bin/env python
# -*- coding: utf-8 -*-

from comapsmarthome_public_api.comap_smart_home import ComapSmartHome


class UserService(ComapSmartHome):
    service_url_suffix = "user"

    def get_user(self, user_id):
        """Get user information"""
        url = "{}/users/{}".format(self.base_url, user_id)
        return self.get_request(url=url, headers=self.request_header)

    def update_user(self, user_id, user):
        """Update user information"""
        url = "{}/users/{}".format(self.base_url, user_id)
        return self.patch_request(url=url, headers=self.request_header, data=user)

    def change_password(self, user_id, password):
        """Change password"""
        data = {"password": password}
        url = "{}/users/{}/password".format(self.base_url, user_id)
        return self.put_request(url=url, headers=self.request_header, data=data)

    def reset_password(self, username):
        """Reset password"""
        data = {"username": username}
        url = "{}/users/password/reset".format(self.base_url)
        return self.post_request(url=url, headers=self.request_header, data=data)


if __name__ == '__main__':
    from comapsmarthome_public_api.client_auth import ClientAuth

    user_id = 'USER_ID'

    auth = ClientAuth()
    user_service = UserService(auth)

    user = user_service.get_user(user_id=user_id)
