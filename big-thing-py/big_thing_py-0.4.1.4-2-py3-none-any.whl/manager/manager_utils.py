from big_thing_py.manager.manager_common import *
from big_thing_py.staff_thing import *


class ManagerModeHandler:
    def __init__(self, mode: SoPManagerMode) -> None:
        self._mode = mode

    def dump_register_packet(self, staff_thing: SoPStaffThing) -> mqtt.MQTTMessage:
        if self._mode == SoPManagerMode.JOIN:
            # in join mode, manager thing don't need to send each staff thing's register packet
            # it's only need to send manager thing's register packet to middleware
            pass
        elif self._mode == SoPManagerMode.SPLIT:
            if staff_thing.get_registered():
                SOPLOG_DEBUG(
                    '[dump_register_packet] staff thing already registered')
                return False

            topic = SoPProtocolType.Base.TM_REGISTER.value % (
                staff_thing.get_name())
            payload = staff_thing.dump()
            msg = mqtt.MQTTMessage(topic, payload)
            return staff_thing.get_name(), payload
        else:
            raise ManagerModeError(
                '[dump_register_packet] please set mode {SoPManagerMode.JOIN|SoPManagerMode.SPLIT}')

    def dump_alive_packet(self, staff_thing_list: List[SoPStaffThing]) -> Union[mqtt.MQTTMessage, List[mqtt.MQTTMessage]]:
        if self._mode == SoPManagerMode.JOIN:
            # in join mode, manager thing don't need to send each staff thing's alive packet
            # it's only need to send manager thing's alive packet to middleware
            pass
        elif self._mode == SoPManagerMode.SPLIT:
            packet_list = []

            for staff_thing in staff_thing_list:
                if staff_thing.get_registered():
                    continue
                topic = SoPProtocolType.Base.TM_ALIVE.value % (
                    staff_thing.get_name())
                payload = EMPTY_JSON
                msg = mqtt.MQTTMessage(topic, payload)
                packet_list.append(msg)

            return packet_list
        else:
            raise ManagerModeError(
                '[dump_alive_packet] please set mode {SoPManagerMode.JOIN|SoPManagerMode.SPLIT}')

    def dump_value_packet(self, staff_thing_list: List[SoPStaffThing]) -> Union[mqtt.MQTTMessage, List[mqtt.MQTTMessage]]:
        if self._mode == SoPManagerMode.JOIN:
            # in join mode, manager thing don't need to send each staff thing's value packet
            # it's only need to send manager thing's value packet to middleware
            pass
        elif self._mode == SoPManagerMode.SPLIT:
            packet_list = []

            for staff_thing in staff_thing_list:
                if staff_thing.get_registered():
                    continue
                for value in staff_thing.get_value_list():
                    value_dump = value.dump()

                    topic = SoPProtocolType.Base.TM_ALIVE.value % (
                        staff_thing.get_name())
                    payload = EMPTY_JSON
                    msg = mqtt.MQTTMessage(topic, payload)
                    packet_list.append(msg)

            return packet_list
        else:
            raise ManagerModeError(
                '[dump_value_packet] please set mode {SoPManagerMode.JOIN|SoPManagerMode.SPLIT}')

    def dump_execute_result_packet(self, staff_thing_list: List[SoPStaffThing]) -> Union[mqtt.MQTTMessage, List[mqtt.MQTTMessage]]:
        if self._mode == SoPManagerMode.JOIN:
            pass
        elif self._mode == SoPManagerMode.SPLIT:
            pass
        else:
            raise ManagerModeError(
                '[dump_execute_result_packet] please set mode {SoPManagerMode.JOIN|SoPManagerMode.SPLIT}')
