from curses import echo, noecho
from busy.commander import Commander
from busy.commander import TodoCommand


class FinishCommand(TodoCommand):

    command = 'finish'
    key = 'f'
    prompt = 'f)inish'

    @classmethod
    def register(self, parser):
        parser.add_argument('--yes', action='store_true')

    def execute_on_queue(self, parsed, queue):
        if parsed:
            tasklist = queue.list(*parsed.criteria or [1])
            indices = [i[0]-1 for i in tasklist]
            confirmed = self.confirmed(parsed, tasklist, 'Finish')
            if confirmed:
                self.status = queue.finish(*indices)
            else:  # pragma: nocover
                self.status = "Finish Cancelled"


Commander.register(FinishCommand)
