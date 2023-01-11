from ..commander import Command
from ..commander import Commander


class QueuesCommand(Command):

    command = 'queues'

    def execute(self, parsed):
        return '\n'.join(sorted(self._root.queue_names))


Commander.register(QueuesCommand)
