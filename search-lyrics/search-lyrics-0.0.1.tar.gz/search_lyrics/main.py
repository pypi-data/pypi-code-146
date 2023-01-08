from os import getenv
from typing import List, Optional
import unicodedata

from genius import Genius
from genius.classes.song import Song

from search_lyrics.exceptions import NoAccessTokenProvided, ArtistNotFound


def normalize_str(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("utf8")


def search_lyrics(
    artist: str, text: str, genius_access_token: Optional[str] = None, verbose=False
) -> List[Song]:
    """
    Search song title by lyrics

    Parameters
    ----------
    artist: str
        artist in which searh for
    text: str
        text to search for
    genius_access_token: typing.Optional[str]
        access token to use for genius api (if not provided, use ENV variable GENIUS_ACCESS_TOKEN)
    verbose: bool
        show what it is doing

    Returns
    -------
    typing.List[genius.classes.song.Song]
    """
    if genius_access_token is None:
        if verbose:
            print("Searching GENIUS_ACCESS_TOKEN in ENV variable")
        genius_access_token = getenv("GENIUS_ACCESS_TOKEN")
        if genius_access_token is None:
            raise NoAccessTokenProvided()
    g = Genius(genius_access_token)
    artistt = g.search_artist(artist)
    if artistt is None:
        raise ArtistNotFound(artist)
    to_search = normalize_str(text).lower()

    occurences: List[Song] = []

    for songg in artistt.songs_by_popularity:
        song: Song = songg
        if verbose:
            print(f"searching in {song.title}..")
        for line in song.lyrics:
            line_normalized = normalize_str(line).lower()
            if to_search in line_normalized:
                if verbose:
                    print(f"Found in {song.title}\nlyrics line: {line}")
                occurences.append(song)
                break
    return occurences
