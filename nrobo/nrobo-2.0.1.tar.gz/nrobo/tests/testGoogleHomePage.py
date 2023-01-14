
import pytest

from helpers.Page import Page
from helpers.nRobo import NRobo

from pages.pageGoogleHome import PageGoogleHome

@pytest.mark.usefixtures('setup')
@pytest.mark.usefixtures('password')
@pytest.mark.usefixtures('username')
@pytest.mark.usefixtures('url')
class TestDemo(NRobo):

    @pytest.mark.sanity
    def test_google_home_page_is_accessible(self, url, username, password):

        print("{0}, {1}, {2}", url, username, password)

        pageGoogleHome = PageGoogleHome(self.driver)

        pageGoogleHome.open_home_page()

    @pytest.mark.sanity
    @pytest.mark.skip
    def test_example_of_skipped_test(self, url, username, password):
        print("{0}, {1}, {2}", url, username, password)

        print("This test will skip and not execute due to pytest marke @pytest.mark.skip is applied")

    @pytest.mark.sanity
    def test_failing_test(self, url, username, password):
        print("{0}, {1}, {2}", url, username, password)

        pageGoogleHome = PageGoogleHome(self.driver)

        pageGoogleHome.log.info("This test will fail!")

        assert 1 == 3




