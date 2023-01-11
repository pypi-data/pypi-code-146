from big_thing_py.common.mqtt_message import *
from big_thing_py.common.soptype import *


class SoPRequest(metaclass=ABCMeta):
    def __init__(self, trigger_msg: SoPMQTTMessage = None, result_msg: SoPMQTTMessage = None) -> None:
        self._action_type: SoPActionType = None
        self._trigger_msg = trigger_msg
        self._result_msg = result_msg

        # seconds
        self._duration: float = None

    def duration(self):
        return self._duration

    def timer_start(self):
        self._trigger_msg.set_timestamp(time.time())

    def timer_end(self):
        try:
            self._result_msg.set_timestamp(time.time())
            self._duration = self._result_msg.timestamp() - \
                self._trigger_msg.timestamp()
        except Exception:
            self._duration = time.time() - self._trigger_msg.timestamp()
        return self.duration()


class SoPRegisterRequest(SoPRequest):
    def __init__(self, trigger_msg: SoPMQTTMessage = None, result_msg: SoPMQTTMessage = None) -> None:
        super().__init__(trigger_msg, result_msg)
        self._action_type = SoPActionType.REGISTER

        self._trigger_msg: SoPExecuteMessage
        self._result_msg: SoPExecuteResultMessage


class SoPExecuteRequest(SoPRequest):
    def __init__(self, trigger_msg: SoPExecuteMessage = None, result_msg: SoPExecuteResultMessage = None) -> None:
        super().__init__(trigger_msg, result_msg)
        self._action_type = SoPActionType.EXECUTE

        self._trigger_msg: SoPExecuteMessage
        self._result_msg: SoPExecuteResultMessage

    def set_return_msg(self, result: SoPExecuteResultMessage):
        self._result_msg = result

    def set_return_value(self, return_value):
        self._result_msg._return_value = return_value
        
    def get_return_msg(self):
        return self._result_msg

    def get_return_value(self):
        return self._result_msg._return_value
