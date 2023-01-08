from typing import List
from pydantic import BaseModel, Field


class Date(BaseModel):
    day: int | None = None
    month: int | None = None
    year: int | None = None


class JPG(BaseModel):
    image_url: str | None = None
    small_image_url: str | None = None
    large_image_url: str | None = None


class Webp(BaseModel):
    image_url: str | None = None
    small_image_url: str | None = None
    large_image_url: str | None = None


class Image(BaseModel):
    jpg: JPG = JPG()
    webp: Webp = Webp()


class Trailer(BaseModel):
    youtube_id: str | None = None
    url: str | None = None
    embed_url: str | None = None


class Title(BaseModel):
    type: str | None = None
    title: str | None = None


class Prop(BaseModel):
    from_: Date = Field(default_factory=Date, alias="from")
    to: Date = Date()
    string: str | None = None


class AirDate(BaseModel):
    from_: str | None = Field(None, alias="from")
    to: str | None = None
    prop: Prop = Prop()


class Broadcast(BaseModel):
    day: str | None = None
    time: str | None = None
    timezone: str | None = None
    string: str | None = None


class Producer(BaseModel):
    mal_id: int | None = None
    type: str | None = None
    name: str | None = None
    url: str | None = None


class Licenser(BaseModel):
    mal_id: int | None = None
    type: str | None = None
    name: str | None = None
    url: str | None = None


class Studio(BaseModel):
    mal_id: int | None = None
    type: str | None = None
    name: str | None = None
    url: str | None = None


class Streaming(BaseModel):
    name: str | None = None
    url: str | None = None


class Genre(BaseModel):
    mal_id: int | None = None
    type: str | None = None
    name: str | None = None
    url: str | None = None


class ExplicitGenre(BaseModel):
    mal_id: int | None = None
    type: str | None = None
    name: str | None = None
    url: str | None = None


class ThemeGenre(BaseModel):
    mal_id: int | None = None
    type: str | None = None
    name: str | None = None
    url: str | None = None


class Demographic(BaseModel):
    mal_id: int | None = None
    type: str | None = None
    name: str | None = None
    url: str | None = None


class Entry(BaseModel):
    mal_id: int | None = None
    type: str | None = None
    name: str | None = None
    url: str | None = None


class Related(BaseModel):
    relation: str | None = None
    entry: List[Entry] = []


class Theme(BaseModel):
    openings: List[str] = []
    endings: List[str] = []


class External(BaseModel):
    name: str | None = None
    url: str | None = None


class Items(BaseModel):
    count: int = 0
    total: int = 0
    per_page: int = 0


class Pagination(BaseModel):
    last_visible_page: int = 1
    has_next_page: bool = False
    current_page: int = 1
    items: Items = Items()


class Character(BaseModel):
    mal_id: int | None = None
    url: str | None = None
    images: Image = Image()
    name: str | None = None


class Person(BaseModel):
    mal_id: int | None = None
    url: str | None = None
    images: Image = Image()
    name: str | None = None


class VoiceActor(BaseModel):
    person: Person = Person()
    language: str | None = None


class Staff(BaseModel):
    person: Person = Person()
    positions: List[str] = []


class News(BaseModel):
    mal_id: int | None = None
    url: str | None = None
    title: str | None = None
    date: str | None = None
    author_username: str | None = None
    author_url: str | None = None
    forum_url: str | None = None
    images: Image = Image()
    comments: int = 0
    excerpt: str | None = None


class Episode(BaseModel):
    mal_id: int | None = None
    url: str | None = None
    title: str | None = None
    title_japanese: str | None = None
    title_romanji: str | None = None
    duration: float | None = None
    aired: str | None = None
    filler: bool = False
    recap: bool = False
    synopsis: str | None = None
    forum_url: str | None = None


class Anime(BaseModel):
    mal_id: int
    url: str
    images: Image = Image()
    trailer: Trailer = Trailer()
    approved: bool | None = None
    titles: List[Title] = []
    title: str | None = None
    title_english: str | None = None
    title_japanese: str | None = None
    title_synonyms: List[str] = []
    type: str | None = None
    source: str | None = None
    episodes: int | None = None
    status: str | None = None
    airing: bool | None = None
    aired: AirDate = AirDate()
    duration: str | None = None
    rating: str | None = None
    score: float | None = None
    scored_by: int | None = None
    rank: int | None = None
    popularity: int | None = None
    members: int | None = None
    favorites: int | None = None
    synopsis: str | None = None
    background: str | None = None
    season: str | None = None
    year: int | None = None
    broadcast: Broadcast = Broadcast()
    producers: List[Producer] = []
    licensors: List[Licenser] = []
    studios: List[Studio] = []
    genres: List[Genre] = []
    explicit_genres: List[ExplicitGenre] = []
    ThemeGenres: List[ThemeGenre] = []
    demographics: List[Demographic] = []
    relations: List[Related] = []
    theme: Theme = Theme()
    external: list[External] = []
    streaming: List[Streaming] = []


class AnimeSearch(BaseModel):
    data: List[Anime] = []
    pagination: Pagination = Pagination()


class AnimeCharacter(BaseModel):
    character: Character = Character()
    role: str | None = None
    voice_actors: List[VoiceActor] = []


class AnimeCharacters(BaseModel):
    data: List[AnimeCharacter] = []
    pagination: Pagination = Pagination()


class AnimeStaff(BaseModel):
    data: List[Staff] = []
    pagination: Pagination = Pagination()


class AnimeEpisodes(BaseModel):
    data: List[Episode] = []
    pagination: Pagination = Pagination()


class AnimeNews(BaseModel):
    data: List[News] = []
    pagination: Pagination = Pagination()
