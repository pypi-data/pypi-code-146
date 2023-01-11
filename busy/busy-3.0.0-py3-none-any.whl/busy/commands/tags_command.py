from ..commander import QueueCommand
from ..commander import Commander


class TagsCommand(QueueCommand):

    command = 'tags'

    def execute_on_queue(self, parsed, queue):
        return '\n'.join(sorted(queue.tags()))


Commander.register(TagsCommand)
