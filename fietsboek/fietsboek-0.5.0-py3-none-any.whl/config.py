"""Configuration parsing for Fietsboek.

Fietsboek mostly relies on pyramid's INI parsing to get its configuration,
however, there are quite a a few custom values that we add/need. Instead of
manually sprinkling ``settings.get(...)`` all over the code, we'd rather just
do it once at application startup, make sure that the values are well-formed,
provide the user with good feedback if they aren't, and set the default values
in a single place.

Most of the logic is handled by pydantic_.

.. _pydantic: https://pydantic-docs.helpmanual.io/
"""
# pylint: disable=no-name-in-module,no-self-argument,too-few-public-methods
import hashlib
import logging
import re
import typing
import urllib.parse
from enum import Enum

import pydantic
from pydantic import AnyUrl, BaseModel, DirectoryPath, Field, SecretStr, validator
from pyramid import settings
from termcolor import colored

LOGGER = logging.getLogger(__name__)

KNOWN_PYRAMID_SETTINGS = {
    "pyramid.reload_templates",
    "pyramid.reload_assets",
    "pyramid.debug_authorization",
    "pyramid.debug_notfound",
    "pyramid.debug_routematch",
    "pyramid.prevent_http_cache",
    "pyramid.prevent_cachebust",
    "pyramid.debug_all",
    "pyramid.reload_all",
    "pyramid.default_locale_name",
    "pyramid.includes",
    "pyramid.tweens",
    "pyramid.reload_resources",
    "retry.attempts",
}

KNOWN_TILE_LAYERS = [
    "osm",
    "osmde",
    "satellite",
    "opentopo",
    "topplusopen",
    "opensea",
    "cycling",
    "hiking",
]


class ValidationError(Exception):
    """Exception for malformed configurations.

    This provides a nice str() representation that can be printed out.
    """

    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        lines = [""]
        for where, error in self.errors:
            lines.append(colored(f"Error in {where}:", "red"))
            lines.append(str(error))
        return "\n".join(lines)


class LayerType(Enum):
    """Enum to distinguish base layers and overlay layers."""

    BASE = "base"
    OVERLAY = "overlay"


class LayerAccess(Enum):
    """Enum discerning whether a layer is publicly accessible or restriced to
    logged-in users.

    Note that in the future, a finer-grained distinction might be possible.
    """

    PUBLIC = "public"
    RESTRICTED = "restricted"


class PyramidList(list):
    """A pydantic field type that uses pyramid.settings.aslist as a parser."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        """Parses the list with pyramid.settings.aslist."""
        if not isinstance(value, str):
            raise TypeError("string required")
        return settings.aslist(value)


class TileLayerConfig(BaseModel, allow_population_by_field_name=True):
    """Object representing a single tile layer."""

    layer_id: str
    """ID of the layer."""

    name: str
    """Human-readable name of the layer."""

    url: AnyUrl
    """URL of the layer tiles (with placeholders)."""

    layer_type: LayerType = Field(LayerType.BASE, alias="type")
    """Type of the layer."""

    zoom: typing.Optional[int] = 22
    """Maximum zoom factor of the layer."""

    attribution: str = ""
    """Attribution of the layer copyright."""

    access: LayerAccess = LayerAccess.PUBLIC
    """Layer access restriction."""


class Config(BaseModel):
    """Object representing the Fietsboek configuration."""

    sqlalchemy_url: str = Field(alias="sqlalchemy.url")
    """SQLAlchemy URL."""

    redis_url: str = Field(alias="redis.url")
    """Redis URL."""

    data_dir: DirectoryPath = Field(alias="fietsboek.data_dir")
    """Fietsboek data directory."""

    enable_account_registration: bool = False
    """Enable registration of new accounts."""

    session_key: str
    """Session key."""

    language_packs: PyramidList = Field([], alias="fietsboek.language_packs")
    """Additional language packs to load."""

    available_locales: PyramidList = PyramidList(["en", "de"])
    """Available locales."""

    email_from: str = Field(alias="email.from")
    """Email sender address."""

    email_smtp_url: str = Field(alias="email.smtp_url")
    """Email SMTP server."""

    email_username: str = Field("", alias="email.username")
    """SMTP username (optional)."""

    email_password: SecretStr = Field(SecretStr(""), alias="email.password")
    """SMTP password (optional)."""

    pages: PyramidList = Field([], alias="fietsboek.pages")
    """Custom pages."""

    default_tile_layers: PyramidList = Field(
        KNOWN_TILE_LAYERS, alias="fietsboek.default_tile_layers"
    )
    """The subset of the default tile layers that should be enabled.

    By default, that's all of them.
    """

    thunderforest_key: SecretStr = Field(SecretStr(""), alias="thunderforest.api_key")
    """API key for the Thunderforest integration."""

    thunderforest_maps: PyramidList = Field([], alias="thunderforest.maps")
    """List of enabled Thunderforest maps."""

    thunderforest_access: LayerAccess = Field(LayerAccess.RESTRICTED, alias="thunderforest.access")
    """Thunderforest access restriction."""

    stamen_maps: PyramidList = Field([], alias="stamen.maps")
    """Enabled stamen maps."""

    disable_tile_proxy: bool = Field(False, alias="fietsboek.tile_proxy.disable")
    """Disable the tile proxy."""

    tile_layers: typing.List[TileLayerConfig] = []
    """Tile layers."""

    @validator("session_key")
    def _good_session_key(cls, value):
        """Ensures that the session key has been changed from its default
        value.
        """
        if value == "<EDIT THIS>":
            raise ValueError("You need to edit the default session key!")
        return value

    @validator("email_smtp_url")
    def _known_smtp_url(cls, value):
        """Ensures that the SMTP URL is valid."""
        parsed = urllib.parse.urlparse(value)
        if parsed.scheme not in {"debug", "smtp", "smtp+ssl", "smtp+starttls"}:
            raise ValueError(f"Unknown mailing scheme {parsed.scheme}".strip())
        return value

    @validator("stamen_maps")
    def _known_stamen(cls, value):
        """Ensures that the stamen maps are known."""
        maps = set(value)
        known_maps = {"toner", "terrain", "watercolor"}
        bad_maps = maps - known_maps
        if bad_maps:
            raise ValueError("Unknown stamen maps: " + ", ".join(bad_maps))
        return value

    def derive_secret(self, what_for):
        """Derive a secret for other parts of the application.

        All secrets are derived from ``secret_key`` in a deterministic way. See
        https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html#admonishment-against-secret-sharing
        on why ``secret_key`` should not be used directly.

        :param what_for: What the secret is used for. Passing the same "use
            case" will generate the same secret.
        :type what_for: str
        :return: The generated secret.
        :rtype: str
        """
        hasher = hashlib.sha256()
        hasher.update(f"{len(what_for)}".encode("utf-8"))
        hasher.update(self.session_key.encode("utf-8"))
        hasher.update(what_for.encode("utf-8"))
        return hasher.hexdigest()


def parse(config):
    """Parses the configuration into a :class:`Config`.

    :param config: The configuration dict to parse.
    :type config: dict
    :return: The parsed (and validated) configuration.
    :rtype: Config
    :raises ValidationError: When the configuration is malformed.
    """
    config = config.copy()
    keys = set(config.keys())
    errors = []
    # First, we try to extract the tile layers.
    tile_layers = []
    for key, value in config.items():
        match = re.match("^fietsboek\\.tile_layer\\.([A-Za-z0-9_-]+)$", key)
        if not match:
            continue
        provider_id = match.group(1)

        prefix = f"{value}."
        inner = {k[len(prefix) :]: v for (k, v) in config.items() if k.startswith(prefix)}
        inner["layer_id"] = provider_id
        inner["name"] = value
        try:
            layer_config = TileLayerConfig.parse_obj(inner)
            tile_layers.append(layer_config)
        except pydantic.ValidationError as validation_error:
            errors.append((f"tile layer {provider_id}", validation_error))

        keys.discard(key)
        for field in TileLayerConfig.__fields__.values():
            keys.discard(f"{prefix}{_field_name(field)}")

    config["tile_layers"] = tile_layers

    # Now we can parse the main config
    try:
        config = Config.parse_obj(config)
    except pydantic.ValidationError as validation_error:
        errors.append(("configuration", validation_error))

    if errors:
        raise ValidationError(errors)

    for field in Config.__fields__.values():
        keys.discard(_field_name(field))
    keys -= KNOWN_PYRAMID_SETTINGS

    for key in keys:
        LOGGER.warning("Unknown configuration key: %r", key)

    return config


def _field_name(field):
    alias = getattr(field, "alias", None)
    if alias:
        return alias
    return field.name
