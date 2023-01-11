from django.test import TestCase

from recomb_to_s3.contrib import send_dict_to_s3
from recomb_to_s3.models import User

data_test = {"test": "test"}


class MyModelTest(TestCase):
    def setUp(self):
        """creates two instances, one with author another without"""
        user = User.objects.create(username="test")
        self.my_model_with_author = send_dict_to_s3(
            author=user, file_name="test.txt", data=data_test
        )
        self.my_model_with_no_author = send_dict_to_s3(
            author=None, file_name="test.txt", data=data_test
        )

    def test_string_representation_with_no_author(self):
        """tests that the file name and type are being created correctly."""
        name_no_author = self.my_model_with_no_author.file.name.split("/")
        name_with_author = self.my_model_with_author.file.name.split("/")
        self.assertEqual(
            f"{name_no_author[0]}/{name_no_author[-1]}", "documents/test.txt"
        )
        self.assertEqual(
            f"{name_with_author[0]}/{name_with_author[1]}/{name_with_author[-1]}",
            "documents/test/test.txt",
        )
        self.assertEqual(self.my_model_with_no_author.file_type, "txt")
        self.assertEqual(self.my_model_with_author.file_type, "txt")

    def test_some_property(self):
        """tests whether the file name and type are being created."""
        self.assertTrue(self.my_model_with_no_author.file.name)
        self.assertTrue(self.my_model_with_author.file.name)
        self.assertTrue(self.my_model_with_no_author.file_type)
        self.assertTrue(self.my_model_with_author.file_type)
