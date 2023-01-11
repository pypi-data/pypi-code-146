from datetime import timedelta

from chalk.utils.duration import timedelta_to_duration


def test_timedelta_to_duration():
    assert timedelta_to_duration(timedelta(seconds=4)) == "4s"
    assert timedelta_to_duration(timedelta(seconds=4, minutes=30)) == f"{30*60+4}s"
    assert timedelta_to_duration(timedelta(seconds=4, microseconds=44)) == f"4s"
    assert timedelta_to_duration(timedelta(seconds=4, microseconds=44, days=1)) == f"1d 4s"
    assert timedelta_to_duration(timedelta(days=2)) == f"2d"
