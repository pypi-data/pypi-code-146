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

"""And specification tests."""

from __future__ import annotations

from unittest import TestCase

from neom.new_ddd.shared_.and_specification import AndSpecification

from .spec_common.false_spec import FalseSpec
from .spec_common.true_spec import TrueSpec


class AndSpecificationTestCase(TestCase):
    def test_and_is_satisfied_by(self):
        trueSpec = TrueSpec()
        falseSpec = FalseSpec()

        andSpecification = AndSpecification[object](trueSpec, trueSpec)
        self.assertTrue(andSpecification.IsSatisfiedBy(object()))

        andSpecification = AndSpecification[object](falseSpec, trueSpec)
        self.assertFalse(andSpecification.IsSatisfiedBy(object()))

        andSpecification = AndSpecification[object](trueSpec, falseSpec)
        self.assertFalse(andSpecification.IsSatisfiedBy(object()))

        andSpecification = AndSpecification[object](falseSpec, falseSpec)
        self.assertFalse(andSpecification.IsSatisfiedBy(object()))
