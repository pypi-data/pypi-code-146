#
# Author: D.S. Ljugmark <spider@skuggor.se>, Modio AB
# SPDX-License-Identifier: AGPL-3.0-or-later
#
from snmp_lookup.selftests import (
    test_keys_look_ok,
    test_mibs_look_ok,
    test_points_look_ok,
    test_validators_look_ok,
    test_types_look_ok,
    test_labels_look_ok,
    test_oids_look_ok,
)


def test_selftest():
    test_keys_look_ok()
    test_mibs_look_ok()
    test_points_look_ok()
    test_validators_look_ok()
    test_types_look_ok()
    test_labels_look_ok()
    test_oids_look_ok()
