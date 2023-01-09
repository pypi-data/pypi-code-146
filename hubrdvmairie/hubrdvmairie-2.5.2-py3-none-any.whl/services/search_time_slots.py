import asyncio
import os
import random
from datetime import date

from fastapi import WebSocket

from ..db.utils import get_all_editors, get_all_meeting_points
from ..services.search_meeting_points import search_close_meeting_points


async def search_slots(
    longitude: float,
    latitude: float,
    start_date: date,
    end_date: date,
    radius_km: int,
    reason: str = "CNI",
    documents_number: int = 1,
    websocket: WebSocket = None,
):
    all_points = get_all_meeting_points()
    meeting_points = search_close_meeting_points(
        all_points, latitude, longitude, radius_km
    )
    all_editors_meeting_points = []
    all_editors_errors = []

    no_response_score = random.randint(1, 3)
    if (
        os.environ.get("MOCK_EMPTY_RESPONSE") in ["True", True]
    ) and no_response_score < 2:
        await asyncio.sleep(3)
    else:
        editor_futures = []
        for editor in get_all_editors():
            editor_futures.append(
                asyncio.ensure_future(
                    editor.search_slots_in_editor(
                        meeting_points,
                        start_date,
                        end_date,
                        reason,
                        documents_number,
                        websocket,
                    )
                )
            )
        all_results = await asyncio.gather(*editor_futures)
        for result in all_results:
            all_editors_meeting_points += result[0]
            if result[1]:
                all_editors_errors.append(result[1])
    return all_editors_meeting_points, all_editors_errors
