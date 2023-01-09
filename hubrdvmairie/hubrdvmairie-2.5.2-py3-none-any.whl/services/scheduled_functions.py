import logging

from unidecode import unidecode

from ..db.utils import get_all_editors, set_all_meeting_points


def run_daily_scheduled_functions():
    _logger = logging.getLogger("root")
    try:
        meeting_point_list = []
        for editor in get_all_editors():
            meeting_point_list += editor.get_managed_meeting_points()
        point_index = 201
        for point in meeting_point_list:
            point["id"] = str(point_index)
            point["decoded_city_name"] = (
                unidecode(point["city_name"])
                .replace(" ", "-")
                .replace("'", "-")
                .lower()
            )
            point_index += 1
        set_all_meeting_points(meeting_point_list)
    except Exception as daily_sch_e:
        _logger.error("Error while running daily scheduled functions : %s", daily_sch_e)
