from search_lyrics.main import search_lyrics
from search_lyrics.entrypoint import entrypoint as search_lyrics_entrypoint
from search_lyrics.__version__ import __version__

version = __version__

__all__ = ["search_lyrics", "search_lyrics_entrypoint", "__version__"]
