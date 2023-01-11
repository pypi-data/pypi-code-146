from ..commander import QueueCommand
from ..commander import Commander


class ShuffleCommand(QueueCommand):

    command = 'shuffle'


Commander.register(ShuffleCommand)
