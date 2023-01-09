import os
from typing import Any, List

from fastapi import APIRouter, Query, Request, Response
from markdown import markdown
from pydantic import Required
from slowapi import Limiter
from slowapi.util import get_remote_address

from ...db.utils import get_all_editors, get_all_meeting_points
from ...models.announcement import Announcement
from ...models.editor_model import Editor
from ...models.municipality import MuncipalityWithDistance, Municipality
from ...services.search_meeting_points import search_close_meeting_points

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/MeetingPointsFromPosition",
    response_model=List[MuncipalityWithDistance],
    responses={
        200: {
            "description": "Meeting Points successfully found",
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
                            "distance_km": 1.56,
                        }
                    ]
                }
            },
        }
    },
)
@limiter.limit("30/minute")
def meeting_points_from_position(
    request: Request,
    longitude: float = Query(default=Required, example=2.352222),
    latitude: float = Query(default=Required, example=48.856613),
    radius_km: int = Query(default=20, enum=[20, 40, 60]),
) -> List[MuncipalityWithDistance]:
    """
    Search Meeting Point from position.
    """
    all_points: List[Municipality] = get_all_meeting_points()
    meeting_points: List[MuncipalityWithDistance] = search_close_meeting_points(
        all_points, latitude, longitude, radius_km
    )
    return meeting_points


@router.get(
    "/Announcement",
    response_model=Announcement,
    responses={
        200: {
            "description": "System global announcement",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "title": "Alerte de sécurité",
                            "description": "Attention, le site rencontre des attaques recurrentes en ce moment.",
                            "alert_level": "error",
                        }
                    ]
                }
            },
        }
    },
)
@limiter.limit("30/minute")
def global_announcement(request: Request) -> Any:
    """
    Return global announcement object.
    """
    if (
        ("ANNOUNCEMENT_TITLE" in os.environ)
        and ("ANNOUNCEMENT_DESCRIPTION" in os.environ)
        and ("ANNOUNCEMENT_ALERT_LEVEL" in os.environ)
    ):
        return {
            "title": os.environ.get("ANNOUNCEMENT_TITLE"),
            "description": markdown(os.environ.get("ANNOUNCEMENT_DESCRIPTION")),
            "alert_level": os.environ.get("ANNOUNCEMENT_ALERT_LEVEL"),
        }
    return Response(status_code=200)


@router.get(
    "/searchCity",
    response_model=Municipality,
    responses={
        200: {
            "description": "City successfully found",
            "content": {
                "application/json": {
                    "example": {
                        "id": "201",
                        "name": "Annexe mairie des Favignolles à Romorantin",
                        "longitude": 1.751597,
                        "latitude": 47.349797,
                        "public_entry_address": "1 rue François RABELAIS",
                        "zip_code": "41200",
                        "city_name": "Romorantin-Lanthenay",
                        "decoded_city_name": "romorantin-lanthenay",
                        "website": "https://rendezvousonline.fr/alias/romorantin-lanthenay-41200-2",
                        "city_logo": "https://pro.rendezvousonline.fr/upload/account/image/logo/2G8VjHfrJWB93mYFhPiYO5F4bPRJdaJz.jpg",
                    }
                }
            },
        }
    },
)
@limiter.limit("30/minute")
def search_city(
    request: Request,
    name: str = Query(default=Required, example="romorantin-lanthenay"),
) -> Municipality:
    """
    Search City by Name.
    """
    all_points: List[Municipality] = get_all_meeting_points()
    city = None
    for point in all_points:
        if point["decoded_city_name"] == name:
            city = point
            break
    return city


@router.get(
    "/status",
    responses={
        200: {
            "description": "Editor information",
            "content": {
                "application/json": {
                    "example": {
                        "editors": [
                            {
                                "slug": "troov",
                                "name": "Troov",
                                "api_url": "https://qa-api.troov.com/api",
                                "status": True,
                            }
                        ]
                    }
                }
            },
        }
    },
)
@limiter.limit("30/minute")
def get_editors(request: Request) -> List[Editor]:
    """
    Get editor detail.
    """
    return {"editors": get_all_editors()}
