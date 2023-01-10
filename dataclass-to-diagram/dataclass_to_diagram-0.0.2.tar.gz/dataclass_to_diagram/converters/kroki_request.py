import logging
from typing import Literal, TypeAlias

import httpx

from dataclass_to_diagram.exceptions import ConverterError

log = logging.getLogger(__name__)

DiagramType: TypeAlias = Literal["c4plantuml"]
OutputFormat: TypeAlias = Literal["png", "svg"]


async def kroki_request(
    diagram_source: str,
    diagram_type: DiagramType,
    output_format: OutputFormat,
    kroki_url: str = "https://kroki.io",
) -> bytes:
    """Запрос на конвертирование к сервису kroki.io."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=kroki_url,
                json={
                    "diagram_source": diagram_source,
                    "diagram_type": diagram_type,
                    "output_format": output_format,
                },
            )
        except httpx.HTTPError as exc:
            log.error(exc)
            raise ConverterError from exc
    return response.content
