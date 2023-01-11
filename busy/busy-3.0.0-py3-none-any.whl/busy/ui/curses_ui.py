
from curses import wrapper, echo, noecho
import curses

from ..ui import UI


class CursesUI(UI):  # pragma: nocover

    label = 'curses'

    def __init__(self, commander):
        super().__init__(commander)
        self._mode = "WORK"

    def start(self):
        wrapper(self.term_loop)

    def confirmed(self, parsed, itemlist, verb):
        self._stdscr.addstr("Finish? (Y/n) ")
        echo()
        confirmed = self._stdscr.getstr().decode().startswith('Y')
        noecho()
        return confirmed

    def term_loop(self, stdscr):
        curses.init_color(curses.COLOR_BLACK, 200, 200, 200)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self._stdscr = stdscr
        stdscr.clear()
        self._commander.queue_key = "tasks"
        status = "Welcome to Busy!"
        list = ""
        bottom = curses.LINES - 1
        cursor = 0
        while True:
            stdscr.clear()
            stdscr.move(0, 0)
            stdscr.addstr("Queue: ", curses.color_pair(1))
            stdscr.addstr(str(self._commander.queue_key), curses.A_BOLD)
            stdscr.move(1, 0)
            queue_key = self._commander.queue_key
            queue = self._commander._root.get_queue(queue_key)
            stdscr.addstr("Top:   ", curses.color_pair(1))
            stdscr.addstr(str(queue.get()) or '', curses.A_BOLD)
            stdscr.move(3, 0)
            stdscr.addstr(status, curses.color_pair(2))
            stdscr.move(4, 0)
            keys = self._commander._keys
            prompts = [self._commander._keys[k].prompt for k in keys]
            stdscr.addstr(" ".join(["e)xit", *prompts, "--> "]))
            incursor = stdscr.getyx()
            stdscr.refresh()
            stdscr.move(*incursor)
            key = stdscr.getkey()
            if key == "e":
                exit()
            else:
                stdscr.addstr(key)
                stdscr.move(bottom, 0)
                stdscr.refresh()
                if key in self._commander._keys:
                    command_class = self._commander._keys[key]
                    root = self._commander._root
                    command = command_class(root, self._commander._ui)
                    args = command.get_args_in_term(stdscr)
                    parsed = self._commander.parse(*args)
                    key = self._commander.queue_key
                    queue = self._commander._root.get_queue(key)
                    result = command.execute_on_queue(parsed, queue)
                    status = command.status or ""
                    command.save()

    # def listmode(self):
    #     length = len(list.splitlines())
    #     if length:
    #         listpad = curses.newpad(length, curses.COLS)
    #         listpad.addstr(list)
    #         self.listmode = True
    #         listpad.move(cursor, 0)
    #         listpad.addstr(">")
    #         listpad.refresh(0, 0, 5, 0, curses.LINES - 5, curses.COLS)
    #     if self.listmode:
    #         if key == "KEY_UP" and cursor > 0:
    #             cursor = cursor - 1
    #         if key == "KEY_DOWN" and cursor < length:
    #             cursor = cursor + 1
