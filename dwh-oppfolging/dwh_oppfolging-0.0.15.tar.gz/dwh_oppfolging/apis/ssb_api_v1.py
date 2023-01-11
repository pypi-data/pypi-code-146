# pylint: disable=missing-module-docstring
from datetime import datetime
import requests # type: ignore
from dwh_oppfolging.misc.transforms import dict_to_string, string_to_sha256_hash, string_to_naive_norwegian_datetime
from dwh_oppfolging.apis.ssb_api_v1_structs import Version, Correspondence

API_VERSION = 1
API_NAME = "SSB"
SEKTOR_ID = 39
NAERING_ID = 6
YRKESKATALOG_ID = 145
YRKESKLASSIFISERING_ID = 7
ORGANISASJONSFORM_ID = 35

_BASE_URL = (
    f"https://data.ssb.no/api/klass/v{API_VERSION}"  # classifications/{0}/changes"
)
_HEADERS = {"Accept": "application/json;charset=UTF-8"}
_VALID_DATE_FMT = "%Y-%m-%d"
_MODIFIED_DATE_FMT = "%Y-%m-%dT%H:%M:%S.%f%z"


def _convert_ssb_date(date: str | None, fmt: str):
    """converts ssb date string to datetime"""
    if date is None:
        return None
    converted_date = string_to_naive_norwegian_datetime(datetime.strptime(date, fmt).isoformat())
    return converted_date


def _build_version_struct(data: dict):
    """returns version struct"""
    url = data["_links"]["self"]["href"]
    version_id = int(url[url.rindex("/") + 1 :])
    version = Version(
        url,
        version_id,
        _convert_ssb_date(data["validFrom"], _VALID_DATE_FMT),
        _convert_ssb_date(data.get("validTo"), _VALID_DATE_FMT),
        _convert_ssb_date(data["lastModified"], _MODIFIED_DATE_FMT),
    )
    return version


def _build_correspondence_struct(data: dict):
    """returns correspondence struct"""
    url = data["_links"]["self"]["href"]
    correspondence_id = int(url[url.rindex("/") + 1 :])
    corr = Correspondence(
        url,
        correspondence_id,
        int(data["sourceId"]),
        int(data["targetId"]),
        _convert_ssb_date(data["lastModified"], _MODIFIED_DATE_FMT),
    )
    return corr


def _build_versioned_classification_code_record(
    classification_id: int,
    version: Version,
    data: dict,
    download_date: datetime,
):
    """returns row dict form that can be inserted into table"""
    record: dict = {}
    record["klassifikasjon_id"] = classification_id
    record["versjon_id"] = version.version_id
    record["gyldig_fom_tid_kilde"] = version.valid_from
    record["gyldig_til_tid_kilde"] = version.valid_to
    record["oppdatert_tid_kilde"] = version.last_modified
    record["api_versjon"] = API_VERSION
    record["data"] = dict_to_string(data)
    record["sha256_hash"] = string_to_sha256_hash(record["data"] + record["oppdatert_tid_kilde"].isoformat())
    record["lastet_dato"] = download_date
    record["kildesystem"] = API_NAME
    return record


def _build_correspondence_code_record(
    source_classification_id: int,
    target_classification_id: int,
    corr: Correspondence,
    data: dict,
    download_date: datetime,
):
    """returns row dict form that can be inserted into table"""
    record: dict = {}
    record["fra_klassifikasjon_id"] = source_classification_id
    record["fra_versjon_id"] = corr.source_version_id
    record["til_klassifikasjon_id"] = target_classification_id
    record["til_versjon_id"] = corr.target_version_id
    record["oppdatert_tid_kilde"] = corr.last_modified
    record["api_versjon"] = API_VERSION
    record["data"] = dict_to_string(data)
    record["sha256_hash"] = string_to_sha256_hash(record["data"])
    record["lastet_dato"] = download_date
    record["kildesystem"] = API_NAME
    return record


def _get_all_versions_for_classification(classification_id: int):
    """returns list of classification version metadata"""
    url = _BASE_URL + "/classifications/" + str(classification_id)
    resp = requests.get(url, headers=_HEADERS, proxies={}, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    versions = [_build_version_struct(entry) for entry in data["versions"]]

    if len(versions) == 0:
        print("found no versions for classification", classification_id)
    else:
        print(
            "found version" + "s" * (len(versions) > 1),
            ", ".join(str(version.version_id) for version in versions[:-1])
            + (len(versions) > 1) * ", and "
            + str(versions[-1].version_id),
            "for classification",
            classification_id,
        )

    return versions


def _get_all_correspondences_for_classification_version(version: Version):
    """gets corrspondance tables, a bit heavy since the api doesnt support
    listing the correspondence tables in the ../classification/<id> response
    instead they are only available in the /version/ endpoint,
    which means we are forced to download version with all its classification codes
    even when we will not need them...
    """
    resp = requests.get(version.url, headers=_HEADERS, proxies={}, timeout=10)
    data = resp.json()
    corrs = [
        _build_correspondence_struct(entry) for entry in data["correspondenceTables"]
    ]

    if len(corrs) == 0:
        print("found no correspondences for version", version.version_id)
    else:
        print(
            "found correspondence between target version" + "s" * (len(corrs) > 1),
            ", ".join(str(corr.target_version_id) for corr in corrs[:-1])
            + (len(corrs) > 1) * ", and "
            + str(corrs[-1].target_version_id),
            "and source version",
            version.version_id,
        )

    return corrs


def _get_all_records_in_classification_version(
    classification_id: int, version: Version, download_date: datetime
):
    """returns list of codes as records for given version of classification"""
    resp = requests.get(version.url, headers=_HEADERS, proxies={}, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    records = [
        _build_versioned_classification_code_record(
            classification_id,
            version,
            code,
            download_date,
        )
        for code in data["classificationItems"]
    ]
    print("found", len(records), "records for version", version.version_id)
    return records


def _get_all_records_in_correspondence(
    source_classification_id: int,
    target_classification_id: int,
    corr: Correspondence,
    download_date: datetime,
):
    """returns list of correspondence-codes as records for given correspondence"""
    resp = requests.get(corr.url, headers=_HEADERS, proxies={}, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    records = [
        _build_correspondence_code_record(
            source_classification_id,
            target_classification_id,
            corr,
            code,
            download_date,
        )
        for code in data["correspondenceMaps"]
    ]
    return records


def get_latest_records_for_classification(
    last_modified_date: datetime, download_date: datetime, classification_id: int
):
    """gets all codes with versions"""
    records = []
    for version in _get_all_versions_for_classification(classification_id):
        if not version.last_modified > last_modified_date:
            print("skipping too old version last modified on", version.last_modified)
            continue
        records += _get_all_records_in_classification_version(
            classification_id, version, download_date
        )
    return records


def get_latest_records_for_correspondance(
    last_modified_date: datetime,
    download_date: datetime,
    source_classification_id: int,
    target_classification_id: int,
):
    """gets all corresponence codes with versions"""
    records = []

    print("looking for versions of source classification", source_classification_id)
    source_versions = _get_all_versions_for_classification(source_classification_id)

    print("looking for versions of target classification", target_classification_id)
    target_versions = _get_all_versions_for_classification(target_classification_id)
    target_version_ids = set(targ.version_id for targ in target_versions)

    for src in source_versions:
        for corr in _get_all_correspondences_for_classification_version(src):
            if not corr.target_version_id in target_version_ids:
                print("skipping correspondence to unknown target classification")
                continue
            if not corr.last_modified > last_modified_date:
                print(
                    "skipping too old correspondence last modified on",
                    corr.last_modified,
                )
                continue
            records += _get_all_records_in_correspondence(
                source_classification_id, target_classification_id, corr, download_date
            )
    return records
