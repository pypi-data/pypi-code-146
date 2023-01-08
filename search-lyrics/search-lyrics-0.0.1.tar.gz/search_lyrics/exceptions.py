class NoAccessTokenProvided(Exception):
    def __init__(self) -> None:
        super().__init__("Genius Access Token is not Provided")


class ArtistNotFound(Exception):
    def __init__(self, artist: str) -> None:
        super().__init__(f"Artist {artist} not found")
