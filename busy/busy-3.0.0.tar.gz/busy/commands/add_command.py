from curses import echo, noecho
from ..commander import QueueCommand
from ..commander import Commander
from ..ui.tcl_ui.edit_task_widget import EditTaskWidget


class AddCommand(QueueCommand):

    command = 'add'
    key = 'a'
    prompt = "a)dd"

    @classmethod
    def register(self, parser):
        super().register(parser)
        parser.add_argument('item', nargs='?')
        parser.add_argument('--interactive', action='store_true')

    def get_args_in_term(self, stdscr):  # pragma: nocover
        stdscr.addstr("Item: ")
        echo()
        item = stdscr.getstr().decode()
        noecho()
        return ["add", "--item", item]  # TODO: Add at the Command level.

    def execute_on_queue(self, parsed, queue):
        if parsed.interactive:  # pragma: no cover
            frame = EditTaskUi(lambda task: queue.add(task))
        else:
            if hasattr(parsed, 'item') and parsed.item:
                item = parsed.item
            else:
                item = input('Item: ')
            queue.add(item)
        self.status = "Added: " + item


Commander.register(AddCommand)
