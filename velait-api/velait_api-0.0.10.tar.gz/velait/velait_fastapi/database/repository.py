from assimilator.alchemy.database import AlchemyRepository as BaseAlchemyRepository
from velait.common.database.exceptions import AlreadyDeletedError


class VelaitRepository(BaseAlchemyRepository):
    def delete(self, obj):
        if obj.is_removed:
            raise AlreadyDeletedError(name="obj", description="Already deleted")

        obj.is_removed = True


__all__ = [
    'VelaitRepository',
]
