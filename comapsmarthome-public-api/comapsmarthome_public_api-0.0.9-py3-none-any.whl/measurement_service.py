#!/usr/bin/env python
# -*- coding: utf-8 -*-

from comapsmarthome_public_api.comap_smart_home import ComapSmartHome

_AVAILABLE_MEASUREMENTS = [
    'time', 'inside_temperature', 'inside_humidity', 'heating_commands', 'presence', 'temperature_instruction',
    'voltage', 'outside_temperature', 'outside_humidity'
]


class MeasurementsService(ComapSmartHome):
    service_url_suffix = 'measurements'

    def get_measurements(self, dt_from, dt_to, zone_id=None, serial_number=None, measurements=_AVAILABLE_MEASUREMENTS):
        """Get a list of all the specified variables for a given product or zone between two dates"""
        if zone_id:
            params = {"zone_id": zone_id, "from": dt_from, "to": dt_to, "measurements": measurements}
        elif serial_number:
            params = {"serial_number": serial_number, "from": dt_from, "to": dt_to, "measurements": measurements}
        url = "{}/".format(self.base_url)
        return self.get_request(url=url, headers=self.request_header, params=params)


if __name__ == '__main__':
    from comapsmarthome_public_api.client_auth import ClientAuth

    dt_from = '2020-10-20T09:30+02:00'
    dt_to = '2020-10-20T11:00+02:00'
    serial_number = 'SERIAL_NUMBER'
    dt_from = '2023-01-10T09:30+02:00'
    dt_to = '2023-01-11T11:00+02:00'
    serial_number = 'aa043ae928c1'

    auth = ClientAuth()
    measurement = MeasurementsService(auth)

    measurements = ['inside_temperature']
    data = measurement.get_measurements(dt_from=dt_from, dt_to=dt_to, serial_number=serial_number, measurements=measurements)
    dates = [d['time'] for d in data]
    temperatures = [d['inside_temperature'] for d in data]
