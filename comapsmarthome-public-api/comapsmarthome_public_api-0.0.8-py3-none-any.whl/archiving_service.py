#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytz
import datetime
from comapsmarthome_public_api.comap_smart_home import ComapSmartHome

_DEFAULT_PROJECTIONS = [
    "id", "request_frame.firmware_version", "request_frame.voltage", "request_frame.reboot",
    "request_frame.motor_calibration_error", "response_frame.calibrate"
]


class ArchivingService(ComapSmartHome):
    service_url_suffix = "archiving"

    def get_transmissions(self, serial_number, dt_from, dt_to, projections=_DEFAULT_PROJECTIONS):
        """Get a list of all the transmissions of the specified product between two dates"""
        global_transmissions = []
        dt = datetime.timedelta(seconds=1)
        dt_from_parsed = datetime.datetime.fromisoformat(dt_from)
        params = [("serial_number", serial_number), ("from", dt_from), ("to", dt_to), ("projections", "received_at")]
        params += [('projections', projection) for projection in projections]

        url = "{}/transmissions/".format(self.base_url)
        transmissions = self.get_request(url=url, headers=self.request_header, params=params)
        global_transmissions += transmissions
        trans_beg = pytz.UTC.localize(datetime.datetime.utcfromtimestamp(transmissions[-1]["received_at"])) if len(transmissions) > 0 else dt_from_parsed
        while len(transmissions) > 0 and trans_beg > dt_from_parsed:
            params[2] = ("to", (trans_beg - dt).isoformat())
            transmissions = self.get_request(url=url, headers=self.request_header, params=params)
            global_transmissions += transmissions
            trans_beg = pytz.UTC.localize(datetime.datetime.utcfromtimestamp(transmissions[-1]["received_at"])) if len(transmissions) > 0 else dt_from_parsed

        return global_transmissions


if __name__ == '__main__':
    from comapsmarthome_public_api.client_auth import ClientAuth

    dt_from = '2020-10-20T09:30+02:00'
    dt_to = '2020-10-20T11:00+02:00'
    serial_number = 'SERIAL_NUMBER'

    auth = ClientAuth()
    archiving = ArchivingService(auth)

    transmissions = archiving.get_transmissions(serial_number=serial_number, dt_from=dt_from, dt_to=dt_to)
