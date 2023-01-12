from dataclasses import asdict, dataclass, field
from typing import List


@dataclass(order=True)
class Company:
    key: str = field(init=False)  # primary key
    name: str
    domain: str  # unique
    description: str  # unique
    # revenue: int  # in millions
    # tags: List[str]  # idea affiliated-search_keys as tag
    _match_tokens: List[str]

    sort_index: float = field(init=False, repr=False)

    def __post_init__(self):
        # assert(self.revenue < (10**4))
        self.key = self.domain
        self.sort_index = self.revenue


from gandai.datastore import Cloudstore

ds = Cloudstore()


# def load_all_orgs() -> List[Organization]:
#     keys = ds.keys("organizations/")
#     data = await asyncio.gather(*[get(k) for k in keys])
#     orgs = list(futures)
#     orgs = [from_dict(Organization, org) for org in orgs]
#     return orgs
