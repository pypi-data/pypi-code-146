from pyqalx.factories.sectors.providers.aws.provider import AWSProvider
from pyqalx.factories.sectors.providers.local.provider import LocalProvider

# A dict of valid external providers.
_providers = {
    AWSProvider._type: AWSProvider,
    LocalProvider._type: LocalProvider,
}
