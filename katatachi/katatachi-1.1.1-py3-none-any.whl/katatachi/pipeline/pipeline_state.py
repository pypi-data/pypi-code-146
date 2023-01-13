import dataclasses

from katatachi.content import ContentStore

from .state_key import StateKey


@dataclasses.dataclass
class PipelineState:
    name: str

    def to_dict(self, content_store: ContentStore):
        return {
            "name": self.name,
            "count": content_store.collection.count_documents({StateKey: self.name}),
        }
