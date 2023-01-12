from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AttachmentOutput:
    fileId: int
    fileName: str
    contentType: str
    entityId: int
    entityType: str
    modelFramework: str | None = None
