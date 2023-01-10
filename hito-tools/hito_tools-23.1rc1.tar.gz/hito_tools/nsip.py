# Module to handle NSIP interaction
import datetime
import re
from typing import Dict, List

import pandas as pd

# FIXME: would be better to allow proper verification of the host certificate...
import requests
import simplejson as json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .exceptions import ConfigMissingParam, NSIPPeriodAmbiguous, NSIPPeriodMissing

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Define exit code in case of errors
EXIT_STATUS_NSIP_API_PARAMS = 10
EXIT_STATUS_NSIP_API_ERROR = 11

# Define some constants related to HTTP
HTTP_STATUS_OK = 200
HTTP_STATUS_CREATED = 201
HTTP_STATUS_ACCEPTED = 202
HTTP_STATUS_NO_CONTENT = 204
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_UNAUTHORIZED = 401
HTTP_STATUS_FORBIDDEN = 403
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_CONFLICT = 409

# Required config params describing the NSIP API in the configuration file
# The key is the API subpart and the value a set of required parameters describing the sub-urls.
# 'base_url' is an implicitly required parameter for each API part.
NSIP_API_REQUIRED_CONFIG = {
    "agent_api": ["declaration_add", "declaration_delete", "declaration_update"],
    "institute_api": ["declaration_period_list"],
    "lab_api": ["agent_list", "declaration_list"],
}

DECLARATION_EXISTS_PATTERN = re.compile(
    r'"A declaration (?P<decl_id>\d+) already exists for this agent.*"$'
)
DECLARATION_ADDED_PATTERN = re.compile(r'"Declaration (?P<decl_id>\d+) successfully created"$')


class NSIPRequestFailure(Exception):
    def __init__(self, code, url):
        self.msg = f"NSIP agent API request failure (Status={code}, URL={url})"
        self.status = EXIT_STATUS_NSIP_API_ERROR

    def __str__(self):
        return repr(self.msg)


class NSIPConnection:
    def __init__(
        self,
        server_url: str,
        bearer_token: Dict[str, str],
        agent_api: str,
        lab_api: Dict[str, str],
        institute_api: Dict[str, str],
    ) -> None:
        self.server_url = server_url
        self.token = bearer_token
        self.agent_api = agent_api
        self.institute_api = institute_api
        self.lab_api = lab_api

    def get_agent_list(self, context: str = "NSIP"):
        """
        Retrieve NSIP agents from NSIP API and return a dict built from the retrieved JSON

        :param context: either 'NSIP' (all agents presents at least one day during the semester)
                        or 'DIRECTORY' (only agents with an active contract)
        :return: dict representing the JSON anwser
        """

        url = f"{self.server_url}{self.lab_api['base_url']}{self.lab_api['agent_list']}"
        r = requests.get(
            url,
            headers={"Authorization": f"Bearer {self.token}"},
            params={"context": context},
        )
        if r.status_code != HTTP_STATUS_OK:
            raise NSIPRequestFailure(r.status_code, url)

        agents = r.json()

        return agents

    def update_agent(
        self,
        reseda_email: str,
        team_id: str = None,
        email: str = None,
        phones: List[str] = None,
        offices: List[str] = None,
    ) -> int:
        """
        Update agent attributes. Every attribute can be omitted if it should not
        be modified. reseda_email is used to identify the user to modify and is
        the only required parameter. An agent cannot be added through the API, it
        has to exist before.

        :param reseda_email: the user resedaEmail, used to identify the user
        :param team_id: ID of user's new team
        :param email: user's new email
        :param phones: user's new phone list
        :param offices: user's new office list
        :return: status (0 for successful update, a positive value if an error occured),
                 http_status, http_reason
        """

        params = {"emailReseda": reseda_email, "context": "DIRECTORY"}
        url = f"{self.server_url}{self.agent_api['base_url']}{self.agent_api['agent_update']}"
        if team_id is not None:
            params["teamId"] = team_id
        if email is not None:
            params["contactEmail"] = email
        if phones is not None:
            # To clear the phones, an empty string must be passed to work around an API error
            if len(phones) == 0:
                phones.add("")
            params["phoneNumbers"] = json.dumps(phones, iterable_as_array=True)
        if offices is not None:
            # To clear the offices, an empty string must be passed to work around an API error
            if len(offices) == 0:
                offices.add("")
            params["offices"] = json.dumps(offices, iterable_as_array=True)
        r = requests.put(url, headers={"Authorization": f"Bearer {self.token}"}, params=params)
        if r.content:
            reason = r.content.decode("utf-8")
        else:
            reason = ""

        if r.status_code == HTTP_STATUS_OK:
            status = 0
        else:
            status = 1
        return status, r.status_code, reason

    def update_declaration(
        self,
        email: str,
        project_id: str,
        project_type: bool,
        time: int,
        validation_date: datetime.date = None,
    ) -> int:
        """
        Add or update a project declaration for a user specified by its RESEDA email

        :param email: RESEDA email of the selected user
        :param project_id: ID of the selected project
        :param project_type: if True, it is a project, else it is a reference (other activities)
        :param time: time spent on the project in the unit appropriate for the project (hour or
                     week)
        :param validation_date: validation date
        :return: status (0 for successful add, -1 for successful update, positive value if errors),
                 http_status if errors else declaration ID added/modified, http_reason
        """

        url = f"{self.server_url}{self.agent_api['base_url']}{self.agent_api['declaration_add']}"
        if project_type:
            params = {"projectId": int(project_id), "referenceId": ""}
        else:
            params = {"projectId": "", "referenceId": int(project_id)}
        params["context"] = "NSIP"
        params["emailReseda"] = email
        params["time"] = time
        if validation_date:
            validation_date_str = validation_date.date().isoformat()
            params["managerValidationDate"] = validation_date_str
        r = requests.post(url, headers={"Authorization": f"Bearer {self.token}"}, params=params)
        if r.content:
            reason = r.content.decode("utf-8")
        else:
            reason = ""

        if r.status_code == HTTP_STATUS_OK:
            m = DECLARATION_ADDED_PATTERN.match(reason)
            if m:
                declaration_id = m.group("decl_id")
            else:
                print(f"ERROR: unable to extract declaration number from request reason ({reason})")
            status = 0

        elif r.status_code == HTTP_STATUS_FORBIDDEN:
            # If http status is Forbidden, parse the associated message. If it is the expected
            # message for an already existing declaration, retrieve the declaration ID and
            # update it.
            m = DECLARATION_EXISTS_PATTERN.match(reason)
            if m:
                declaration_id = m.group("decl_id")
                url = (
                    f"{self.server_url}{self.agent_api['base_url']}"
                    f"{self.agent_api['declaration_update']}"
                )
                params = {"id": declaration_id, "time": time, "context": "NSIP"}
                if validation_date_str:
                    params["managerValidationDate"] = validation_date_str
                status = -1
                r = requests.put(
                    url,
                    headers={"Authorization": f"Bearer {self.token}"},
                    params=params,
                )

        if r.status_code == HTTP_STATUS_OK:
            return status, declaration_id, reason
        else:
            return 1, r.status_code, reason

    def get_declaration_period_id(self, period_date: datetime):
        """
        Return the declaration ID for the declaration period matching a given date (the date must
        be included in the period.

        :param period_date: date that must be inside the period
        :return: declaration period ID
        """

        url = (
            f"{self.server_url}{self.institute_api['base_url']}"
            f"{self.institute_api['declaration_period_list']}"
        )

        r = requests.get(url, headers={"Authorization": f"Bearer {self.token}"})
        if r.status_code != HTTP_STATUS_OK:
            raise NSIPRequestFailure(r.status_code, url)

        periods = pd.read_json(r.content.decode())
        periods["startDateDeclaration"] = pd.to_datetime(periods.startDateDeclaration)
        periods["endDateDeclaration"] = pd.to_datetime(periods.endDateDeclaration)
        selected_period = periods.loc[
            (periods.startDateDeclaration <= period_date)
            & (periods.endDateDeclaration > period_date)
        ]
        if len(selected_period) == 0:
            raise NSIPPeriodMissing(period_date)
        elif len(selected_period) > 1:
            raise NSIPPeriodAmbiguous(period_date, len(selected_period))

        return selected_period.iloc[0]["id"]

    def get_declarations(self, period_date: datetime):
        """
        Return the NSIP declaration list for the declaration period matching a given date (the
        date must be included in the period).

        :param period_date: date that must be inside the period
        :return: declaration list as a dict
        """

        period_id = self.get_declaration_period_id(period_date)

        url = f"{self.server_url}{self.lab_api['base_url']}{self.lab_api['declaration_list']}"
        params = {"idPeriod": period_id}
        r = requests.get(url, headers={"Authorization": f"Bearer {self.token}"}, params=params)
        if r.status_code != HTTP_STATUS_OK:
            raise NSIPRequestFailure(r.status_code, url)

        declarations = r.json()

        return declarations

    def get_activities(self, project_activity: bool):
        """
        Return the list of projects for the laboratory defined in NSIP

        :param project_activity: true for projects, false for other activities
        :return: activity list as a list
        """

        if project_activity:
            activity_api = self.lab_api["project_list"]
        else:
            activity_api = self.lab_api["reference_list"]

        url = f"{self.server_url}{self.lab_api['base_url']}{activity_api}"
        r = requests.get(
            url,
            headers={"Authorization": f"Bearer {self.token}"},
        )
        if r.status_code != HTTP_STATUS_OK:
            raise NSIPRequestFailure(r.status_code, url)

        activities = r.json()

        return activities

    def get_teams(self):
        """
        Return the list of lab teams as a list of dict

        :return: list
        """

        url = f"{self.server_url}{self.lab_api['base_url']}{self.lab_api['team_list']}"
        r = requests.get(url, headers={"Authorization": f"Bearer {self.token}"})
        if r.status_code != HTTP_STATUS_OK:
            raise NSIPRequestFailure(r.status_code, url)

        teams = r.json()

        return teams


def check_nsip_config(nsip_config) -> bool:
    """
    Check the NSIP parameters and return True if it os or raise an exception otherwise

    :param nsip_config: dict containing NSIP parameters
    :return:
    """

    required_keys = set(NSIP_API_REQUIRED_CONFIG.keys())
    required_keys.update(["server_url", "token"])
    for k in required_keys:
        if k not in nsip_config:
            raise ConfigMissingParam(f"nsip/{k}")
        if k in NSIP_API_REQUIRED_CONFIG:
            required_subkeys = set(NSIP_API_REQUIRED_CONFIG[k])
            required_subkeys.add("base_url")
            for sk in required_subkeys:
                if sk not in nsip_config[k]:
                    raise ConfigMissingParam(f"nsip/{k}/{sk}")

    return True


def nsip_session_init(nsip_config):
    """
    Initialize the NSIP session, using the configuration parameters. It is valid for an
    application not to initalize all APIs.

    :param nsip_config: dict containing the NSIP configuration
    :return: a NSIPConnection object
    """

    if "agent_api" in nsip_config:
        agent_api = nsip_config["agent_api"]
    else:
        agent_api = None

    if "lab_api" in nsip_config:
        lab_api = nsip_config["lab_api"]
    else:
        lab_api = None

    if "institute_api" in nsip_config:
        institute_api = nsip_config["institute_api"]
    else:
        institute_api = None

    return NSIPConnection(
        nsip_config["server_url"],
        nsip_config["token"],
        agent_api,
        lab_api,
        institute_api,
    )
