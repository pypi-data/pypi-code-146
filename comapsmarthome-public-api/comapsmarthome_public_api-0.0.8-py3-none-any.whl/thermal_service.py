#!/usr/bin/env python
# -*- coding: utf-8 -*-

from comapsmarthome_public_api.comap_smart_home import ComapSmartHome


class ThermalService(ComapSmartHome):
    service_url_suffix = "thermal"

    def get_housing_thermal_details(self, housing_id):
        """Get housing thermal details"""
        url = "{}/housings/{}/thermal-details".format(self.base_url, housing_id)
        return self.get_request(url=url, headers=self.request_header)

    def get_zone_thermal_details(self, housing_id, zone_id):
        """Get zone thermal details"""
        url = "{}/housings/{}/thermal-details/zones/{}".format(self.base_url, housing_id, zone_id)
        return self.get_request(url=url, headers=self.request_header)

    def set_heating_system_state(self, housing_id, state):
        """Enable/disable heating"""
        data = {"state": state}
        url = "{}/housings/{}/thermal-control/heating-system-state".format(self.base_url, housing_id)
        return self.put_request(url=url, headers=self.request_header, data=data)

    def set_absence(self, housing_id, id, dt_from, dt_to):
        """Define absence period"""
        data = {"id": id, "begin_at": dt_from, "end_at": dt_to}
        url = "{}/housings/{}/thermal-control/absence".format(self.base_url, housing_id)
        return self.post_request(url=url, headers=self.request_header, data=data)

    def cancel_absence(self, housing_id):
        """Cancel absence period"""
        url = "{}/housings/{}/thermal-control/absence".format(self.base_url, housing_id)
        return self.delete_request(url=url, headers=self.request_header)

    def leave_home(self, housing_id):
        """Send 'leave-home' signal"""
        url = "{}/housings/{}/thermal-control/leave-home".format(self.base_url, housing_id)
        return self.post_request(url=url, headers=self.request_header)

    def delete_leave_home(self, housing_id):
        """Cancel 'leave-home' signal"""
        url = "{}/housings/{}/thermal-control/leave-home".format(self.base_url, housing_id)
        return self.delete_request(url=url, headers=self.request_header)

    def come_back_home(self, housing_id):
        """Send 'come-back-home' signal"""
        url = "{}/housings/{}/thermal-control/come-back-home".format(self.base_url, housing_id)
        return self.post_request(url=url, headers=self.request_header)

    def delete_come_back_home(self, housing_id):
        """Cancel 'come-back-home' signal"""
        url = "{}/housings/{}/thermal-control/come-back-home".format(self.base_url, housing_id)
        return self.delete_request(url=url, headers=self.request_header)

    def plus_action(self, housing_id, zone_id):
        """'Plus' action on the zone"""
        url = "{}/housings/{}/thermal-control/zones/{}/heat/raise".format(self.base_url, housing_id, zone_id)
        return self.post_request(url=url, headers=self.request_header)

    def minus_action(self, housing_id, zone_id):
        """'Minus' action on the zone'"""
        url = "{}/housings/{}/thermal-control/zones/{}/heat/fall".format(self.base_url, housing_id, zone_id)
        return self.post_request(url=url, headers=self.request_header)

    def set_temporary_instruction(self, housing_id, zone_id, duration, set_point):
        """Set temporary instruction"""
        data = {"duration": duration, "set_point": {"instruction": set_point}}
        url = "{}/housings/{}/thermal-control/zones/{}/temporary-instruction".format(self.base_url, housing_id, zone_id)
        return self.post_request(url=url, headers=self.request_header, data=data)

    def cancel_temporary_instruction(self, housing_id, zone_id):
        """Cancel temporary instruction"""
        url = "{}/housings/{}/thermal-control/zones/{}/temporary-instruction".format(self.base_url, housing_id, zone_id)
        return self.delete_request(url=url, headers=self.request_header)

    def get_thermal_settings(self, housing_id):
        """Get housing thermal settings"""
        url = "{}/housings/{}/thermal-settings".format(self.base_url, housing_id)
        return self.get_request(url=url, headers=self.request_header)

    def get_custom_temperatures(self, housing_id):
        """Get housing custom temperatures"""
        url = "{}/housings/{}/custom-temperatures".format(self.base_url, housing_id)
        return self.get_request(url=url, headers=self.request_header)

    def update_custom_temperatures(self, housing_id, temperatures):
        """Update housing custom temperatures"""
        url = "{}/housings/{}/custom-temperatures".format(self.base_url, housing_id)
        return self.patch_request(url=url, headers=self.request_header, data=temperatures)

    def get_programs(self, housing_id):
        """Get housing programs"""
        url = "{}/housings/{}/programs".format(self.base_url, housing_id)
        return self.get_request(url=url, headers=self.request_header)

    def set_program_schedule(self, housing_id, zone_id, program_id, prog_type, schedule_id):
        """Set schedule for specified zone and program"""
        data = {"programming_type": prog_type, "schedule_id": schedule_id}
        url = "{}/housings/{}/programs/{}/zones/{}".format(self.base_url, housing_id, program_id, zone_id)
        return self.post_request(url=url, headers=self.request_header, data=data)

    def create_program(self, housing_id, title):
        """create new program"""
        data = {"title": title}
        url = "{}/housings/{}/programs".format(self.base_url, housing_id)
        return self.post_request(url=url, headers=self.request_header, data=data)

    def update_program(self, housing_id, program_id, title):
        """Update program"""
        data = {"title": title}
        url = "{}/housings/{}/programs/{}".format(self.base_url, housing_id, program_id)
        return self.patch_request(url=url, headers=self.request_header, data=data)

    def delete_program(self, housing_id, program_id):
        """Delete program"""
        url = "{}/housings/{}/programs/{}".format(self.base_url, housing_id, program_id)
        return self.delete_request(url=url, headers=self.request_header)

    def activate_program(self, housing_id, program_id):
        """Activate program"""
        url = "{}/housings/{}/programs/{}/activate".format(self.base_url, housing_id, program_id)
        return self.post_request(url=url, headers=self.request_header)

    def get_schedules(self, housing_id):
        """Get the list of schedules for the specified housing"""
        url = "{}/housings/{}/schedules".format(self.base_url, housing_id)
        return self.get_request(url=url, headers=self.request_header)

    def create_schedule(self, housing_id, schedule):
        """Create schedule"""
        url = "{}/housings/{}/schedules".format(self.base_url, housing_id)
        return self.post_request(url=url, headers=self.request_header, data=schedule)

    def get_schedule(self, housing_id, schedule_id):
        """Get schedule details"""
        url = "{}/housings/{}/schedules/{}".format(self.base_url, housing_id, schedule_id)
        return self.get_request(url=url, headers=self.request_header)

    def update_schedules(self, housing_id, schedule_id, schedule):
        """Update specified schedule"""
        url = "{}/housings/{}/schedules/{}".format(self.base_url, housing_id, schedule_id)
        return self.put_request(url=url, headers=self.request_header, data=schedule)

    def delete_schedule(self, housing_id, schedule_id):
        """Delete schedule"""
        url = "{}/housings/{}/schedules/{}".format(self.base_url, housing_id, schedule_id)
        return self.delete_request(url=url, headers=self.request_header)

    def duplicate_schedule(self, housing_id, schedule_id):
        """Duplicate schedule"""
        url = "{}/housings/{}/schedules/{}/duplicate".format(self.base_url, housing_id, schedule_id)
        return self.post_request(url=url, headers=self.request_header)

    def create_zone(self, housing_id, id, title, area_type):
        """Create new zone"""
        data = {"id": id, "title": title, "area_type": area_type}
        url = "{}/housings/{}/zones".format(self.base_url, housing_id)
        return self.post_request(url=url, headers=self.request_header, data=data)

    def get_zones(self, housing_id):
        """Get a list of all zones in specified housing"""
        url = "{}/housings/{}/zones".format(self.base_url, housing_id)
        return self.get_request(url=url, headers=self.request_header)

    def update_zone(self, housing_id, zone_id, title, area_type):
        """Update specified zone"""
        data = {"title": title, "area_type": area_type}
        url = "{}/housings/{}/zones/{}".format(self.base_url, housing_id, zone_id)
        return self.patch_request(url=url, headers=self.request_header, data=data)

    def get_zone(self, housing_id, zone_id):
        """Get zone details"""
        url = "{}/housings/{}/zones/{}".format(self.base_url, housing_id, zone_id)
        return self.get_request(url=url, headers=self.request_header)

    def delete_zone(self, housing_id, zone_id):
        """Delete zone"""
        url = "{}/housings/{}/zones/{}".format(self.base_url, housing_id, zone_id)
        return self.delete_request(url=url, headers=self.request_header)

    def get_eligible_zones(self, housing_id, serial):
        """Get eligible zones for specified object"""
        url = "{}/housings/{}/eligible-zones/{}".format(self.base_url, housing_id, serial)
        return self.get_request(url=url, headers=self.request_header)

    def associate_object_to_zone(self, housing_id, zone_id, serial):
        """Associate specified object to the specified zone"""
        data = {"serial_number": serial}
        url = "{}/housings/{}/zones/{}/associate-object".format(self.base_url, housing_id, zone_id)
        return self.put_request(url=url, headers=self.request_header, data=data)

    def set_heating_priority(self, housing_id, heating_priority):
        """Set the heating priority for a housing. Can be one of [primary|secondary]"""
        data = {'heating_priority': heating_priority}
        url = "{}/housings/{}/heating-priority".format(self.base_url, housing_id)
        self.post_request(url=url, headers=self.request_header, data=data)

if __name__ == '__main__':
    from comapsmarthome_public_api.client_auth import ClientAuth

    housing_id = 'HOUSING_ID'

    auth = ClientAuth()
    thermal = ThermalService(auth)

    zones = thermal.get_zones(housing_id=housing_id)
