"""Flywheel import metadata extraction fields and utilities."""
# check out the core-api input validation regexes for field loading context:
# https://gitlab.com/flywheel-io/product/backend/core-api/-/blob/master/core/models/regex.py
import enum
import json
import re
import typing as t
from collections import defaultdict
from functools import cached_property
from pathlib import Path

import fw_utils
import pathvalidate
from fw_utils import AttrDict, Pattern, Template, get_field, parse_field_name
from pydantic import BaseModel, Field, PrivateAttr, root_validator

from .aliases import ALIASES

__all__ = ["MetaData", "MetaExtractor", "extract_meta"]


class MetaData(dict):
    """Flywheel metadata dict with sorted/validated keys and attr access."""

    def __setitem__(self, name: str, value) -> None:
        """Validate/canonize field names before setting keys."""
        super().__setitem__(validate_import_field(name), value)

    def __getattr__(self, name: str):
        """Return dictionary keys as attributes."""
        return getattr(self.dict, name)

    def __iter__(self):
        """Return dict key iterator respecting the hierarchy/field order."""
        return iter(sorted(super().keys(), key=self.sort_key))

    @staticmethod
    def sort_key(field: str):
        """Return sorting key to order meta fields by hierarchy/importance."""
        return IMPORT_FIELD_NUM[field], field

    def keys(self):
        """Return dict keys, sorted."""
        return list(self)

    def values(self):
        """Return dict values, sorted."""
        return [self[k] for k in self]

    def items(self):
        """Return key, value pairs, sorted."""
        return iter((k, self[k]) for k in self)

    @property
    def dict(self) -> AttrDict:
        """Return inflated metadata dict ready for Flywheel uploads."""
        return AttrDict.from_flat(self)

    @property
    def json(self) -> bytes:
        """Return JSON dump of the inflated meta."""
        return json.dumps(self.dict, separators=(",", ":")).encode()


Mappings = t.Union[str, t.List[t.Union[t.Tuple[str, str], str]], t.Dict[str, str]]


class MetaExtractor:  # pylint: disable=too-few-public-methods
    """Meta Extractor."""

    def __init__(
        self,
        *,
        mappings: Mappings = None,
        defaults: Mappings = None,
        overrides: Mappings = None,
        customize: t.Callable[[dict, dict], None] = None,
    ) -> None:
        """Validate, compile and (functools)cache metadata extraction mapping patterns."""
        # load/validate mapping patterns
        # TODO allow mapping expressions in reverse order
        # be aware of file.path and (fileinfo.)path conflict
        self.mappings = [
            (Template(t), ImportPattern(p))
            for t, p in parse_metadata_mappings(mappings or [])
        ]
        # validate default fields and values
        self.defaults = dict(
            load_field_tuple(field, default)
            for field, default in parse_metadata_mappings(defaults or [])
        )
        # validate override fields and values
        self.overrides = dict(
            load_field_tuple(field, override)
            for field, override in parse_metadata_mappings(overrides or [])
        )
        self.customize = customize

    @cached_property
    def fields(self) -> t.Set[str]:
        """Return set of fields appear in the mappings/defaults/overrides."""
        return set().union(
            self.defaults.keys(),
            self.overrides.keys(),
            *[p.fields for _, p in self.mappings],
        )

    def extract(self, data: t.Any) -> MetaData:  # pylint: disable=too-many-locals
        """Extract metadata from given dict like object."""
        meta: t.Dict[str, t.Any] = {}

        def setdefault(field, value):
            if value not in ("", None):
                field, value = load_field_tuple(field, value)
                meta.setdefault(field, value)

        for template, pattern in self.mappings:
            values = [get_field(data, field) for field in template.fields]
            if any(value in ("", None) for value in values):
                # skip if data doesn't have a value for one or more keys
                continue
            for field, value in pattern.match(template.format(data)).to_flat().items():
                # setdefault allows using multiple patterns as fallback
                setdefault(field, value)
        # apply user-defaults (eg. {'project.label': 'Default Project'})
        for field, user_default in self.defaults.items():
            setdefault(field, user_default)
        # apply file-defaults (eg. {'session.label': 'StudyDescription'})
        default_meta: dict = getattr(data, "get_default_meta", lambda: {})()
        for field, file_default in default_meta.items():
            setdefault(field, file_default)
        # apply user-overrides (eg. {'project.label': 'Override Project'})
        for field, user_override in self.overrides.items():
            meta[field] = user_override
        # set timezone if timestamp present
        for prefix in ("session", "acquisition"):
            ts_field, tz_field = f"{prefix}.timestamp", f"{prefix}.timezone"
            dt = meta.get(ts_field)
            if dt:
                meta[ts_field] = dt.isoformat(timespec="milliseconds")
                meta[tz_field] = getattr(dt.tzinfo, "key", dt.tzname())
        # trigger user-callback if given for further meta customization
        if self.customize is not None:
            self.customize(data, meta)
        return MetaData(meta)


def extract_meta(
    data: t.Any,
    *,
    mappings: Mappings = None,
    defaults: Mappings = None,
    overrides: Mappings = None,
    customize: t.Callable[[dict, dict], None] = None,
) -> MetaData:
    """Extract Flywheel metadata from a dict like object."""
    # NOTE using the class enables validation and caching
    meta_extractor = MetaExtractor(
        mappings=mappings,
        defaults=defaults,
        overrides=overrides,
        customize=customize,
    )
    return meta_extractor.extract(data)


def load_group_id(value: str) -> t.Optional[str]:
    """Normalize to lowercase and return validated value (or None)."""
    group_id = value.lower()
    if re.match(r"^[0-9a-z][0-9a-z.@_-]{0,62}[0-9a-z]$", group_id):
        return group_id
    return None


def load_cont_id(value: str) -> t.Optional[str]:
    """Normalize to lowercase and return validated value (or None)."""
    cont_id = value.lower()
    if re.match(r"^[0-9a-f]{24}$", cont_id):
        return cont_id
    return None


def load_cont_label(value: str, trunc: int = 64) -> str:
    """Normalize for path compatibility as core would and truncate if needed."""
    label = value.replace("*", "star")  # retain T2* MR context
    label = str(pathvalidate.sanitize_filename(label, replacement_text="_"))
    return label[:trunc] if trunc else label


def load_acq_label(value: str) -> str:
    """Normalize for path compatibility but truncate at 128 instead of 64."""
    return load_cont_label(value, trunc=128)


def load_file_name(value: t.Union[str, Path]) -> str:
    """Normalize for path compatibility without truncating."""
    name = value.as_posix() if isinstance(value, Path) else value
    return load_cont_label(name, trunc=0)


def load_subj_sex(value: str) -> t.Optional[str]:
    """Normalize to lowercase and return validated value (or None)."""
    subj_sex = value.lower()
    subj_sex_map = {"m": "male", "f": "female", "o": "other"}  # dicom
    subj_sex = subj_sex_map.get(subj_sex, subj_sex)
    if re.match(r"^male|female|other|unknown$", subj_sex):
        return subj_sex
    return None


# TODO
# def load_subj_type(value: str) -> t.Optional[str]:
#     """Return validated subject type (or None)."""
#     human|animal|phantom


# def load_subj_race(value: str) -> t.Optional[str]:
#     """Return validated subject race (or None)."""
#     r"American Indian or Alaska Native|Asian"
#     r"|Native Hawaiian or Other Pacific Islander|Black or African American|White"
#     r"|More Than One Race|Unknown or Not Reported"


# def load_subj_ethnicity(value: str) -> t.Optional[str]:
#     """Return validated subject ethnicity."""
#     Not Hispanic or Latino|Hispanic or Latino|Unknown or Not Reported


def load_sess_age(value: t.Union[str, int, float]) -> t.Optional[int]:
    """Return as a validated integer (or None)."""
    # NOTE add unit conversion here if/when needed later [target: seconds]
    try:
        return int(value)
    except ValueError:
        return None


def load_sess_weight(value: t.Union[str, int, float]) -> t.Optional[float]:
    """Return as a validated float (or None)."""
    # NOTE add unit conversion here if/when needed later [target: kilograms]
    try:
        return float(value)
    except ValueError:
        return None


def load_tags(value: str) -> list:
    """Return list of strings split by comma."""
    return value.split(",") if value else []


def load_any(value):
    """Return value as-is."""
    return value  # pragma: no cover


def load_field_tuple(field: str, value) -> t.Tuple[str, t.Any]:
    """Return validated field name and value as a tuple."""
    field = validate_import_field(field)
    value = IMPORT_FIELD_LOADERS.get(field, load_any)(value)
    return field, value


IMPORT_FIELD_LOADERS: t.Dict[str, t.Callable] = {
    "external_routing_id": load_any,
    "group._id": load_group_id,
    "group.label": load_cont_label,
    "project._id": load_cont_id,
    "project.label": load_cont_label,
    "subject._id": load_cont_id,
    "subject.label": load_cont_label,
    "subject.firstname": load_any,
    "subject.lastname": load_any,
    "subject.sex": load_subj_sex,
    # "subject.type": load_subj_type,
    # "subject.race": load_subj_race,
    # "subject.ethnicity": load_subj_ethnicity,
    "subject.species": load_any,
    "subject.strain": load_any,
    "subject.tags": load_tags,
    "subject.info.*": load_any,
    "session._id": load_cont_id,
    "session.uid": load_any,
    "session.label": load_cont_label,
    "session.age": load_sess_age,
    "session.weight": load_sess_weight,
    "session.operator": load_any,
    "session.timestamp": Pattern.load_timestamp,
    # session.timezone is auto-populated
    "session.tags": load_tags,
    "session.info.*": load_any,
    "acquisition._id": load_cont_id,
    "acquisition.uid": load_any,
    "acquisition.label": load_acq_label,
    "acquisition.timestamp": Pattern.load_timestamp,
    # acquisition.timezone is auto-populated
    "acquisition.tags": load_tags,
    "acquisition.info.*": load_any,
    "file.name": load_file_name,
    "file.type": load_any,
    "file.tags": load_tags,
    "file.info.*": load_any,
    "file.path": str,
    "file.provider_id": str,
    "file.reference": bool,
    "file.size": int,
    "file.client_hash": str,
    "file.zip_member_count": int,
}
IMPORT_FIELDS = list(IMPORT_FIELD_LOADERS)
IMPORT_FIELD_INDEX = {field: index for index, field in enumerate(IMPORT_FIELDS)}
IMPORT_FIELD_NUM = defaultdict(lambda: len(IMPORT_FIELDS), IMPORT_FIELD_INDEX)


def validate_import_field(field: str) -> str:
    """Return validated/canonic import field name for the field shorthand."""
    return parse_field_name(field, aliases=ALIASES, allowed=IMPORT_FIELDS)


class ImportPattern(Pattern):
    """Import pattern for extracting Flywheel metadata fields from strings."""

    def __init__(self, pattern: str) -> None:
        """Init pattern with field name validators and value loaders."""
        super().__init__(
            pattern,
            validate=validate_import_field,
            loaders=IMPORT_FIELD_LOADERS,
        )


# RULES


class StrEnum(str, enum.Enum):
    """String enum."""

    def __str__(self) -> str:
        """Return string representation of a level."""
        return self.name  # pragma: no cover


class ImportLevel(StrEnum):
    """Flywheel hierarchy levels with files."""

    # TODO enable all upload levels
    # project = "project"
    # subject = "subject"
    # session = "session"
    acquisition = "acquisition"


LEVELS = list(ImportLevel)

IMPORT_FILTERS = {
    # fields that are available when scanning filesystem
    "path": fw_utils.StringFilter,
    "size": fw_utils.SizeFilter,
    "created": fw_utils.TimeFilter,
    "modified": fw_utils.TimeFilter,
    # everything else available once we parsed the file
    "*": fw_utils.StringFilter,
}


def validate_import_filter_field(field: str) -> str:
    """Return validated/canonic import filter field name for the field shorthand."""
    return fw_utils.parse_field_name(field, allowed=list(IMPORT_FILTERS))


class ImportFilter(fw_utils.IncludeExcludeFilter):
    """Import include/exclude filter with field validation and filter types."""

    def __init__(
        self,
        include: list[str] = None,
        exclude: list[str] = None,
    ) -> None:
        """Init filter with field name validators and filter types."""
        super().__init__(
            IMPORT_FILTERS,
            include=include,
            exclude=exclude,
            validate=validate_import_filter_field,
        )


class ImportRule(BaseModel):
    """Import rule defining what to import and how."""

    # TODO rename here and in export to container
    # TODO add depth, dirname and filename to filters (fs-like only)
    level: ImportLevel = Field(
        ImportLevel.acquisition,
        title="Flywheel hierarchy level to import files to",
    )
    include: list[str] | None = Field(
        title=(
            "Include filters - if given, "
            "only include files matching at least one include filter"
        ),
        example=["path=~.dcm"],
    )
    exclude: list[str] | None = Field(
        title=(
            "Exclude filters - if given, "
            "exclude files matching any of the exclude filters"
        ),
        example=["path=~meta.json"],
    )
    mappings: Mappings = Field(
        title="Metadata mapping patterns",
        example=[
            ("path", "{sub}/{ses}/{acq}/{file}"),
            ("path", "{file.info.original_path}"),
        ],
    )
    defaults: Mappings | None = Field(
        title="Metadata fallback defaults",
        example={"session.label": "control"},
    )
    overrides: Mappings | None = Field(
        title="Metadata manual overrides",
        example={"subject.label": "ex1000"},
    )

    @property
    def meta_fields(self) -> t.Set[str]:
        """Return metadata fields that are present in the rule."""
        return self.extractor.fields

    @root_validator(skip_on_failure=True)
    @classmethod
    def validate_rule(cls, values: dict) -> dict:
        """Validate the filters and the mappings given the level constraint."""
        level = ImportLevel(values.setdefault("level", "acquisition"))
        # sanity check that level is acquisition for know
        assert level == ImportLevel.acquisition, f"Unsupported import level {level}"
        # validate filters
        filt = ImportFilter(
            include=values.get("include"),
            exclude=values.get("exclude"),
        )
        values["include"] = [str(i) for i in filt.include]
        values["exclude"] = [str(e) for e in filt.exclude]
        # validate patterns
        extractor = MetaExtractor(
            mappings=values.get("mappings"),
            defaults=values.get("defaults"),
            overrides=values.get("overrides"),
        )
        values["mappings"] = [(str(t), str(p)) for t, p in extractor.mappings]
        values["defaults"] = extractor.defaults
        values["overrides"] = extractor.overrides
        assert values["mappings"], "At least one pattern is required"
        return values

    _filter: ImportFilter = PrivateAttr(None)
    _extractor: MetaExtractor = PrivateAttr(None)

    @property
    def filter(self) -> ImportFilter:
        """Return initialized import filter instance."""
        if not self._filter:
            self._filter = ImportFilter(include=self.include, exclude=self.exclude)
        return self._filter

    @property
    def extractor(self) -> MetaExtractor:
        """Return initialized meta extractor instance."""
        if not self._extractor:
            self._extractor = MetaExtractor(
                mappings=self.mappings,
                defaults=self.defaults,
                overrides=self.overrides,
            )
        return self._extractor

    def match(self, value) -> bool:
        """Return True if the values passes the include/exclude filters."""
        return self.filter.match(value)

    def extract(self, value: dict) -> MetaData | None:
        """Extract metadata."""
        if not self.match(value):
            return None  # pragma: no cover
        return self.extractor.extract(value)


# HELPERS


def parse_metadata_mappings(mappings: Mappings) -> t.Iterable[t.Tuple[str, str]]:
    """Parse and yield metadata mappings as a tuple."""
    if isinstance(mappings, str):
        mappings = [mappings]
    elif isinstance(mappings, dict):
        mappings = list(mappings.items())
    for mapping in mappings:
        if isinstance(mapping, str):
            yield mapping.split("=", maxsplit=1)  # type: ignore
        else:
            yield mapping
