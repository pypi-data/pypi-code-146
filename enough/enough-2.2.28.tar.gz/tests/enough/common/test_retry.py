import pytest
from enough.common import retry


def test_that_retry_works_on_simple_function():

    @retry.retry(Exception)
    def f():
        return True

    assert f()


def test_that_retry_fails():

    @retry.retry(AssertionError)
    def f():
        assert 0

    with pytest.raises(retry.RetryException):
        f()


def test_that_retry_works_on_complex_function():
    class C():
        fail = 2

        @retry.retry(Exception, tries=3)
        def f(self):
            self.fail -= 1
            assert self.fail == 0
            return True

    c = C()
    assert c.f()
    assert c.fail == 0


def test_that_retry_works_with_fixed_delays():
    class C():
        fail = 2

        @retry.retry(Exception, tries=3, delay=2, exponential=False)
        def f(self):
            self.fail -= 1
            assert self.fail == 0
            return True

    c = C()
    assert c.f()
    assert c.fail == 0
