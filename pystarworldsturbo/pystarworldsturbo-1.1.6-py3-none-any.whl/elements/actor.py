from typing import List, Type
from pyoptional.pyoptional import PyOptional

from .body import Body
from .sensor import Sensor
from .actuator import Actuator
from .mind import Mind
from ..common.message import BccMessage
from ..common.action import Action


class Actor(Body):
    def __init__(self, mind: Mind, sensors: List[Sensor]=[], actuators: List[Actuator]=[]) -> None:
        super(Body, self).__init__()

        self.__mind: Mind = mind
        self.__sensors: List[Sensor] = sensors
        self.__actuators: List[Actuator] = actuators

    def get_mind(self) -> Mind:
        return self.__mind

    def get_sensors(self) -> List[Sensor]:
        return self.__sensors

    def get_listening_sensor(self) -> PyOptional[Sensor]:
        return self.get_sensor_for(event_type=BccMessage)

    def get_sensor_for(self, event_type: Type) -> PyOptional[Sensor]:
        for sensor in self.__sensors:
            if sensor.is_subscribed_to(event_type=event_type):
                return PyOptional.of(sensor)

        return PyOptional.empty()

    def get_actuators(self) -> List[Actuator]:
        return self.__actuators

    def get_actuator_for(self, event_type: Type) -> PyOptional[Actuator]:
        for actuator in self.__actuators:
            if actuator.is_subscribed_to(event_type=event_type):
                return PyOptional.of(actuator)

        return PyOptional.empty()

    def cycle(self) -> None:
        # Abstract.
        raise NotImplementedError()

    def get_pending_actions(self) -> List[Action]:
        actions: List[Action] = []

        # Any actor must execute at least one action per cycle.
        while not actions:
            actions += self.__get_pending_actions()

        return actions

    def __get_pending_actions(self) -> List[Action]:
        actions: List[Action] = []

        for actuator in self.__actuators:
            while actuator.has_pending_actions():
                actions += [a for a in actuator.source_all()]

        return actions
