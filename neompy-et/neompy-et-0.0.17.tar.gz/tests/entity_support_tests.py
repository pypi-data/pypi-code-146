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

"""EntitySupport tests."""

from __future__ import annotations

from typing import ForwardRef
from unittest import TestCase

from neom.new_ddd.shared import EntitySupport, Identity


class EntitySupportTestCase(TestCase):
    """EntitySupport test case."""

    def test_no_identity(self):
        entity = self.NoIdentityEntity()
        with self.assertRaisesRegex(
            TypeError, "Must have a unique identity field"
        ):
            entity.Identity()

    def test_two_identity(self):
        entity = self.TwoIdentityEntity(
            name1="Bruce Banner", name2="Bruce Banner"
        )
        with self.assertRaisesRegex(
            TypeError, "Only one field can be an identity"
        ):
            entity.Identity()

    def test_ok_identity(self):
        entity = self.IdentityEntity(name="Bruce Banner")
        self.assertEqual("Bruce Banner", entity.Identity())

    def test_same_identity(self):
        e1 = self.IdentityEntity(name="Bruce Banner")
        e2 = self.IdentityEntity(name="Bruce Banner")
        e3 = self.IdentityEntity(name="Bruce Wayne")

        self.assertTrue(e1.SameIdentityAs(e2))
        self.assertFalse(e2.SameIdentityAs(e3))

        self.assertEqual(e1, e2)
        self.assertNotEqual(e2, e3)

        self.assertEqual(hash(e1), hash(e2))
        self.assertNotEqual(hash(e2), hash(e3))

    class NoIdentityEntity(EntitySupport[ForwardRef("NoIdentityEntity"), str]):
        pass

    class IdentityEntity(EntitySupport[ForwardRef("IdentityEntity"), str]):
        name: Identity[str]

    class TwoIdentityEntity(
        EntitySupport[ForwardRef("TwoIdentityEntity"), str]
    ):
        name1: Identity[str]
        name2: Identity[str]
