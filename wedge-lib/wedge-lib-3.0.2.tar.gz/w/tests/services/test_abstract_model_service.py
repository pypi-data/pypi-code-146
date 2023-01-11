import pytest
from django.db import IntegrityError

from w.data_test_factory.data_test_factory import DataTestFactory
from w.django.tests.django_testcase import DjangoTestCase
from w.tests.fixtures.datasets.django_app import models, dtf_recipes
from w.tests.fixtures.datasets.services.model_services import (
    ExampleService,
    AuthorService,
    BookService,
)


class TestAbstractModelService(DjangoTestCase):
    _dtf = DataTestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.author = cls._dtf.build(dtf_recipes.base_author)
        cls.book = cls._dtf.build(dtf_recipes.base_book)
        cls.new_author_birth_city = cls._dtf.build(dtf_recipes.base_city)
        cls.new_book_series = cls._dtf.build(dtf_recipes.base_series)

    """
    create
    """

    def test_create_with_success_return_instance(self):
        """Ensure create succeed"""
        actual = ExampleService.create(attribute_one="one", attribute_two="two")
        assert isinstance(actual, models.Example)
        assert actual.attribute_one == "one"
        assert actual.attribute_two == "two"

    """
    get_or_create
    """

    def test_get_or_create_with_existing_instance_return_tuple(self):
        """Ensure method succeeds and returns a tuple containing existing instance and
        creation boolean indicator to False"""
        kwargs = {"firstname": self.author.firstname, "lastname": self.author.lastname}
        defaults = {"birth_city": self.new_author_birth_city}
        instance, created = AuthorService.get_or_create(defaults=defaults, **kwargs)
        assert instance == self.author
        assert created is False

    def test_get_or_create_with_non_existent_instance_return_tuple(self):
        """Ensure method succeeds and returns a tuple containing new instance and
        creation boolean indicator to True"""
        kwargs = {"firstname": self.author.firstname, "lastname": "New lastname"}
        defaults = {"birth_city": self.new_author_birth_city}
        instance, created = AuthorService.get_or_create(defaults=defaults, **kwargs)
        assert instance != self.author
        assert created is True

    def test_get_or_create_with_non_existent_instance_and_no_defaults_return_tuple(
        self,
    ):
        """Ensure method succeeds and returns a tuple containing new instance and
        creation boolean indicator to True"""
        kwargs = {"firstname": self.author.firstname, "lastname": "New lastname"}
        instance, created = AuthorService.get_or_create(**kwargs)
        assert instance != self.author
        assert created is True

    def test_get_or_create_with_non_existent_instance_and_missing_required_field_raise_integrity_error(  # noqa
        self,
    ):
        """Ensure method fails and raises IntegrityError exception"""
        kwargs = {"name": "book name 1"}
        defaults = {
            "series": self.new_book_series,
        }
        match = "NOT NULL constraint failed: django_app_book.author_id"
        with pytest.raises(IntegrityError, match=match):
            BookService.get_or_create(defaults=defaults, **kwargs)

    """
    update_or_create
    """

    def test_update_or_create_with_non_existent_instance_return_tuple(self):
        """Ensure method succeeds and returns a tuple containing new instance and
        creation boolean indicator to True"""
        kwargs = {"firstname": "different firstname", "lastname": self.author.lastname}
        defaults = {"birth_city": self.new_author_birth_city}
        instance, created = AuthorService.update_or_create(defaults=defaults, **kwargs)
        assert instance != self.author
        assert created is True

    def test_update_or_create_with_existing_instance_return_tuple(self):
        """Ensure method succeeds and returns a tuple containing updated existing
        instance and creation boolean indicator to False"""
        kwargs = {"firstname": self.author.firstname, "lastname": self.author.lastname}
        defaults = {"birth_city": self.new_author_birth_city}
        instance, created = AuthorService.update_or_create(defaults=defaults, **kwargs)
        assert instance == self.author
        assert instance.birth_city == self.new_author_birth_city
        assert created is False

    def test_update_or_create_with_existing_instance_and_no_defaults_return_tuple(self):
        """Ensure method succeeds and returns a tuple containing existing instance not
        updated and creation boolean indicator to False"""
        kwargs = {"firstname": self.author.firstname, "lastname": self.author.lastname}
        instance, created = AuthorService.update_or_create(**kwargs)
        assert instance == self.author
        # Nothing actually changed
        assert instance.birth_city == self.author.birth_city
        assert created is False

    def test_update_or_create_with_non_existent_instance_and_missing_required_field_raise_integrity_error(  # noqa
        self,
    ):
        """Ensure method fails and raises IntegrityError exception"""
        kwargs = {"name": "book name 1"}
        defaults = {
            "series": self.new_book_series,
        }
        match = "NOT NULL constraint failed: django_app_book.author_id"
        with pytest.raises(IntegrityError, match=match):
            BookService.update_or_create(defaults=defaults, **kwargs)

    # todofsc: finir les tests
