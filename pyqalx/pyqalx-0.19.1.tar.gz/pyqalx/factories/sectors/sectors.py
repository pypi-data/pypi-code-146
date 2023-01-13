from collections import defaultdict

from pyqalx.core.errors import QalxFactoryBuildError
from pyqalx.factories.sectors.providers import _providers, LocalProvider


class Sectors(dict):
    """
    A dict subclass that groups the remote sectors into a dictionary
    of <provider_type>:<profile_name>:<region_name><sector_name>:<sector>
    This deep nesting will enable us to create a single stack for
    each provider:profile:region intersection

    Class attributes
        RESERVED_KEYS:  Specific keys at the top level of a stage that cannot
                        be used as the name of a sector.

    Instance attributes
        plan:           The factory plan as JSON
        stage:          The stage that the sectors are for
        factory:        The factory instance the sectors are built for
        validate_default_region:    Boolean of whether the default region
        should be validated
    """

    USER_PROFILE_KEY = "user_profile"
    BOT_PROFILE_KEY = "bot_profile"
    RESERVED_KEYS = {"workflow", USER_PROFILE_KEY, BOT_PROFILE_KEY}

    def __init__(
        self, factory, validate_default_region=True, validate_permissions=True
    ):
        """
        :param factory: The factory instance
        :param validate_default_region: Whether the default region should be
        validated.  The only time we don't want to ensure that there is a valid
        default region is when running the bootstrap script on remote bots as
        this uses the internal server to figure out the region
        :param validate_permissions: Whether the permissions of the calling
        user should be validated for remote sectors.  This won't need to happen
        when running the bootstrap script on remote bots as this uses the internal
        server to figure out the region
        """
        _sectors = {}
        for key in _providers.keys():
            _sectors[key] = defaultdict(lambda: defaultdict(dict))
        super(Sectors, self).__init__(_sectors)
        self.validate_default_region = validate_default_region
        self.validate_permissions = validate_permissions
        self.factory = factory
        self._group_sectors()

    @staticmethod
    def _get_provider(sector):
        sector_type = sector["type"]
        try:
            return _providers[sector_type]
        except KeyError:  # pragma: no cover
            # Should be handled by validation - this is here to
            # as a safety net.
            raise QalxFactoryBuildError(
                f"`{sector_type}` is not a valid "
                f"sector type.  Valid sector type"
                f' are `{", ".join(_providers.keys())}`'
            )

    def _group_sectors(self):
        """
        Groups the sectors on the plan by profile_name and then region_name.
        If no profile/region name supplied for a sector then use the default
        for the sectors provider.  Will ultimately lead to a group
        of sectors for each provider:profile_name:region_name intersection
        :return: A dict of sectors parameters grouped
         by profile_name:region_name
        """
        sectors = self._sectors()
        for sector_name, sector in sectors.items():
            provider = self._get_provider(sector)
            profile_name = sector[provider.PROFILE_NAME_KEY]
            region_name = sector[provider.REGION_NAME_KEY]

            self[provider._type][profile_name][region_name][
                sector_name
            ] = sector
        return self

    def _sectors(self):
        """
        Iterates over all the sectors on the stage and returns them grouped
        by profile_name/region_name.  All local sectors will be combined into
        a single sector.
        :return:The provider sectors as a dict of sector_name:sector_data
        """
        sectors = {}
        stage = self.factory._plan_stages[self.factory.stage]
        for sector_name, sector in stage.items():
            if sector_name not in self.RESERVED_KEYS:
                provider = self._get_provider(sector)
                if sector.get(provider.REGION_NAME_KEY) is None:
                    sector[
                        provider.REGION_NAME_KEY
                    ] = provider.default_region_name(
                        validate=self.validate_default_region,
                        log=self.factory.session.log,
                    )
                if provider._type == LocalProvider._type:
                    profile_name = provider.default_profile_name()
                else:
                    profile_name = self.factory.aws_profile
                sector[provider.PROFILE_NAME_KEY] = profile_name
                sector[self.USER_PROFILE_KEY] = self.factory.user_profile
                sector[self.BOT_PROFILE_KEY] = self.factory.bot_profile
                if self.validate_permissions:
                    profile_name = sector[provider.PROFILE_NAME_KEY]
                    region_name = sector[provider.REGION_NAME_KEY]
                    provider.validate_permissions(
                        profile_name=profile_name,
                        region_name=region_name,
                        log=self.factory.session.log,
                    )
                sectors[sector_name] = sector
        return sectors
