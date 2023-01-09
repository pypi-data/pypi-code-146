import argparse
import json
import os
import time
import psutil


def get_task_count():
    tasks = psutil.process_iter()
    task_numb = {"total": 0, "running": 0, "sleeping": 0, "stopped": 0, "zombie": 0}
    for task in tasks:
        try:
            status = task.status()
            task_numb["total"] += 1
            if status == "sleeping":
                task_numb["sleeping"] += 1
            elif status == "stopped":
                task_numb["stopped"] += 1
            elif status == "zombie":
                task_numb["zombie"] += 1
        except Exception:
            pass
    return task_numb


class Snapshot:
    def __init__(self):
        self.tasks = get_task_count()
        self.cpu_times = psutil.cpu_times()
        self.memory = psutil.virtual_memory()
        self.swap = psutil.swap_memory()
        self.timestamp = int(time.time())

    @staticmethod
    def get_task_count():
        return task_numb

    def to_dict(self):
        return {
            'Tasks': self.tasks,
            '%CPU': {
                'user': self.cpu_times.user,
                'system': self.cpu_times.system,
                'idle': self.cpu_times.idle,
            },
            ' KiB Mem': {
                'total': self.memory.total,
                'free': self.memory.free,
                'used': self.memory.used
            },
            'KiB Swap': {
                'total': self.swap.total,
                'free': self.swap.free,
                'used': self.swap.used
            },
            'Timestamp': self.timestamp,
        }
# snapshot = Snapshot()
# print(snapshot.to_dict())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Interval between snapshots in seconds", type=int, default=30)
    parser.add_argument("-f", help="Output file name", default="snapshot.json")
    parser.add_argument("-n", help="Quantity of snapshot to output", default=20)
    args = parser.parse_args()

    with open(args.f, "w") as file:
        file.truncate(0)

    # Clear the contents of the output file
    # Take and output snapshots repeatedly
    for _ in range(args.n):
        snapshot = Snapshot().to_dict()

        # Clear the console and output the snapshot
        os.system('clear')
        print(snapshot, end="\r")

        # Write the snapshot to the output file as JSON
        with open(args.f, "a") as file:
            json.dump(snapshot, file)
            # json.dump(snapshot, file, indent=2, sort_keys=True)

            file.write('\n')

        # Sleep for the specified interval before taking the next snapshot
        time.sleep(args.i)


if __name__ == '__main__':
    main()
