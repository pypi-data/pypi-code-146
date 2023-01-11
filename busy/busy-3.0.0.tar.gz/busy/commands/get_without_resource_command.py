from busy.commander import Commander
from busy.commander import TodoCommand


class GetWithoutResourceCommand(TodoCommand):

    command = "get-without-resource"

    def execute_on_queue(self, parsed, queue):
        if parsed.criteria:  # pragma: nocover
            message = ("The `get-without-resource` command only returns the"
                       " top item - repeat without criteria")
            raise RuntimeError(message)
        else:
            return str(queue.get_without_resource() or '')


Commander.register(GetWithoutResourceCommand)
