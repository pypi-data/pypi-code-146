from ..commander import QueueCommand
from ..commander import Commander


class DeleteCommand(QueueCommand):

    command = 'delete'

    @classmethod
    def register(self, parser):
        super().register(parser)
        parser.add_argument('--yes', action='store_true')

    def execute_on_queue(self, parsed, queue):
        itemlist = queue.list(*parsed.criteria or [1])
        indices = [i[0]-1 for i in itemlist]
        if self.confirmed(parsed, itemlist, 'Delete'):
            queue.delete_by_indices(*indices)


Commander.register(DeleteCommand)
