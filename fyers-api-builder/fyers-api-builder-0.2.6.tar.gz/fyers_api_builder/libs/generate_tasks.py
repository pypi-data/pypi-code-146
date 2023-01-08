from datetime import datetime, timedelta


def generate_tasks(fetch_from_epoch, fetch_to_epoch):
    tasks = []

    while True:
        fetch_from_epoch_item = (
            tasks[-1]["fetch_from"] if len(tasks) else fetch_from_epoch
        )

        fetch_to_epoch_item = int(
            (
                datetime.fromtimestamp(fetch_from_epoch_item) + timedelta(days=100)
            ).timestamp()
        )

        if fetch_to_epoch_item >= fetch_to_epoch:
            tasks.append(
                {
                    "fetch_from": fetch_from_epoch_item,
                    "fetch_to": fetch_to_epoch,
                }
            )
            break
        else:
            tasks.append(
                {
                    "fetch_from": fetch_from_epoch_item,
                    "fetch_to": fetch_to_epoch_item,
                }
            )
            continue

    return tasks
