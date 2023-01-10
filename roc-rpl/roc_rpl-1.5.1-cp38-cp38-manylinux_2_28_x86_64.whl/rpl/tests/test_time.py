#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Testing roc.rpl.time.py."""


from roc.rpl.time import Time
import numpy as np
from datetime import datetime

TIME_INSTANCE = Time()

def test_cuc_to_nanosec():
    """Test roc.rpl.time.Time.cuc_to_nanosec function."""
    # Create input RPW CUC time
    in_time = np.empty([3, 2], dtype=np.uint32)
    # RPW CUC time at 2000-01-02 00:00:00.0762939453125
    in_time[0, :] = [86400, 5000]
    # RPW CUC time at 2010-01-02 00:00:00.9918212890625
    in_time[1, :] = [315619200, 65000]
    # RPW CUC time at 2017-01-02 00:00:00.0030517578125
    in_time[2, :] = [536630400, 200]

    # Create expected time
    exp_time = np.empty([3], dtype=np.uint64)
    exp_time[0] = 86400076293945
    exp_time[1] = 315619200991821289
    exp_time[2] = 536630400003051757

    out_time = Time.cuc_to_nanosec(in_time)

    for i, etime in enumerate(exp_time):
        # Assert at the microsecond resolution
        assert int(out_time[i]/1000.) == int(etime/1000.)

def test_cuc_to_microsec():
    """Test roc.rpl.time.Time.cuc_to_microsec function."""
    # Create input RPW CUC time
    in_time = np.empty([3, 2], dtype=np.uint32)
    # RPW CUC time at 2000-01-02 00:00:00.0762939453125
    in_time[0, :] = [86400, 5000]
    # RPW CUC time at 2010-01-02 00:00:00.9918212890625
    in_time[1, :] = [315619200, 65000]
    # RPW CUC time at 2017-01-02 00:00:00.0030517578125
    in_time[2, :] = [536630400, 200]

    # Create expected time
    exp_time = np.empty([3], dtype=np.uint64)
    exp_time[0] = 86400076294
    exp_time[1] = 315619200991821
    exp_time[2] = 536630400003052

    out_time = Time.cuc_to_microsec(in_time)

    for i, etime in enumerate(exp_time):
        # Assert at the microsecond resolution
        assert int(out_time[i]/1000.) == int(etime/1000.)

def test_obt_to_tt2000_nospice():
    """
    Test roc.rpl.time.Time.obt_to_utc function
    with to_tt2000=True and no_spice=True options.
    """
    # Create input RPW CUC time
    in_time = np.empty([3, 2], dtype=np.uint32)
    # RPW CUC time at 2000-01-02 00:00:00.0762939453125
    in_time[0, :] = [86400, 5000]
    # RPW CUC time at 2010-01-02 00:00:00.9918212890625
    in_time[1, :] = [315619200, 65000]
    # RPW CUC time at 2017-01-02 00:00:00.0030517578125
    in_time[2, :] = [536630400, 200]

    # Create expected time
    exp_time = np.empty([3], dtype=int)
    exp_time[0] = 43264260293
    exp_time[1] = 315576065175821
    exp_time[2] = 536587264187051

    TIME_INSTANCE.no_spice = True
    out_time = TIME_INSTANCE.obt_to_utc(in_time, to_tt2000=True)

    for i, etime in enumerate(exp_time):
        # Assert at the microsecond resolution
        assert int(out_time[i]/1000.0) == etime

def test_cuc_to_scet():
    """
    Test roc.rpl.time.Time.cuc_to_scet.

    :return:
    """

    # Create input RPW CUC time
    in_time = np.empty([2, 2], dtype=np.uint32)
    in_time[0, :] = [549570899, 64512]
    in_time[1, :] = [315619200, 65000]

    # Create expected time
    exp_time = np.empty([2], dtype=np.float64)
    exp_time[0] = 549570899.984375
    exp_time[1] = 315619200.9918213

    out_time = Time.cuc_to_scet(in_time)

    for i, etime in enumerate(exp_time):
        assert out_time[i] == etime


def test_obt_to_utc_nospice():
    """
    Test roc.rpl.time.Time.obt_to_utc without using SPICE.

    :return:
    """

    expected = datetime(2000, 1, 1, 0, 0, 0, 488)

    input = (0, 32, 1)

    TIME_INSTANCE.no_spice = True
    utc_time = TIME_INSTANCE.obt_to_utc([input], to_datetime=True)[0]

    assert utc_time == expected
