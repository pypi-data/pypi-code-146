from typing import ClassVar

from .models import Status, StatusDto, UpdateDto, ContentDto
from ..core import BaseLoLEndpoint
from ..enums import Region, Locale


class StatusEndpoint(BaseLoLEndpoint):
    BASE: ClassVar[str] = '/lol/status/v4/platform-data'

    async def get(self, region: Region):
        data = await self.fetch(region, self.BASE)
        return Status(
            id = data['id'],
            name = data['name'],
            locales = [Locale(locale) for locale in data['locales']],
            maintenances = [
                StatusDto(
                    id = item['id'],
                    status = item['maintenance_status'],
                    severity = item['incident_severity'],
                    created_at = item['created_at'],
                    archive_at = item['archive_at'],
                    updated_at = item['updated_at'],
                    titles = [
                        ContentDto(
                            content = title['content'],
                            locale = Locale(title['locale'])
                        ) for title in item['titles']
                    ],
                    updates = [
                        UpdateDto(
                            id = update['id'],
                            created_at = update['created_at'],
                            updated_at = update['updated_at'],
                            translations = [
                                ContentDto(
                                    content = content['content'],
                                    locale = Locale(content['locale'])
                                ) for content in update['translations']
                            ]
                        ) for update in item['updates']
                    ],
                    platforms = item['platforms']
                ) for item in data['maintenances']
            ],
            incidents = [
                StatusDto(
                    id = item['id'],
                    status = item['maintenance_status'],
                    severity = item['incident_severity'],
                    created_at = item['created_at'],
                    archive_at = item['archive_at'],
                    updated_at = item['updated_at'],
                    titles = [
                        ContentDto(
                            content = title['content'],
                            locale = Locale(title['locale'])
                        ) for title in item['titles']
                    ],
                    updates = [
                        UpdateDto(
                            id = update['id'],
                            created_at = update['created_at'],
                            updated_at = update['updated_at'],
                            translations = [
                                ContentDto(
                                    content = content['content'],
                                    locale = Locale(content['locale'])
                                ) for content in update['translations']
                            ]
                        ) for update in item['updates']
                    ],
                    platforms = item['platforms']
                ) for item in data['incidents']
            ]
        )