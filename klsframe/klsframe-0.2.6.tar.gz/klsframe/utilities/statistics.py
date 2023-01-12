from datetime import datetime

stats_example_json = {
    'total clicks': 0,
    'total_key_presses': 0,
    'time_traveling': 0
}


def timing(func, *args):
    start_dt = datetime.now()
    func(*args)
    elapsed = datetime.now() - start_dt
    print(
        f'[INFO] Execution completed {int(elapsed.seconds / 60)} '
        f'min {elapsed.seconds % 60} s {elapsed.microseconds} µs')


if __name__ == '__main__':
    # Do some quick tests here
    pass
