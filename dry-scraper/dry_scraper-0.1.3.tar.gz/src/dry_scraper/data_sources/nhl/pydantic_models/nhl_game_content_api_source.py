from datetime import datetime
from typing import List, Dict, Optional, Annotated, Literal
from uuid import UUID
from pydantic import BaseModel, constr, Field, HttpUrl

GameContentLink = constr(regex=r"^/api/v1/game/\d{10}/content$")
ResolutionString = constr(regex=r"^\d{2,4}x\d{2,4}$")


class Empty(BaseModel):
    ...

    class Config:
        extra = "forbid"


class ContributorEntry(BaseModel):
    name: str
    twitter: str


class Contributor(BaseModel):
    contributors: List[ContributorEntry]
    source: str


class ImageCut(BaseModel):
    aspect_ratio: str = Field(alias="aspectRatio")
    width: int
    height: int
    src: HttpUrl
    at2x: HttpUrl
    at3x: HttpUrl


class Image(BaseModel):
    title: str
    alt_text: str = Field(alias="altText")
    cuts: Dict[ResolutionString, ImageCut]


class Playback(BaseModel):
    name: str
    width: Optional[int | str]
    height: Optional[int | str]
    url: HttpUrl | str


class Keyword(BaseModel):
    type: str
    value: str
    display_name: str = Field(alias="displayName")


class PhotoMediaItem(BaseModel):
    type: str
    image: Image


class MediaItem(BaseModel):
    type: str
    id: int
    date: datetime
    title: str
    blurb: str
    description: str
    duration: str
    auth_flow: bool = Field(alias="authFlow")
    media_playback_id: int = Field(alias="mediaPlaybackId")
    media_state: str = Field(alias="mediaState")
    keywords: List[Keyword]
    image: Image
    playbacks: List[Playback]


class EditorialItem(BaseModel):
    type: str
    state: str
    date: datetime
    id: str
    headline: str
    subhead: str
    seo_title: str = Field(alias="seoTitle")
    seo_description: str = Field(alias="seoDescription")
    seo_keywords: str = Field(alias="seoKeywords")
    slug: str
    commenting: bool
    tagline: str
    contributor: Contributor
    keywords_display: List[Keyword] = Field(alias="keywordsDisplay")
    keywords_all: List[Keyword] = Field(alias="keywordsAll")
    approval: str
    url: str
    data_URI: str = Field(alias="dataURI")
    media: MediaItem | PhotoMediaItem | Empty
    preview: str


class NhlTvItem(BaseModel):
    guid: UUID
    media_state: str = Field(alias="mediaState")
    media_playback_id: int = Field(alias="mediaPlaybackId")
    media_feed_type: str = Field(alias="mediaFeedType")
    call_letters: str = Field(alias="callLetters")
    event_id: str = Field(alias="eventId")
    language: str
    free_game: bool = Field(alias="freeGame")
    feed_name: str = Field(alias="feedName")
    game_plus: bool = Field(alias="gamePlus")


class AudioItem(BaseModel):
    media_state: str = Field(alias="mediaState")
    media_playback_id: int = Field(alias="mediaPlaybackId")
    media_feed_type: str = Field(alias="mediaFeedType")
    call_letters: str = Field(alias="callLetters")
    event_id: str = Field(alias="eventId")
    language: str
    free_game: bool = Field(alias="freeGame")
    feed_name: str = Field(alias="feedName")
    game_plus: bool = Field(alias="gamePlus")


class EditorialCategory(BaseModel):
    title: str
    topic_list: str = Field(alias="topicList")
    items: List[EditorialItem]


class NhlTvEntry(BaseModel):
    title: Literal["NHLTV"]
    platform: str
    items: List[NhlTvItem]


class AudioEpgEntry(BaseModel):
    title: Literal["Audio"]
    topic_list: Optional[int | str] = Field(alias="topicList")
    items: List[AudioItem]


class ExtendedHighlightsEpgEntry(BaseModel):
    title: Literal["Extended Highlights"]
    topic_list: Optional[int | str] = Field(alias="topicList")
    items: List[MediaItem]


class RecapEpgEntry(BaseModel):
    title: Literal["Recap"]
    topic_list: Optional[int | str] = Field(alias="topicList")
    items: List[MediaItem]


class PowerPlayEpgEntry(BaseModel):
    title: Literal["Power Play"]
    topic_list: Optional[int | str] = Field(alias="topicList")
    items: List[MediaItem]


EpgEntry = Annotated[
    NhlTvEntry
    | AudioEpgEntry
    | ExtendedHighlightsEpgEntry
    | RecapEpgEntry
    | PowerPlayEpgEntry,
    Field(discriminator="title"),
]


class Editorial(BaseModel):
    preview: EditorialCategory
    articles: EditorialCategory
    recap: EditorialCategory


class Milestone(BaseModel):
    title: str
    description: str
    type: str
    type: str
    time_absolute: datetime = Field(alias="timeAbsolute")
    time_offset: datetime = Field(alias="timeOffset")
    period: int | str
    stats_event_id: int | str = Field(alias="statsEventId")
    team_id: int | str = Field(alias="teamId")
    player_id: int | str = Field(alias="playerId")
    period_time: str = Field(alias="periodTime")
    ordinal_num: str = Field(alias="ordinalNum")
    highlight: MediaItem | Empty


class Milestones(BaseModel):
    title: Literal["Milestones"]
    steam_start: datetime = Field(alias="streamStart")
    items: List[Milestone]


class Media(BaseModel):
    epg: List[EpgEntry]
    milestones: Milestones | Empty


class HighlightEntries(BaseModel):
    title: str
    topic_list: str = Field(alias="topicList")
    items: List[MediaItem]


class Highlights(BaseModel):
    scoreboard: HighlightEntries
    gamecenter: HighlightEntries = Field(alias="gameCenter")


class GameContent(BaseModel):
    link: GameContentLink
    editorial: Editorial
    media: Media
    highlights: Highlights
