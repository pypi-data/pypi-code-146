from busy.commander import Commander
from busy.commander import TodoCommand


class ResourceCommand(TodoCommand):

    command = "resource"

    def execute_on_queue(self, parsed, queue):
        if parsed.criteria:  # pragma: nocover
            message = ("The `resource` command only returns the top item - "
                       "repeat without criteria")
            raise RuntimeError(message)
        else:
            return str(queue.resource() or '')


Commander.register(ResourceCommand)
