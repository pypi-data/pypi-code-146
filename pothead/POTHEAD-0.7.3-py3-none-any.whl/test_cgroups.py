from unittest import TestCase
from math import inf

from .cgroups import parse_cpu_quota_v1, parse_cpu_quota_v2


class CgroupsTest(TestCase):
    def test_v1_valid(self):
        assert parse_cpu_quota_v1("500000", "500000") == 1.0
        assert parse_cpu_quota_v1("200000", "500000") == 0.4
        assert parse_cpu_quota_v1("-1", "500000") == inf

    def test_v1_invalid(self):
        self.verify_exception_with_msg(
            lambda: parse_cpu_quota_v1("0", "500000"), "Quota for cgroups v1 was 0"
        )

    def test_v2_valid(self):
        assert parse_cpu_quota_v2("500000 500000") == 1.0
        assert parse_cpu_quota_v2("200000 500000") == 0.4
        assert parse_cpu_quota_v2("max 500000") == inf

    def test_v2_invalid(self):
        self.verify_exception_with_msg(
            lambda: parse_cpu_quota_v2("0 500000"),
            "Quota in cgroups v2 cpu.max file was <= 0. Content: 0 500000",
        )
        self.verify_exception_with_msg(
            lambda: parse_cpu_quota_v2("-1 500000"),
            "Quota in cgroups v2 cpu.max file was <= 0. Content: -1 500000",
        )
        self.verify_exception_with_msg(
            lambda: parse_cpu_quota_v2("200000 0"),
            "Period in cgroups v2 cpu.max file was <= 0. Content: 200000 0",
        )
        self.verify_exception_with_msg(
            lambda: parse_cpu_quota_v2("200000 -1"),
            "Period in cgroups v2 cpu.max file was <= 0. Content: 200000 -1",
        )

    def verify_exception_with_msg(self, func, msg):
        with self.assertRaises(Exception) as ctx:
            func()
        assert str(ctx.exception) == msg
