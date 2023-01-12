"""A system for making more dynamic and complex checks on discord.py commands.

:copyright: (c) 2022 Tanner B. Corcoran
:license: MIT, see LICENSE for more details.
"""

__title__ = "league-registrar"
__author__ = "Tanner B. Corcoran"
__email__ = "tannerbcorcoran@gmail.com"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2022 Tanner B. Corcoran"
__version__ = "0.0.2"
__description__ = "A system for making more dynamic and complex checks on discord.py commands"
__url__ = "https://github.com/tanrbobanr/dpy-check"
__download_url__ = "https://pypi.org/project/dpy-check/"

__all__ = (
    "ctx",
    "itx",
    "types",
    "exceptions",
    "constants",
    "utils",
    "user_has_channel_perms",
    "bot_has_channel_perms",
    "ErrorHandler",
    "Formatter",
    "user_has_guild_perms",
    "bot_has_guild_perms",
    "in_dm",
    "is_user",
    "in_channel",
    "in_guild",
    "in_category",
    "is_bot_owner",
    "channel_is_nsfw",
    "is_guild_owner",
    "username_contains",
    "membership",
    "custom",
    "Not",
    "Any",
    "Or",
    "All",
    "And",
    "user_has_role",
    "bot_has_role"
)

from . import ctx
from . import itx
from . import types
from . import exceptions
from . import constants
from . import utils
from ._channel_perms import (
    user_has_channel_perms,
    bot_has_channel_perms
)
from ._error_handler import (
    ErrorHandler,
    Formatter
)
from ._guild_perms import (
    user_has_guild_perms,
    bot_has_guild_perms
)
from ._misc import (
    in_dm,
    is_user,
    in_channel,
    in_guild,
    in_category,
    is_bot_owner,
    channel_is_nsfw,
    is_guild_owner,
    username_contains,
    membership,
    custom
)
from ._modifiers import (
    Not,
    Any,
    Or,
    All,
    And
)
from ._role import (
    user_has_role,
    bot_has_role
)
