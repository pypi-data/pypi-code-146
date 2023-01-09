import typing as t

from sarus_data_spec.manager.ops.asyncio.base import BaseScalarOp


class RandomSeed(BaseScalarOp):
    async def value(self) -> t.Any:
        assert self.scalar.is_random_seed()
        return self.scalar.protobuf().spec.random_seed.value
