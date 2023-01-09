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

"""ValueObjectSupport tests."""

from __future__ import annotations

from typing import ForwardRef
from unittest import TestCase

from neom.new_ddd.shared import Field, ValueObjectSupport


class ValueObjectSupportTestCase(TestCase):
    """ValueObjectSupport test case."""

    def test_eq(self):
        """Test eq method."""

        class XValueObject(ValueObjectSupport[ForwardRef("XValueObject")]):
            name: Field[str]

        class YValueObject(XValueObject):
            age: Field[int]

        vo1 = XValueObject(name="X")
        vo2 = XValueObject(name="X")
        vo3 = YValueObject(name="X", age=3)

        self.assertEqual(vo1, vo2)
        self.assertEqual(vo2, vo1)
        self.assertNotEqual(vo2, vo3)
        self.assertNotEqual(vo3, vo2)

        self.assertTrue(vo1.SameValueAs(vo2))
        self.assertFalse(vo2.SameValueAs(vo3))

    def test_copy(self):
        """Test Copy method."""

        class Person(ValueObjectSupport[ForwardRef("XValueObject")]):
            name: Field[str]

        person = Person(name="Dummy")
        otherPerson = person.Copy()

        self.assertEqual(person.name, otherPerson.name)
        self.assertTrue(person.SameValueAs(otherPerson))
