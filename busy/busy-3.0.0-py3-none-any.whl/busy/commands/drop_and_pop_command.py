from ..commander import QueueCommand
from ..commander import Commander


class DropCommand(QueueCommand):

    command = 'drop'
    key = 'r'
    prompt = "d(r)op"


Commander.register(DropCommand)


class PopCommand(QueueCommand):

    command = 'pop'
    key = 'o'
    prompt = "p(o)p"


Commander.register(PopCommand)
