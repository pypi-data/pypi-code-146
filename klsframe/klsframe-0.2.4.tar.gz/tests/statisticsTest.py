import klsframe.utilities.statistics as stats
import time


def test_timing():
    def addition(*args):
        try:
            total = 0
            for arg in args:
                total += int(arg)
            print(f"{' + '.join([str(val) for val in args])} = {total}")
            time.sleep(3)
        except TypeError:
            print('[ERROR] Invalid parameters. Only numbers allowed')

    stats.timing(addition, 2, 3)


if __name__ == '__main__':
    test_timing()
