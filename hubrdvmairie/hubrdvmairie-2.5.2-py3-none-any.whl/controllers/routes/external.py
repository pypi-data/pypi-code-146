import asyncio
import os
from datetime import date
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import Required, constr
from slowapi import Limiter
from slowapi.util import get_remote_address

from ...db.utils import get_all_editors, get_all_meeting_points
from ...models.municipality import Municipality
from ...services.mock_data import get_mock_slots
from ..dependencies.auth_token import verify_auth_token

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/getManagedMeetingPoints",
    response_model=List[Municipality],
    responses={
        200: {
            "description": "Municipalities list retrieved successfully!",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "201",
                            "name": "Mairie ANNEXE LILLE-SECLIN",
                            "longitude": 3.0348016639327,
                            "latitude": 50.549140395451,
                            "public_entry_address": "89 RUE ROGER BOUVRY",
                            "zip_code": "59113",
                            "city_name": "SECLIN",
                            "website": "http://www.ville-seclin.fr",
                            "city_logo": "https://www.ville-seclin.fr/images/logo-ville-seclin/logo_ville_de_seclin.png",
                        }
                    ]
                }
            },
        },
        "401": {
            "description": "User not authorized",
            "content": {
                "application/json": {"example": "X-HUB-RDV-AUTH-TOKEN header invalid"}
            },
        },
    },
    dependencies=[Depends(verify_auth_token)],
)
@limiter.limit("30/minute")
def get_managed_meeting_points(
    request: Request,
) -> Any:
    """
    Get the list of Meeting Points we handle.
    """

    return get_all_meeting_points()


@router.get(
    "/availableTimeSlots",
    responses={
        200: {
            "description": "Available time slots successfully found",
            "content": {
                "application/json": {
                    "example": {
                        "506": [
                            {
                                "datetime": "2022-12-19T10:00Z",
                                "callback_url": "http://www.ville-seclin.fr/rendez-vous/passeports?date=2022-12-19T10:00Z",
                            },
                            {
                                "datetime": "2022-12-19T10:20Z",
                                "callback_url": "http://www.ville-seclin.fr/rendez-vous/passeports?date=2022-12-19T10:20Z",
                            },
                            {
                                "datetime": "2022-12-19T10:40Z",
                                "callback_url": "http://www.ville-seclin.fr/rendez-vous/passeports?date=2022-12-19T10:40Z",
                            },
                            {
                                "datetime": "2022-12-19T11:00Z",
                                "callback_url": "http://www.ville-seclin.fr/rendez-vous/passeports?date=2022-12-19T11:00Z",
                            },
                        ],
                        "7789": [
                            {
                                "datetime": "2022-12-19T10:00Z",
                                "callback_url": "http://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud/rendez-vous/passeports?date=2022-12-19T10:00Z",
                            },
                            {
                                "datetime": "2022-12-19T10:20Z",
                                "callback_url": "http://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud/rendez-vous/passeports?date=2022-12-19T10:20Z",
                            },
                            {
                                "datetime": "2022-12-19T10:40Z",
                                "callback_url": "http://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud/rendez-vous/passeports?date=2022-12-19T10:40Z",
                            },
                            {
                                "datetime": "2022-12-19T11:00Z",
                                "callback_url": "http://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud/rendez-vous/passeports?date=2022-12-19T11:00Z",
                            },
                        ],
                    }
                }
            },
        },
        "401": {
            "description": "User not authorized",
            "content": {
                "application/json": {"example": "X-HUB-RDV-AUTH-TOKEN header invalid"}
            },
        },
    },
    dependencies=[Depends(verify_auth_token)],
)
@limiter.limit("30/minute")
async def get_available_time_slots(
    request: Request,
    meeting_point_ids: list[str] = Query(default=Required, example=["201", "203"]),
    start_date: date = Query(default=Required, example="2022-11-01"),
    end_date: date = Query(default=Required, example="2022-11-30"),
    reason: str = Query(
        default="CNI", enum=["CNI", "PASSPORT", "CNI-PASSPORT", "RETRIEVAL"]
    ),
    documents_number: int = Query(default=1),
):
    """
    Search available time slots.
    """

    all_points = get_all_meeting_points()

    result = {}

    meeting_points = []
    for meeting_point_id in meeting_point_ids:
        meeting_point = None
        index = 0
        while index < len(all_points):
            if meeting_point_id == all_points[index]["id"]:
                meeting_point = all_points[index]
                break
            index += 1

        if not meeting_point:
            raise HTTPException(
                status_code=404, detail=f"Unknown Meeting Point ID : {meeting_point_id}"
            )
        meeting_points.append(meeting_point)

    if os.environ.get("MOCK_EDITORS") in ["True", True]:
        for meeting_point in meeting_points:
            result[meeting_point["id"]] = get_mock_slots(
                meeting_point, start_date, end_date
            )
    else:
        for editor in get_all_editors():
            available_slots_obj = await editor.get_available_time_slots(
                meeting_points, start_date, end_date, reason, documents_number
            )
            for meeting_point in meeting_points:
                if (
                    meeting_point["_editor_name"] == editor.name
                    and meeting_point["_internal_id"] in available_slots_obj[0]
                ):
                    result[meeting_point["id"]] = available_slots_obj[0][
                        meeting_point["_internal_id"]
                    ]

    return result


@router.get(
    "/searchApplicationIds",
    responses={
        200: {
            "description": "Application IDs searched successfully!",
            "content": {
                "application/json": {
                    "example": {
                        "6123155111": [
                            {
                                "meeting_point": "Mairie ANNEXE LILLE-SECLIN",
                                "datetime": "2022-12-19T10:00Z",
                                "management_url": "http://www.ville-seclin.fr/rendez-vous/predemande?num=6123155111",
                                "cancel_url": "http://www.ville-seclin.fr/rendez-vous/annulation?num=6123155111",
                            }
                        ]
                    }
                }
            },
        },
        "401": {
            "description": "User not authorized",
            "content": {
                "application/json": {"example": "X-HUB-RDV-AUTH-TOKEN header invalid"}
            },
        },
        "422": {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/HTTPValidationError"}
                }
            },
        },
    },
    dependencies=[Depends(verify_auth_token)],
)
@limiter.limit("50/minute")
async def search_application_ids(
    request: Request,
    application_ids: List[
        constr(regex=r"^([a-zA-Z0-9]{10}[,;:\-/.\s])*[a-zA-Z0-9]{10}$")
    ] = Query(
        default=Required,
        example=["6123155111", "6123155222"],
        pattern=r"^([a-zA-Z0-9]{10}[,;:\-/.\s])*[a-zA-Z0-9]{10}$",
    ),
) -> Any:
    """
    Get the list of meetings by application_id.
    """

    meetings = []

    editor_futures = []
    for editor in get_all_editors():
        editor_futures.append(
            asyncio.ensure_future(editor.search_meetings(application_ids))
        )
    meetings = await asyncio.gather(*editor_futures)

    result = {}
    for editor_meetings in meetings:
        for key in editor_meetings:
            if editor_meetings[key]:
                if key not in result:
                    result[key] = []
                result[key] += editor_meetings[key]

    return result
