from w.services.technical.string_service import StringService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestExcelService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()

    """
    strip_accents
    """

    def test_strip_accents_with_success_return_cleaned_txt(self):
        """Ensure method succeeds"""
        txt = "àéèïôù"
        actual = StringService.strip_accents(txt)
        self.assert_equals_resultset(actual)

    """
    clean
    """

    def test_clean_with_no_replacement_return_cleaned_txt(self):
        """Ensure method succeeds"""
        txt = "  tHis Is à str-iNg 2 clé@N :  "
        actual = StringService.clean(txt)
        self.assert_equals_resultset(actual)

    def test_clean_with_success_return_cleaned_txt(self):
        """Ensure method succeeds"""
        txt = "  tHis Is à str-iNg 2 clé@N :  "
        actual = StringService.clean(txt, {"2": "to", "@": "a", " :": ".", "-": ""})
        self.assert_equals_resultset(actual)
