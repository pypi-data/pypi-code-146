import json
import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from ...controllers.routes.time_slots import search_slots
from ...db.utils import add_ws_use_rates, get_all_editors, get_ws_use_rates
from ...services.data_validator import is_valid_search_criteria

logging.getLogger("uvicorn.error").setLevel(logging.ERROR)

router = APIRouter()


@router.websocket("/SlotsFromPositionStreaming")
async def slots_from_position_streaming(websocket: WebSocket):
    _logger = logging.getLogger("root")
    try:
        await websocket.accept()
        while True:
            raw_data = await websocket.receive_text()
            # Check use rate per minute
            if get_ws_use_rates(websocket.client.host) > 30:
                await websocket.send_text("end_of_search")
                raise Exception("Websocket rate limit exceeded")
            else:
                add_ws_use_rates(websocket.client.host)
            start_time = datetime.now()
            data = json.loads(raw_data)
            if not is_valid_search_criteria(data):
                raise HTTPException(status_code=400, detail="Invalid search criteria")
            latitude = float(data["latitude"])
            longitude = float(data["longitude"])
            start_date = None
            try:
                if "start_date" in data:
                    start_date = datetime.strptime(
                        data["start_date"], "%Y-%m-%d"
                    ).date()
            except ValueError:
                pass
            end_date = None
            try:
                if "end_date" in data:
                    end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
            except ValueError:
                pass
            radius_km = int(data["radius_km"])
            reason = None
            if "reason" in data:
                reason = data["reason"]
            documents_number = None
            if "documents_number" in data:
                documents_number = int(data["documents_number"])

            result, errors = await search_slots(
                longitude,
                latitude,
                start_date,
                end_date,
                radius_km,
                reason,
                documents_number,
                websocket=websocket,
            )
            json_text = json.dumps(
                {
                    "step": "end_of_search",
                    "editors_number": len(get_all_editors()),
                    "editor_errors_number": len(errors),
                },
                default=str,
            )
            await websocket.send_text(json_text)
            _logger.info(
                "End of websocket search",
                extra={
                    "extra_info": {
                        "type": "access",
                        "searchCriteria": data,
                        "searchLocation": {"lat": latitude, "lon": longitude},
                        "response_time": (datetime.now() - start_time).microseconds
                        / 1000,
                        "protocol": "websocket",
                        "realip": websocket.client.host,
                    }
                },
            )
    except WebSocketDisconnect:
        _logger.debug("Client disconnected.")
    except HTTPException as websocket_e:
        _logger.error("Error during websocket connexion : %s", websocket_e.detail)
    except Exception as websocket_e:
        _logger.error("Error during websocket connexion : %s", websocket_e)
