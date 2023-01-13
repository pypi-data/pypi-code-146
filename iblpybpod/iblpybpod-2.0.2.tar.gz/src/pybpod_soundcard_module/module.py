from enum import IntEnum
from pybpodapi.bpod_modules.bpod_module import BpodModule


class SoundCommandType(IntEnum):
    """
    Enumeration for the commands that can be sent through the Sound Card module, when connected through the BPod's
    State Machine.

    """
    #: Plays a specific sound index
    PLAY = 1
    #: Stops playing a specific sound index
    STOP_SPECIFIC = 2
    #: Stops all sounds
    STOP_ALL = 3


class SoundCard(BpodModule):

    @staticmethod
    def check_module_type(module_name):
        return module_name and module_name.startswith('SoundCard')

    @staticmethod
    def get_command(command_type, sound_index=None):
        """
        Returns the proper bytes to send as output_actions in the BPod StateMachine's states. In the case of the Play
        and StopSpecific command_types, it is required to \ use the BPod's load_serial_message method to be able to
        send to the module more than 1 byte properly.

        .. note:: This might not be required in a future version of BPod's firmware

        :param command_type: Instruction of type :class:`.SoundCommandType` to generate the command
        :param sound_index: The sound index to play or stop

        """
        if not command_type:
            raise Exception("You need to provide the type of the command you want returned")

        if command_type is SoundCommandType.PLAY or command_type is SoundCommandType.STOP_SPECIFIC:
            if not sound_index:
                raise Exception("You need to provide the sound_index value to play")

            if sound_index < 2 or sound_index > 31:
                raise Exception("sound_index must have a value between 2 and 31")

        if command_type is SoundCommandType.PLAY:
            return [ord('P'), sound_index]
        if command_type is SoundCommandType.STOP_SPECIFIC:
            return [ord('x'), sound_index]

        # by default return stop
        return ord('X')
