# -*- coding: utf-8 -*-
# BSD 3-Clause License
#
# Copyright (c) 2020-2022, Faster Speeding
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# pyright: reportPrivateUsage=none
# This leads to too many false-positives around mocks.

import tanjun


def test_aliases():
    assert set(tanjun.utilities.__all__) == {
        "ALL_PERMISSIONS",
        "DM_PERMISSIONS",
        "calculate_everyone_permissions",
        "calculate_permissions",
        "fetch_everyone_permissions",
        "fetch_permissions",
    }
    assert tanjun.utilities.ALL_PERMISSIONS is tanjun.permissions.ALL_PERMISSIONS
    assert tanjun.utilities.DM_PERMISSIONS is tanjun.permissions.DM_PERMISSIONS
    assert tanjun.utilities.calculate_everyone_permissions is tanjun.permissions.calculate_everyone_permissions
    assert tanjun.utilities.calculate_permissions is tanjun.permissions.calculate_permissions
    assert tanjun.utilities.fetch_everyone_permissions is tanjun.permissions.fetch_everyone_permissions
    assert tanjun.utilities.fetch_permissions is tanjun.permissions.fetch_permissions
