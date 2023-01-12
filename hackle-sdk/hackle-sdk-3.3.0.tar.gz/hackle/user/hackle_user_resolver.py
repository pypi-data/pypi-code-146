from hackle import logger as _logging
from hackle.commons import utils
from hackle.commons import validator
from hackle.model import User, HackleUser
from hackle.user.identifier_type import IdentifierType
from hackle.user.identifiers_builder import IdentifiersBuilder
from hackle.user.internal_hackle_user import InternalHackleUser


class HackleUserResolver(object):

    def __init__(self, logger=None):
        self.logger = _logging.adapt_logger(logger or _logging.NoOpLogger())

    def resolve_or_none(self, user):

        if user is None:
            return None

        if isinstance(user, User):
            hackle_user = HackleUser.of(user)
        elif isinstance(user, HackleUser):
            hackle_user = user
        else:
            return None

        if hackle_user.properties is None:
            user_properties = {}
        else:
            user_properties = hackle_user.properties

        if not validator.is_valid_properties(user_properties):
            self.logger.warning(
                'User properties is not valid. User properties must be not dic types and items types must be string_types, number, bool.'
                ': {}'.format(user_properties))
            user_properties = utils.filter_properties(user_properties)

        identifiers_builder = IdentifiersBuilder(self.logger)
        identifiers_builder.add_identifiers(hackle_user.identifiers)

        if hackle_user.id is not None:
            identifiers_builder.add(IdentifierType.ID, hackle_user.id)

        if hackle_user.user_id is not None:
            identifiers_builder.add(IdentifierType.USER, hackle_user.user_id)

        if hackle_user.device_id is not None:
            identifiers_builder.add(IdentifierType.DEVICE, hackle_user.device_id)

        identifiers = identifiers_builder.build()

        if len(identifiers) == 0:
            return None

        return InternalHackleUser(identifiers, user_properties)
