from rich.progress import Progress, BarColumn, TimeRemainingColumn, DownloadColumn, TransferSpeedColumn, TextColumn

from threading import Thread

class ProgressBar:

    threads: list[Thread]
    size: int

    def __init__(self, threads, size) -> None:
        self.threads = threads
        self.size = size

    def show(self):
        temp = 0
        with Progress(
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeRemainingColumn(),
        ) as progress_bar:

            task = progress_bar.add_task(description='eta', total=self.size)

            while not progress_bar.finished:

                progress = 0

                for thread in self.threads:
                    progress += thread.progress

                progress_bar.update(task, advance=progress - temp)
                temp = progress