from ..commander import QueueCommand
from ..commander import Commander


class ListCommand(QueueCommand):

    command = 'list'
    # key = "l"
    # prompt = "l)ist"

    def execute_on_queue(self, parsed, queue):
        itemlist = queue.list(*parsed.criteria)
        self.status = "Listed " + queue.criteria_string(*parsed.criteria)
        return self._list(queue, itemlist)


Commander.register(ListCommand)
