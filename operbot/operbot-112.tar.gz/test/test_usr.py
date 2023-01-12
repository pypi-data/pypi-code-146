# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"user"


import unittest


from operbot.irc import User


class TestUser(unittest.TestCase):

    def test_user(self):
        user = User()
        self.assertEqual(type(user), User)
