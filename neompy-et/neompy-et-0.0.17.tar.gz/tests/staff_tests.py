# Copyright 2022 neomadas-dev
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#   3. Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Staff tests."""

from __future__ import annotations

from unittest import TestCase

from neom.new_ddd import staff


class PhoneTestCase(TestCase):
    def test_creation(self):
        phone = staff.Phone(country=51, area=123, number=1234567)

        self.assertEqual(51, phone.country)
        self.assertEqual(123, phone.area)
        self.assertEqual(1234567, phone.number)


class MobileTestCase(TestCase):
    def test_creation(self):
        mobile = staff.Mobile.Make("(+51) 987-654-321")
        self.assertEqual(mobile.country, 51)
        self.assertEqual(mobile.area, None)
        self.assertEqual(mobile.number, 987654321)

    def test_format(self):
        mobile = staff.Mobile.Make("(+51) 987-654-321")
        self.assertEqual(str(mobile), "(+51) 987-654-321")

    def test_bad_creation(self):
        with self.assertRaisesRegex(
            ValueError,
            r"Invalid mobile phone \+51987654321. Use \(\+xx\) xxx-xxx-xxx.",
        ):
            staff.Mobile.Make("+51987654321")


class EmailTestCase(TestCase):
    def test_creation_and_format(self):
        email = staff.Email(address="dummy@staff.ui")
        self.assertEqual(str(email), "dummy@staff.ui")

    def test_validate(self):
        email = staff.Email(address="dummy.at.staff.ui")
        with self.assertRaisesRegex(
            ValueError, r"Invalid email address format dummy\.at\.staff\.ui"
        ):
            email.Validate()
