"""
Test checks for access to fleetfinder
"""

# Standard Library
from http import HTTPStatus

# Django
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

# AA Fleet Finder
from fleetfinder.tests.utils import create_fake_user


class TestAccess(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up groups and users
        """

        super().setUpClass()

        cls.group = Group.objects.create(name="Superhero")

        # User cannot access fleetfinder
        cls.user_1001 = create_fake_user(1001, "Peter Parker")

        # User can access fleetfinder
        cls.user_1002 = create_fake_user(
            1002, "Bruce Wayne", permissions=["fleetfinder.access_fleetfinder"]
        )

    def test_has_no_access(self):
        """
        Test that a user without access get a 302
        :return:
        """

        # given
        self.client.force_login(self.user_1001)

        # when
        res = self.client.get(reverse("fleetfinder:dashboard"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.FOUND)

    def test_has_access(self):
        """
        Test that a user with access get to see it
        :return:
        """

        # given
        self.client.force_login(self.user_1002)

        # when
        res = self.client.get(reverse("fleetfinder:dashboard"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.OK)
