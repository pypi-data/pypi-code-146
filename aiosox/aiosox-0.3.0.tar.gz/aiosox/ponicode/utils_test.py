from aiosox import utils


class Test_Utils_To_no_underscore:
    def test_to_no_underscore_1(self):
        utils.to_no_underscore("2017-09-29T23:01:00.000Z")

    def test_to_no_underscore_2(self):
        utils.to_no_underscore("2017-09-29T19:01:00.000")

    def test_to_no_underscore_3(self):
        utils.to_no_underscore("01:04:03")

    def test_to_no_underscore_4(self):
        utils.to_no_underscore("Mon Aug 03 12:45:00")

    def test_to_no_underscore_5(self):
        utils.to_no_underscore("")

    def test_to_no_underscore_6(self):
        utils.to_no_underscore(None)


class Test_Utils_Title_case:
    def test_title_case_1(self):
        result = utils.title_case("Mon Aug 03 12:45:00")

    def test_title_case_2(self):
        result = utils.title_case("2017-09-29T23:01:00.000Z")

    def test_title_case_3(self):
        result = utils.title_case("01:04:03")

    def test_title_case_4(self):
        result = utils.title_case("")
