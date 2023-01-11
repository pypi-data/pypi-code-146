# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

__version__ = '0.8.0'

from tgclients.aggregator import (
    Aggregator,
)
from tgclients.auth import (
    TextgridAuth,
    TextgridAuthException,
)
from tgclients.config import (
    TextgridConfig,
)
from tgclients.crud import (
    TextgridCrud,
    TextgridCrudRequest,
    TextgridCrudException,
)
from tgclients.metadata import (
    TextgridMetadata,
)
from tgclients.search import (
    TextgridSearch,
    TextgridSearchRequest,
    TextgridSearchException,
)
from tgclients.utils import (
    Utils,
)
__all__ = [
    'Aggregator',
    'TextgridAuth',
    'TextGridAuthException',
    'TextgridConfig',
    'TextgridCrud',
    'TextgridCrudRequest',
    'TextgridCrudException',
    'TextgridSearch',
    'TextgridSearchRequest',
    'TextgridSearchException',
    'Utils',
]
