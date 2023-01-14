from pydantic import BaseModel, Field


class SiteConfig(BaseModel):
    site_id: int = Field(..., alias='siteId')
