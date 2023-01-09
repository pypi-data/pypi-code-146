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

import copy
import pickle
from unittest import TestCase

from neom.core import ioc


class IocTestCase(TestCase):
    def test_manager_wire(self):
        ioc.manager.wire(object, None)
        self.assertIn(object, ioc.manager.pairs)

    def test_autowire_deprecated(self):
        ioc.manager.wire(object, str)

        @ioc.AutoWire
        class Dummy:
            foo: object

        dummy = Dummy()
        self.assertIsInstance(dummy.foo, str)

    def test_wireable(self):
        ioc.manager.wire(object, str)

        @ioc.Wireable
        class Dummy:
            foo: ioc.Wired[object]

        dummy = Dummy()
        self.assertIsInstance(dummy.foo, str)

    def test_wire(self):
        ioc.manager.wire(object, str)

        @ioc.wire
        def dummy(foo: ioc.Wired[object]):
            return foo

        self.assertIsInstance(dummy(), str)

    def test_provider_not_subclass(self):
        with self.assertRaises(TypeError) as cm:
            ioc.Provider("", (), None)
        self.assertEqual(
            str(cm.exception),
            "Cannot subclass <class 'neom.core.ioc.Provider'>",
        )

    def test_provider_not_init_subclass(self):
        with self.assertRaises(TypeError) as cm:

            class Dummy(ioc.Provider):
                pass

        self.assertEqual(str(cm.exception), "Cannot subclass provider classes")

    def test_provider_not_init(self):
        with self.assertRaises(TypeError) as cm:
            ioc.Wired()
        self.assertEqual(str(cm.exception), "Cannot instantiate ioc.Wired")

    def test_provider_instance(self):
        with self.assertRaises(TypeError) as cm:
            isinstance(object(), ioc.Wired)
        self.assertEqual(
            str(cm.exception), "ioc.Wired cannot be used with isinstance()"
        )

    def test_provider_subclass(self):
        with self.assertRaises(TypeError) as cm:
            issubclass(object, ioc.Wired)
        self.assertEqual(
            str(cm.exception), "ioc.Wired cannot be used with issubclass()"
        )

    def test_provider_copy(self):
        self.assertIs(ioc.Wired, copy.copy(ioc.Wired))

    def test_provider_deepcopy(self):
        self.assertIs(ioc.Wired, copy.deepcopy(ioc.Wired))

    def test_provider_hash(self):
        self.assertEqual(hash(ioc.Wired), hash(ioc.Wired))

    def test_provider_eq(self):
        dummy = ioc.Provider("Wired", "")
        self.assertEqual(ioc.Wired, dummy)

    def test_provider_reduce(self):
        self.assertIs(pickle.loads(pickle.dumps(ioc.Wired)), ioc.Wired)
