#!/usr/bin/env python

# stdlib imports
import pathlib

# third party imports
from configobj import ConfigObj

from strec.sm_probs import get_probs
from strec.subtype import SubductionSelector, get_event_details


def _test_get_region_probs():
    select_file = pathlib.Path.home() / ".strec" / "select.conf"
    config = ConfigObj(str(select_file))
    eventid = "ak0219neiszm"
    selector = SubductionSelector(verbose=False, prefix="")
    lat, lon, depth, tensor_params = selector.getOnlineTensor(eventid)
    details = get_event_details(eventid)
    strec_info = selector.getSubductionTypeByID(eventid)
    probs = get_probs(details["magnitude"], depth, strec_info, config)
    x = 1


if __name__ == "__main__":
    test_get_region_probs()
