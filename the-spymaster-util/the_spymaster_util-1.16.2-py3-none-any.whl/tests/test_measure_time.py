from time import sleep

from the_spymaster_util.measure_time import MeasureTime

SLEEP_TIME_SEC = 0.1


def test_measure_time_is_a_context_manager():
    with MeasureTime() as measure:
        sleep(SLEEP_TIME_SEC)

    assert abs(SLEEP_TIME_SEC - measure.duration.total_seconds()) < 0.01
