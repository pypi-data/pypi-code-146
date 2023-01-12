from dataclasses import asdict, dataclass, field
from time import time

from gandai.datastore import Cloudstore

ds = Cloudstore()


@dataclass
class Comment:
    key: str = field(init=False)
    search_key: str
    actor_key: str  #
    domain: str  # domain
    body: str
    created: int = field(init=False)

    def __post_init__(self):
        self.created = int(time())
        self.key = f"searches/{self.search_key}/comments/{self.created}"


def post_comment(actor_key: str, search_key: str, domain: str, body: str) -> dict:
    comment = Comment(
        actor_key=actor_key, search_key=search_key, domain=domain, body=body
    )
    ds[comment.key] = asdict(comment)
    return asdict(comment)
