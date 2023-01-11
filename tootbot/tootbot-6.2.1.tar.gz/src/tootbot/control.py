"""This module contains helper classes and methods to assist with determining
if a reddit post should be published on Mastodon."""
import configparser
import sys
from dataclasses import dataclass
from logging import DEBUG
from logging import Formatter
from logging import getLogger
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from typing import Any
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import aiosqlite
from typing_extensions import Final

from . import __display_name__
from . import POST_RECORDER_SQLITE_DB

PR = TypeVar("PR", bound="PostRecorder")
ConfigClass = TypeVar("ConfigClass", bound="Configuration")

logger = getLogger(__display_name__)


class PostRecorder:
    """Implements logging of reddit posts published to Mastodon and also
    checking against the log of published content to determine if a post would
    be a duplicate."""

    LAST_POST_TS: Final[str] = "last-post-timestamp"

    def __init__(self: PR, history_db_dir: str = ".") -> None:
        self.history_db_file = f"{history_db_dir.rstrip('/')}/{POST_RECORDER_SQLITE_DB}"
        self.history_db: Optional[aiosqlite.Connection] = None

    async def db_init(self: PR) -> None:
        """Initialises DB connection and tables if necessary."""
        self.history_db = await aiosqlite.connect(database=self.history_db_file)
        # Make sure DB tables exist
        await self.history_db.execute(
            "CREATE TABLE IF NOT EXISTS post (id TEXT PRIMARY KEY) WITHOUT ROWID"
        )
        await self.history_db.execute(
            "CREATE TABLE IF NOT EXISTS share "
            "(url TEXT PRIMARY KEY) "
            "WITHOUT ROWID"
        )
        await self.history_db.execute(
            "CREATE TABLE IF NOT EXISTS hash "
            "(checksum TEXT PRIMARY KEY) "
            "WITHOUT ROWID"
        )
        await self.history_db.execute(
            "CREATE TABLE IF NOT EXISTS settings "
            "(key TEXT PRIMARY KEY, value) "
            "WITHOUT ROWID"
        )
        await self.history_db.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (:key, :value)",
            {"key": PostRecorder.LAST_POST_TS, "value": 0},
        )
        await self.history_db.commit()

    async def duplicate_check(self: PR, identifier: str) -> bool:
        """Checks if identifier can be found in log file of content posted to
        Mastodon.

        Arguments:
            identifier (string):
                Any identifier we want to make sure has not already been posted.
                This can be id of reddit post, url of media attachment file to be
                posted, or checksum of media attachment file.

        Returns:
            boolean:
                False if "identifier" is not in log of content already posted to
                Mastodon
                True if "identifier" has been found in log of content.
        """
        logger.debug("PostRecorder.duplicate_check(identifier=%s)", identifier)

        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        # check for reddit_id
        cursor = await self.history_db.execute(
            "SELECT * FROM post where id=:id", {"id": identifier}
        )
        if await cursor.fetchone():
            logger.debug("PostRecorder.duplicate_check(...) -> True")
            return True

        # check for Shared URL
        cursor = await self.history_db.execute(
            "SELECT * FROM share where url=:url", {"url": identifier}
        )
        if await cursor.fetchone():
            logger.debug("PostRecorder.duplicate_check(...) -> True")
            return True

        # check for attachment hash
        cursor = await self.history_db.execute(
            "SELECT * FROM hash where checksum=:checksum", {"checksum": identifier}
        )
        if await cursor.fetchone():
            logger.debug("PostRecorder.duplicate_check(...) -> True")
            return True

        logger.debug("PostRecorder.duplicate_check(...) -> False")
        return False

    async def log_post(
        self: PR,
        reddit_id: Optional[str] = None,
        shared_url: Optional[str] = None,
        check_sum: Optional[str] = None,
    ) -> None:
        """Logs details about reddit posts that have been published.

        Arguments:
            reddit_id (string):
                Id of post on reddit that was published to Mastodon
            shared_url (string):
                URL of media attachment that was shared on Mastodon
            check_sum (string):
                Checksum of media attachment that was shared on Mastodon.
                This enables checking for duplicate media even if file has been renamed.
        """
        logger.debug(
            "PostRecorder.log_post(reddit_id=%s ,shared_url= %s, checksum= %s)",
            reddit_id,
            shared_url,
            check_sum,
        )

        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        if reddit_id:
            await self.history_db.execute("INSERT INTO post VALUES (?)", (reddit_id,))
        if shared_url:
            await self.history_db.execute("INSERT INTO share VALUES (?)", (shared_url,))
        if check_sum:
            await self.history_db.execute("INSERT INTO hash VALUES (?)", (check_sum,))
        await self.history_db.commit()

    async def get_setting(
        self: PR,
        key: str,
    ) -> Any:
        """Retrieves a setting from database.

        :param self: Post Recorded instance
        :param key: Key to setting stored in DB
        :type key: str

        :return: Value of setting. This could be an int, str, or float
        """
        logger.debug("PostRecorder.get_settings(key=%s)", key)
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        cursor = await self.history_db.execute(
            "SELECT value FROM settings WHERE key=:key", {"key": key}
        )
        row = await cursor.fetchone()
        if row is None:
            return None

        logger.debug("PostRecorder.get_settings(...) returns: %s", row[0])
        return row[0]

    async def save_setting(
        self: PR,
        key: str,
        value: Union[int, str, float],
    ) -> None:
        """Retrieves a setting from database.

        :param self: Post Recorded instance
        :param key: Key to setting stored in DB
        :type key: str
        :param value: Value to store as a setting
        :type key: Union[int, str, float]

        :return: None
        """
        logger.debug("PostRecorder.save_settings(key=%s, value=%s)", key, value)
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        await self.history_db.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (:key, :value)",
            {"key": key, "value": value},
        )

        await self.history_db.commit()

    async def close_db(self: PR) -> None:
        """Closes db connection."""
        if self.history_db:
            await self.history_db.close()


@dataclass
class Secret:
    """Dataclass for API login secrets."""

    client_id: Optional[str]
    client_secret: str


@dataclass
class BotConfig:
    """Dataclass holding configuration values for general behaviour of
    tootbot."""

    post_recorder: PostRecorder
    delay_between_posts: int
    run_once_only: bool
    hash_tags: List[str]
    log_level: str


@dataclass
class RedditReaderConfig:
    """Dataclass holding configuration values related to Reddit."""

    post_limit: int
    nsfw_allowed: bool
    nsfw_marked: bool
    spoilers: bool
    self_posts: bool
    stickied_allowed: bool


@dataclass
class PromoConfig:
    """Dataclass holding configuration values related to Promotional message
    settings."""

    every: int
    message: str


@dataclass
class HealthCheckConfig:
    """Dataclass holding configuration values around Healthchecks
    monitoring."""

    enabled: bool
    base_url: str
    uuid: str


@dataclass
class MediaConfig:
    """Dataclass holding configuration values around attached media."""

    folder: str
    media_only: bool


@dataclass
class MastodonConfig:
    """Dataclass holding configuration values for Mastodon settings.

    This also stores the number of times the mastodon API has returned
    an error to allow throttling of posting toots in a controlled manner
    """

    # pylint: disable=too-many-instance-attributes

    domain: str
    media_always_sensitive: bool
    post_visibility: str
    throttling_enabled: bool
    throttling_max_delay: int
    number_of_errors: int
    use_caption: bool
    use_tags: bool
    use_backlink: bool


@dataclass
class SubredditConfig:
    """Dataclass to hold configuration settings about the subreddits to be
    monitored."""

    name: str
    tags: str


@dataclass
class Configuration:
    """Dataclass to hold all settings for tootbot."""

    bot: BotConfig
    subreddits: List[SubredditConfig]
    promo: PromoConfig
    health: HealthCheckConfig
    media: MediaConfig
    mastodon_config: MastodonConfig
    reddit: RedditReaderConfig

    @classmethod
    async def load_config(
        cls: Type[ConfigClass],
        config_dir: str,
        debug_log: str,
    ) -> ConfigClass:
        """Loads aor queries config parameters from user, as necessary."""

        if debug_log:
            file_log_formatter = Formatter(
                "%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s",
                datefmt="%H:%M:%S",
            )
            file_handler = TimedRotatingFileHandler(
                filename=debug_log,
                backupCount=7,
                when="midnight",
            )
            file_handler.setFormatter(file_log_formatter)
            file_handler.setLevel(DEBUG)
            logger.addHandler(file_handler)

        # Make sure config file exists
        try:
            config = configparser.ConfigParser()
            config.read(f"{config_dir}/config.ini")
        except configparser.Error as config_error:
            print("[ERROR] Error while reading config file: %s", config_error)
            sys.exit(1)

        await cls._set_up_logging(config)
        bot = await Configuration._load_bot_settings(
            config=config,
            config_dir=config_dir,
        )
        reddit = RedditReaderConfig(
            post_limit=int(config["BotSettings"]["PostLimit"]),
            nsfw_allowed=str_to_bool(config["BotSettings"]["NSFWPostsAllowed"]),
            nsfw_marked=str_to_bool(config["BotSettings"]["NSFWPostsMarked"]),
            spoilers=str_to_bool(config["BotSettings"]["SpoilersAllowed"]),
            self_posts=str_to_bool(config["BotSettings"]["SelfPostsAllowed"]),
            stickied_allowed=str_to_bool(config["BotSettings"]["StickiedPostsAllowed"]),
        )
        promo = PromoConfig(
            every=int(config["PromoSettings"]["PromoEvery"]),
            message=config["PromoSettings"]["PromoMessage"],
        )
        health = await Configuration._load_healthchecks_settings(config)
        media = MediaConfig(
            folder=config["MediaSettings"]["MediaFolder"],
            media_only=str_to_bool(config["MediaSettings"]["MediaPostsOnly"]),
        )
        mastodon_config = MastodonConfig(
            domain=config["Mastodon"]["InstanceDomain"],
            media_always_sensitive=str_to_bool(config["Mastodon"]["SensitiveMedia"]),
            post_visibility=config["Mastodon"].get("PostVisibility", "public"),
            throttling_enabled=str_to_bool(config["Mastodon"]["ThrottlingEnabled"]),
            throttling_max_delay=int(config["Mastodon"]["ThrottlingMaxDelay"]),
            number_of_errors=0,
            use_caption=config["Mastodon"].getboolean("UseCaption", fallback=True),
            use_tags=config["Mastodon"].getboolean("UseTags", fallback=True),
            use_backlink=config["Mastodon"].getboolean("UseBacklink", fallback=True),
        )
        subreddits = await Configuration._load_subreddits_settings(config)

        configuration = cls(
            bot=bot,
            subreddits=subreddits,
            promo=promo,
            health=health,
            media=media,
            mastodon_config=mastodon_config,
            reddit=reddit,
        )
        logger.debug("After loading of config: %s", configuration)
        return configuration

    @staticmethod
    async def _load_subreddits_settings(
        config: configparser.ConfigParser,
    ) -> List[SubredditConfig]:
        """Loads Subreddit configuration options."""
        subreddits = []
        for subreddit, hashtags in config.items("Subreddits"):
            subreddits.append(SubredditConfig(subreddit, hashtags.strip()))
        return subreddits

    @staticmethod
    async def _load_healthchecks_settings(
        config: configparser.ConfigParser,
    ) -> HealthCheckConfig:
        """Loads HealthChecks configuration options."""
        health_enabled = False
        if len(config["HealthChecks"]["BaseUrl"]) > 0:
            health_enabled = True
        health = HealthCheckConfig(
            enabled=health_enabled,
            base_url=config["HealthChecks"]["BaseUrl"],
            uuid=config["HealthChecks"]["UUID"],
        )
        return health

    @staticmethod
    async def _load_bot_settings(
        config: configparser.ConfigParser,
        config_dir: str,
    ) -> BotConfig:
        """Loads BotSettings configuration options."""
        hash_tags = []
        if config["BotSettings"]["Hashtags"]:
            # Parse list of hashtags
            hash_tags_string = config["BotSettings"]["Hashtags"]
            hash_tags = [x.strip() for x in hash_tags_string.split(",")]
        bot = BotConfig(
            post_recorder=PostRecorder(history_db_dir=config_dir),
            delay_between_posts=int(config["BotSettings"]["DelayBetweenPosts"]),
            run_once_only=str_to_bool(config["BotSettings"]["RunOnceOnly"]),
            hash_tags=hash_tags,
            log_level=config["BotSettings"]["LogLevel"],
        )
        await bot.post_recorder.db_init()
        return bot

    @staticmethod
    async def _set_up_logging(config: configparser.ConfigParser) -> None:
        """Set-up logging."""
        log_level = "INFO"
        if config["BotSettings"]["LogLevel"]:
            log_level = config["BotSettings"]["LogLevel"]

        std_out_formatter = Formatter(
            "%(name)s[%(process)d] %(levelname)s %(message)s",
            datefmt="%H:%M:%S",
        )
        std_out_handler = StreamHandler(sys.stdout)
        std_out_handler.setFormatter(std_out_formatter)
        std_out_handler.setLevel(log_level)
        logger.addHandler(std_out_handler)


def str_to_bool(value: Any) -> bool:
    """Helper function to convert a string into a boolean value.

    returns: bool
    """
    if not value:
        return False
    return str(value).lower() in ("y", "yes", "t", "true", "on", "1")
