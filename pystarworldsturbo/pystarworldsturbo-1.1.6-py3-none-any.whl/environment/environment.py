from typing import Dict, List, Type, Optional
from pyoptional.pyoptional import PyOptional

from .ambient import Ambient
from .physics.action_executor import ActionExecutor
from ..elements.actor import Actor
from ..elements.body import Body
from ..elements.sensor import Sensor
from ..common.message import Message, BccMessage
from ..common.action import Action
from ..common.perception import Perception
from ..common.action_result import ActionResult
from ..common.exceptions import IdentityException
from ..utils.utils import ignore


class Environment():
    def __init__(self, ambient: Ambient, initial_actors: List[Actor]=[], initial_passive_bodies: List[Body]=[]) -> None:
        self.__ambient: Ambient = ambient
        self.__actors: Dict[str, Actor] = {actor.get_id(): actor for actor in initial_actors}
        self.__passive_bodies: Dict[str, Body] = {passive_body.get_id(): passive_body for passive_body in initial_passive_bodies}

    def get_ambient(self) -> Ambient:
        return self.__ambient

    def get_actors(self) -> Dict[str, Actor]:
        return self.__actors

    def get_actors_list(self) -> List[Actor]:
        return [actor for actor in self.__actors.values()]

    def get_actor(self, actor_id: str) -> PyOptional[Actor]:
        if actor_id not in self.__actors:
            return PyOptional.empty()
        else:
            return PyOptional.of(self.__actors[actor_id])

    def add_actor(self, actor: Actor) -> None:
        assert actor not in self.__actors

        self.__actors[actor.get_id()] = actor

    def remove_actor(self, actor_id: str) -> None:
        assert actor_id in self.__actors

        del self.__actors[actor_id]

    def get_passive_bodies(self) -> Dict[str, Body]:
        return self.__passive_bodies

    def get_passive_bodies_list(self) -> List[Body]:
        return [body for body in self.__passive_bodies.values()]

    def get_passive_body(self, passive_body_id: str) -> PyOptional[Body]:
        if passive_body_id not in self.__passive_bodies:
            return PyOptional.empty()
        else:
            return PyOptional.of(self.__passive_bodies[passive_body_id])

    def add_passive_body(self, passive_body: Body) -> None:
        assert passive_body not in self.__passive_bodies

        self.__passive_bodies[passive_body.get_id()] = passive_body

    def remove_passive_body(self, passive_body_id: str) -> None:
        assert passive_body_id in self.__passive_bodies

        del self.__passive_bodies[passive_body_id]

    def generate_perception_for_actor(self, actor_id: str, action_type: Type[Action], action_result: ActionResult) -> PyOptional[Perception]:
        # Abstract.

        ignore(actor_id)
        ignore(action_type)
        ignore(action_result)

        raise NotImplementedError()

    def send_message_to_recipients(self, message: Message, check_sender_identity: bool=True) -> None:
        if check_sender_identity and message.get_sender_id() not in self.__actors:
            raise IdentityException("Unknown sender: {}. The sender must be an actor living in the environment.".format(message.get_sender_id()))

        if message.get_recipients_ids() == []:
            message.override_recipients(recipient_ids=[recipient_id for recipient_id in self.__actors if recipient_id != message.get_sender_id()])

        self.__send_message_to_recipients(message=message)

    def __send_message_to_recipients(self, message: Message) -> None:
        for recipient_id in message.get_recipients_ids():
            if recipient_id in self.__actors and recipient_id != message.get_sender_id():
                bcc_message: BccMessage = BccMessage(content=message.get_content(), sender_id=message.get_sender_id(), recipient_id=recipient_id)
                recipient_listening_sensor: PyOptional[Sensor] = self.__actors[recipient_id].get_listening_sensor()

                recipient_listening_sensor.if_present(lambda sensor, perception=bcc_message: sensor.sink(perception=perception))

    def send_perception_to_actor(self, perception: Perception, actor_id: str) -> None:
        assert actor_id and actor_id in self.__actors

        actor_sensor: PyOptional[Sensor] = self.__actors[actor_id].get_sensor_for(type(perception))

        actor_sensor.if_present(lambda sensor, perception=perception: sensor.sink(perception=perception))

    def execute_cycle_actions(self) -> None:
        for actor in self.__actors.values():
            self.__execute_actor_actions(actor=actor)

    def __execute_actor_actions(self, actor: Actor) -> None:
        actor.cycle()
        actions: List[Action] = actor.get_pending_actions()
        self.validate_actions(actions=actions)

        for action in actions:
            self.execute_action(action=action)

    def validate_actions(self, actions: List[Action]) -> None:
        # Abstract.

        ignore(actions)

    def execute_action(self, action: Action) -> None:
        action_executor: ActionExecutor = self.get_executor_for(action=action).or_else_raise(ValueError("No executor found for action of type {}.".format(type(action))))
        result: ActionResult = action_executor.execute(env=self, action=action)
        perception: Perception = self.generate_perception_for_actor(action_type=type(action), actor_id=action.get_actor_id(), action_result=result).or_else_raise()

        self.send_perception_to_actor(perception=perception, actor_id=action.get_actor_id())

    def get_executor_for(self, action: Action) -> PyOptional[ActionExecutor]:
        # Abstract.

        ignore(action)

        raise NotImplementedError()
