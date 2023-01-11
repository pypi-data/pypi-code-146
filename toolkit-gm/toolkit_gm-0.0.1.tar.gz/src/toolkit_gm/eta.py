import datetime
from misc import percent

class Eta:
    """Object to follow execution advancement."""

    def __init__(self) -> None:
        self.begin_time = 0
        self.length = 0
        self.current_count = 0
        self.last_display_time = 0
        self.text = ''


    def begin(self, length, text) -> None:
        """Start a counter."""

        self.length = length
        self.current_count = 0
        self.text = text

        now = datetime.datetime.now().timestamp()
        self.begin_time = now

        print(self.text + ' - Elapsed: [00:00] - ETA [??:??] - ' + percent(0))
        self.last_display_time = now


    def iter(self, force_print=False) -> None:
        """On an iteration."""

        self.current_count += 1
        now = datetime.datetime.now().timestamp()

        timeSinceLastDisplay = now - self.last_display_time

        if (now - self.last_display_time < 1) and not force_print: return

        time_spent = now - self.begin_time
        percent_spent = self.current_count / self.length

        if(percent_spent != 0): time_left = (time_spent / percent_spent) - time_spent
        else: time_left = 0

        minutes_elapsed = int(time_spent / 60)
        seconds_elapsed = round(time_spent - (60 * minutes_elapsed))
        minutes_left = int(time_left / 60)
        seconds_left = round(time_left - (60 * minutes_left))

        print('\033[1A\033[K' + self.text + f' - Elapsed: [{minutes_elapsed}:{seconds_elapsed}] - ETA [{minutes_left}:{seconds_left}] - ' + percent(percent_spent))
        self.last_display_time = now


    def end(self) -> None:
        """Finalize an ETA counting."""

        now = datetime.datetime.now().timestamp()
        total_time = now - self.begin_time
        total_minutes = int(total_time / 60)
        total_sec = round(total_time - (60 * total_minutes))

        print('\033[1A\033[K' + self.text + f' is done - Elapsed: [{total_minutes}:{total_sec}]')


    def log(self, string) -> None:
        """Print out a log, without messing with the ETA display."""

        print(string)
        self.iter(force_print=True)

