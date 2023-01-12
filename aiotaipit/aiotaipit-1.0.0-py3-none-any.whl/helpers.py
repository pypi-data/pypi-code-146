"""Helpers and utils."""

from const import REGIONS, UNKNOWN


def get_region_name(region_id: int) -> str:
    region_name = REGIONS.get(region_id, f'{UNKNOWN} <{region_id}>')
    return region_name
