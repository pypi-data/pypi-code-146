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

"""ValueObject tests."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import ForwardRef, cast
from unittest import TestCase

from neom.new_ddd.shared import Field, ValueObject


class ValueObjectDeclarationTestCase(TestCase):
    """ValueObject declaration test case."""

    def test_primitives(self):
        """Test most common value object definition."""

        class Person(ValueObject[ForwardRef("Person")]):
            """Dummy."""

            name: Field[str]
            age: Field[int]
            birth: Field[datetime]

            def SameValueAs(self, other: Person) -> bool:
                return (
                    self.name == other.name
                    and self.age == other.age
                    and self.birth == other.birth
                )

            def Copy(self) -> ForwardRef("Person"):
                return Person(name=self.name, age=self.age, birth=self.birth)

        person = Person(name="Bruce Wayne", age=9, birth=datetime(2010, 1, 2))

        self.assertIsInstance(person, Person)
        self.assertEqual(person.name, "Bruce Wayne")
        self.assertEqual(person.age, 9)
        self.assertEqual(person.birth, datetime(2010, 1, 2))
        self.assertTrue(person.SameValueAs(person))
        self.assertTrue(person.SameValueAs(person.Copy()))

    def test_inheritance(self):
        """Test value object inheritance."""

        class PersonalInfo(ValueObject):
            """Dummy."""

            name: Field[str]
            age: Field[int]

            def SameValueAs(self, other: PersonalInfo) -> bool:
                return self.name == other.name and self.age == other.age

            def Copy(self) -> ForwardRef("PersonalInfo"):
                return PersonalInfo(name=self.name, age=self.age)

        class Person(PersonalInfo):
            """Dummy."""

            birth: Field[datetime]

            def SameValueAs(self, other: Person) -> bool:
                return (
                    super().SameValueAs(cast(PersonalInfo, other))
                    and self.birth == other.birth
                )

            def Copy(self) -> ForwardRef("Person"):
                personalInfo = super().Copy()
                return Person(
                    name=personalInfo.name,
                    age=personalInfo.age,
                    birth=self.birth,
                )

        person = Person(name="Bruce Wayne", age=9, birth=datetime(2010, 1, 2))

        self.assertIsInstance(person, Person)
        self.assertEqual(person.name, "Bruce Wayne")
        self.assertEqual(person.age, 9)
        self.assertEqual(person.birth, datetime(2010, 1, 2))
        self.assertTrue(person.SameValueAs(person))
        self.assertTrue(person.SameValueAs(person.Copy()))


class ValueObjectMethodsTestCase(TestCase):
    """ValueObject methods test case."""

    def setUp(self):
        class Person(ValueObject[ForwardRef("Person")]):
            """Dummy."""

            name: Field[str]
            age: Field[int]
            birth: Field[datetime]

            def SameValueAs(self, other: Person) -> bool:
                return (
                    self.name == other.name
                    and self.age == other.age
                    and self.birth == other.birth
                )

            def Copy(self) -> ForwardRef("Person"):
                return deepcopy(self)

        self.person = Person

    def test_same_value_as(self):
        """Test SameValueAs method."""
        p1 = self.person(name="Bruce Wayne", age=9, birth=datetime(2010, 1, 2))
        p2 = self.person(name="Bruce Wayne", age=9, birth=datetime(2010, 1, 2))
        self.assertTrue(p1.SameValueAs(p2))

    def test_copy(self):
        """Test Copy method."""
        p1 = self.person(name="Bruce Wayne", age=9, birth=datetime(2010, 1, 2))
        p2 = p1.Copy()

        # TODO: improve this test to verify deep copy

        self.assertIs(p1.name, p2.name)
        self.assertEqual(p1.name, p2.name)

        self.assertIs(p1.age, p2.age)
        self.assertEqual(p1.age, p2.age)

        self.assertIsNot(p1.birth, p2.birth)
        self.assertEqual(p1.birth, p2.birth)


class ValueObjectBackCompatibilityTestCase(TestCase):
    """ValueObject back compatibility test case."""

    def test_auto_fields(self):
        """Test SameValueAs method."""

        class Person(ValueObject[ForwardRef("Person")]):
            """Dummy."""

            name: str
            age: int
            birth: datetime

            def SameValueAs(self, other: Person) -> bool:
                return (
                    self.name == other.name
                    and self.age == other.age
                    and self.birth == other.birth
                )

            def Copy(self) -> ForwardRef("Person"):
                return Person(name=self.name, age=self.age, birth=self.birth)

        person = Person(name="Bruce Wayne", age=9, birth=datetime(2010, 1, 2))

        self.assertIsInstance(person, Person)
        self.assertEqual(person.name, "Bruce Wayne")
        self.assertEqual(person.age, 9)
        self.assertEqual(person.birth, datetime(2010, 1, 2))
        self.assertTrue(person.SameValueAs(person))
        self.assertTrue(person.SameValueAs(person.Copy()))
