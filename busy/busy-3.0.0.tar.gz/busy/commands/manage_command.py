from io import StringIO

from ..commander import QueueCommand
from ..commander import Commander
from ..file import write_items
from ..file import read_items
from ..ui.tcl_ui.edit_task_widget import EditTaskWidget
import busy


def text_editor(itemclass, *items):
    sio = StringIO(newline=None)
    write_items(sio, *items)
    before = sio.getvalue()
    sio.close()
    edited = busy.editor(before)
    sio2 = StringIO(edited)
    new_items = read_items(sio2, itemclass)
    sio2.close()
    return new_items


def single_task_ui_editor(itemclass, *items):  # pragma: no cover
    assert len(items) == 1
    ui = EditTaskUi(initial_value=str(items[0]))
    return [itemclass(ui.value)]


class ManageCommand(QueueCommand):

    command = 'manage'

    @classmethod
    def register(self, parser):
        super().register(parser)
        parser.add_argument('--interactive', action='store_true')

    def execute_on_queue(self, parsed, queue):
        if parsed.interactive:  # pragma: no cover
            editor = single_task_ui_editor
        else:
            editor = text_editor
        queue.manage(*parsed.criteria, editor=editor)


Commander.register(ManageCommand)
