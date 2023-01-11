from w.services.technical.list_service import ListService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestListService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        cls.list1 = [10, 11, 12, 13, 14, 16, 15]
        cls.list2 = [10, 11, 12, 18, 19, 16]

    """
    list_differences
    """

    def test_list_differences_with_no_difference_return_list(self):
        """Ensure method succeed with no difference"""
        assert ListService.list_differences(["no", "diff"], ["no", "diff"]) == []

    def test_list_differences_with_success_return_list(self):
        """Ensure method succeed with no difference"""
        expected = [18, 19, 13, 14, 15]
        assert ListService.list_differences(self.list1, self.list2) == expected

    """
    are_same
    """

    def test_are_same_with_no_difference_return_true(self):
        """Ensure method return True if lists are same"""
        assert ListService.are_same(["no", "diff"], ["no", "diff"]) is True

    def test_are_same_with_success_return_false(self):
        """Ensure method return False if lists are different"""
        assert ListService.are_same(self.list1, self.list2) is False

    """
    are_different
    """

    def test_are_different_with_no_difference_return_false(self):
        """Ensure method return False if lists are same"""
        assert ListService.are_different(["no", "diff"], ["no", "diff"]) is False

    def test_are_different_with_success_return_true(self):
        """Ensure method return True if lists are different"""
        assert ListService.are_different(self.list1, self.list2) is True
