import asyncio
import json
import logging
import os
import random
from datetime import date, datetime, timedelta

import httpx
from fastapi import WebSocket
from httpx import ConnectTimeout, ReadTimeout
from pydantic import ValidationError

from ..logging.app_logger import write_external_service_data
from ..services.mock_data import get_mock_managed_meeting_points, get_mock_slots
from .application import Application
from .municipality import Municipality


class Editor:
    slug: str
    name: str
    api_url: str
    _test_mode: bool
    status: bool

    def __init__(
        self, slug: str, name: str, api_url: str, test_mode: bool, status: bool = True
    ):
        self.slug = slug
        self.name = name
        self.api_url = api_url
        self._test_mode = test_mode
        self.status = status

    def get_managed_meeting_points(self):
        _logger = logging.getLogger("root")
        points = []
        if self._test_mode:
            points = get_mock_managed_meeting_points(self)
        else:
            try:
                headers = {
                    "x-hub-rdv-auth-token": os.environ.get(f"{self.slug}_auth_token")
                }
                response = httpx.get(
                    f"{self.api_url}/getManagedMeetingPoints",
                    headers=headers,
                    timeout=20,
                    follow_redirects=True,
                )
                write_external_service_data(_logger, response)
                if response.status_code in [200]:
                    if not self.status:
                        self.status = True
                    points = response.json()
                else:
                    raise Exception(f"Status code not handled : {response.status_code}")
            except Exception as get_meeting_points_e:
                if self.status:
                    self.status = False
                _logger.error(
                    "Error while getting meeting points for %s : %s",
                    self.name,
                    str(get_meeting_points_e),
                    extra={"extra_info": {"type": "app", "editor_name": self.name}},
                )

        valid_meeting_points = []
        for point in points:
            point["_editor_name"] = self.name
            point["_internal_id"] = str(point["id"])
            try:
                if point["zip_code"] in point["public_entry_address"]:
                    point["public_entry_address"] = point["public_entry_address"][
                        : point["public_entry_address"].index(point["zip_code"])
                    ].strip()
                Municipality.parse_obj(point)
                valid_meeting_points.append(point)
            except ValidationError as meeting_point_validation_e:
                _logger.error(
                    "Error while validating meeting point : %s \nError: %s",
                    point,
                    meeting_point_validation_e,
                    extra={"extra_info": {"type": "app", "editor_name": self.name}},
                )

        return valid_meeting_points

    async def get_available_time_slots(
        self, meeting_points, start_date, end_date, reason="CNI", documents_number=1
    ):
        _logger = logging.getLogger("root")
        result = {}
        editor_error = None
        response = None
        if self._test_mode:
            await asyncio.sleep(random.randint(3, 12))
            for meeting_point in meeting_points:
                meeting_point_slots = get_mock_slots(
                    meeting_point, start_date, end_date
                )
                result[meeting_point["_internal_id"]] = meeting_point_slots
        else:
            # this sleep is necessary to not block other async operations
            await asyncio.sleep(0.0000001)
            meeting_point_ids = [x["_internal_id"] for x in meeting_points]
            try:
                headers = {
                    "x-hub-rdv-auth-token": os.environ.get(f"{self.slug}_auth_token")
                }
                parameters = {
                    "start_date": start_date or date.today(),
                    "end_date": end_date or (date.today() + timedelta(days=150)),
                    "meeting_point_ids": meeting_point_ids,
                    "reason": reason,
                    "documents_number": documents_number,
                }
                async with httpx.AsyncClient(verify=False) as async_client:
                    response = await async_client.get(
                        f"{self.api_url}/availableTimeSlots",
                        headers=headers,
                        params=parameters,
                        timeout=15,
                        follow_redirects=True,
                    )
                    write_external_service_data(_logger, response)
                    if response.status_code in [200]:
                        if not self.status:
                            self.status = True
                        result = response.json()
                    else:
                        raise Exception(
                            f"Status code not handled : {response.status_code} : {response.reason_phrase}"
                        )
            except ReadTimeout:
                if self.status:
                    self.status = False
                _logger.error(
                    "Timeout while getting available time slots for %s",
                    self.name,
                    extra={"extra_info": {"type": "app", "editor_name": self.name}},
                )
            except ConnectTimeout:
                if self.status:
                    self.status = False
                _logger.error(
                    "Connexion Timeout while getting available time slots for %s",
                    self.name,
                    extra={"extra_info": {"type": "app", "editor_name": self.name}},
                )
            except Exception as get_meeting_points_e:
                if self.status:
                    self.status = False
                _logger.error(
                    "Error while getting available time slots for %s : %s",
                    self.name,
                    str(get_meeting_points_e),
                    extra={
                        "extra_info": {
                            "type": "app",
                            "parameters": {
                                "start_date": str(parameters["start_date"]),
                                "end_date": str(parameters["end_date"]),
                                "meeting_point_ids": parameters["meeting_point_ids"],
                                "reason": parameters["reason"],
                                "documents_number": parameters["documents_number"],
                            },
                            "editor_name": self.name,
                        }
                    },
                )
                editor_error = {"error": get_meeting_points_e, "editor": self.name}

        if (not start_date) and (not end_date):
            return result

        filtered_dates_result = {}
        try:
            for meeting_point_id in result:
                filtered_dates_result[meeting_point_id] = []
                for available_timeslot in result[meeting_point_id]:
                    timeslot_datetime = None
                    for datetime_format in ["%Y-%m-%dT%H:%MZ", "%Y-%m-%dT%H:%M:%S%z"]:
                        try:
                            timeslot_datetime = datetime.strptime(
                                available_timeslot["datetime"], datetime_format
                            )
                            if timeslot_datetime.tzinfo:
                                utcoffset = (
                                    timeslot_datetime.utcoffset().total_seconds()
                                    / 60
                                    / 60
                                )
                                timeslot_datetime = timeslot_datetime.replace(
                                    tzinfo=None
                                ) + timedelta(hours=utcoffset)
                            break
                        except ValueError:
                            pass
                    if (
                        (not timeslot_datetime)
                        or (start_date and (timeslot_datetime.date() < start_date))
                        or (end_date and (timeslot_datetime.date() > end_date))
                    ):
                        _logger.debug(
                            "[%s] DATE OUT OF RANGE : %s",
                            self.name,
                            str(timeslot_datetime),
                        )
                    else:
                        filtered_dates_result[meeting_point_id].append(
                            {
                                "datetime": timeslot_datetime.strftime(
                                    "%Y-%m-%dT%H:%M:%SZ"
                                ),
                                "callback_url": available_timeslot["callback_url"],
                            }
                        )
        except Exception as checking_date_filter_e:
            _logger.error(
                "[%s] Checking date filter error : %s",
                self.name,
                str(checking_date_filter_e),
                extra={"extra_info": {"type": "app", "editor_name": self.name}},
            )
            return {}
        return filtered_dates_result, editor_error

    async def search_slots_in_editor(
        self,
        meeting_points,
        start_date,
        end_date,
        reason="CNI",
        documents_number=1,
        websocket: WebSocket = None,
    ):
        editor_error = None
        editor_meeting_points = []
        editor_meeting_points_with_slots = []
        for meeting_point in meeting_points:
            if meeting_point["_editor_name"] == self.name:
                editor_meeting_points.append(meeting_point)
        if editor_meeting_points:
            slots, editor_error = await self.get_available_time_slots(
                editor_meeting_points, start_date, end_date, reason, documents_number
            )
            for meeting_point in editor_meeting_points:
                if (
                    meeting_point["_internal_id"] in slots
                    and slots[meeting_point["_internal_id"]]
                ):
                    meeting_point["available_slots"] = slots[
                        meeting_point["_internal_id"]
                    ]
                    editor_meeting_points_with_slots.append(meeting_point)
            if websocket:
                safe_editor_meeting_points_with_slots = []
                for editor_meeting_point_with_slots in editor_meeting_points_with_slots:
                    editor_meeting_point_with_slots_copy = (
                        editor_meeting_point_with_slots.copy()
                    )
                    if "_editor_name" in editor_meeting_point_with_slots_copy:
                        del editor_meeting_point_with_slots_copy["_editor_name"]
                    if "_internal_id" in editor_meeting_point_with_slots_copy:
                        del editor_meeting_point_with_slots_copy["_internal_id"]
                    safe_editor_meeting_points_with_slots.append(
                        editor_meeting_point_with_slots_copy
                    )
                json_string = json.dumps(
                    safe_editor_meeting_points_with_slots, default=str
                )
                await websocket.send_text(json_string)
        return editor_meeting_points_with_slots, editor_error

    async def search_meetings(self, application_ids):
        _logger = logging.getLogger("root")
        await asyncio.sleep(0.00001)
        meetings = {}
        if not self._test_mode:
            try:
                headers = {
                    "x-hub-rdv-auth-token": os.environ.get(f"{self.slug}_auth_token")
                }
                parameters = {"application_ids": application_ids}
                async with httpx.AsyncClient(verify=False) as async_client:
                    response = await async_client.get(
                        f"{self.api_url}/searchApplicationIds",
                        headers=headers,
                        params=parameters,
                        timeout=5,
                        follow_redirects=True,
                    )
                    write_external_service_data(_logger, response)
                    if response.status_code in [200]:
                        if not self.status:
                            self.status = True
                        meetings = response.json()
                    else:
                        raise Exception(
                            f"Status code not handled : {response.status_code} : {response.reason_phrase}"
                        )
            except Exception as search_meetings_e:
                if self.status:
                    self.status = False
                _logger.error(
                    "Error while seachring meetings by application ID for %s : %s",
                    self.name,
                    str(search_meetings_e),
                    extra={"extra_info": {"type": "app", "editor_name": self.name}},
                )
        else:
            await asyncio.sleep(random.randint(3, 5))

        valid_meetings = {}
        for applicationId in meetings:
            valid_meetings[applicationId] = []
            for meeting in meetings[applicationId]:
                try:
                    Application.parse_obj(meeting)
                    valid_meetings[applicationId].append(meeting)
                except ValidationError as meeting_validation_e:
                    _logger.error(
                        "Error while validating meeting : %s \nError: %s",
                        meeting,
                        meeting_validation_e,
                        extra={"extra_info": {"type": "app", "editor_name": self.name}},
                    )
        return valid_meetings


def init_all_editors():
    citopia_editor = Editor(
        "citopia", "Citopia", "https://pro.rendezvousonline.fr/api", False, True
    )
    synbird_editor = Editor(
        "synbird", "Synbird", "https://sync.synbird.com/ants", False, True
    )
    esii_editor = Editor(
        "esii", "ESII", "https://api.esii-orion.com/ants/api/public/1/ants", False, True
    )
    troov_editor = Editor("troov", "Troov", "https://qa-api.troov.com/api", False, True)
    rdv_360_editor = Editor(
        "rdv360", "RDV360", "http://ants.rdv360.com/api", False, True
    )
    ypok_editor = Editor(
        "ypok", "Ypok", "https://yservice.ypok.com/api.php", False, True
    )
    solocal_editor = Editor(
        "solocal", "Solocal", "https://api.solocal.com/v1/ants", False, True
    )
    smartagenda_editor = Editor(
        "smartagenda",
        "SmartAgenda",
        "https://interfaces.smartagenda.fr/partenaires/ants/",
        False,
        True,
    )
    numesia_editor = Editor(
        "numesia", "Numesia", "https://rdvs.numesia.fr/api", False, True
    )
    mega_editor = Editor("mega", "Mega", "https://www.mega.com", True, True)
    orionRDV_editor = Editor(
        "orionRDV", "OrionRDV", "https://orionrdv.com/", True, True
    )
    if os.environ.get("MOCK_EDITORS") in ["True", True]:
        return [citopia_editor, mega_editor, orionRDV_editor, synbird_editor]
    else:
        return [
            citopia_editor,
            synbird_editor,
            esii_editor,
            troov_editor,
            rdv_360_editor,
            ypok_editor,
            solocal_editor,
            smartagenda_editor,
            numesia_editor,
        ]
