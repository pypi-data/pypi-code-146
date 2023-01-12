# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import re
from pybpodgui_api.models.task.task_io import TaskIO

logger = logging.getLogger(__name__)


class TaskFile(TaskIO):
    """ Represents a state machine """

    def find_task_variables_from_file(self):

        task_variables = []

        # match any line begining with v. and get variable name and value until end of line or # sign
        pattern = "^v\.(?P<vname>\w+)\s*\=\s*(?P<vvalue>.*(?=#)|.*)"

        with open(self.path, "r") as file:
            file_content = file.read()

        for v_name in re.findall(pattern, file_content, re.MULTILINE):
            if not v_name in [var_name for var_name in task_variables]:
                logger.debug("Find variable name: %s", v_name)
                task_variables.append(v_name)  # ignore variables value at this point

        return task_variables

    def find_states_from_file(self, start=1):
        return self.find_pattern(start, search_match="states")

    def find_events_from_file(self, start=1):
        return self.find_pattern(start, search_match="events")

    def find_pattern(self, start=1, search_match=None):

        matches = {}

        regex = r"{0}\s*=\s*\[(.+?)(?=\])".format(search_match)
        try:
            found_matches = re.findall(regex, self.code, flags=re.DOTALL)[0]
        except:
            logger.warning("Invalid {0} format or no {0} defined".format(search_match))
            return matches

        for idx, read_state in enumerate(found_matches.split(','), start=start):
            try:
                state_id = str(read_state.replace("'", ""))  # if it is string
            except:
                state_id = str(read_state.replace("'", ""))  # if it is a var

            matches[idx] = state_id.strip()

        logger.debug("Found %s: %s", search_match, matches)

        return matches
