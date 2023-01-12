# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import json


class ProviderInfo:
    def __init__(self, provider_id=None, raw_id=None, photo_url=None,
                 display_name=None, open_id=None):
        self.provider_id = provider_id
        self.raw_id = raw_id
        self.photo_url = photo_url
        self.display_name = display_name
        self.open_id = open_id

    def get_provider_id(self):
        return self.provider_id

    def set_provider_id(self, provider_id: str):
        self.provider_id = provider_id

    def get_raw_id(self):
        return self.raw_id

    def set_raw_id(self, raw_id: str):
        self.raw_id = raw_id

    def get_photo_url(self):
        return self.photo_url

    def set_photo_url(self, photo_url: str):
        self.photo_url = photo_url

    def get_display_name(self):
        return self.display_name

    def set_display_name(self, display_name: str):
        self.display_name = display_name

    def get_open_id(self):
        return self.open_id

    def set_open_id(self, open_id: str):
        self.open_id = open_id

    def __iter__(self):
        yield from {
            "providerId": self.provider_id,
            "rawId": self.raw_id,
            "photoUrl": self.photo_url,
            "displayName": self.display_name,
            "openId": self.open_id,
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return {
            "providerId": self.provider_id,
            "rawId": self.raw_id,
            "photoUrl": self.photo_url,
            "displayName": self.display_name,
            "openId": self.open_id,
        }

    @staticmethod
    def from_json(json_dct):
        return ProviderInfo(json_dct.get("providerId"), json_dct.get("rawId"), json_dct.get("photoUrl"),
                            json_dct.get("displayName"), json_dct.get('openId'))
