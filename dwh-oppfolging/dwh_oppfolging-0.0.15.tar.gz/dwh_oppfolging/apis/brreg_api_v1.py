# pylint: disable=missing-module-docstring
# pylint: disable=line-too-long
from typing import Generator
from datetime import datetime
import gzip
import requests # type: ignore
import ijson # type: ignore
from dwh_oppfolging.misc.transforms import dict_to_string, string_to_sha256_hash, string_to_naive_norwegian_datetime
from dwh_oppfolging.apis.brreg_api_v1_structs import PagedRequestForEmbeddedList, Update


API_VERSION = 1
API_NAME = "BRREG"
UNIT_NAME_ENHET = "enheter"
UNIT_NAME_UNDERENHET = "underenheter"

_BASE_URL = "https://data.brreg.no/enhetsregisteret/api"
_HEADERS_FMT = "application/vnd.brreg.enhetsregisteret.{unit_name}.v" + str(API_VERSION) + "+{ftype};charset=UTF-8"


def _build_headers(unit_name: str, ftype: str = "json"):
    headers = {"Accept": _HEADERS_FMT.format(unit_name=unit_name[:-2], ftype=ftype)}
    return headers


def _convert_brreg_date(date: str | None):
    """converts brreg date string to datetime"""
    if date is None:
        return None
    converted_date = string_to_naive_norwegian_datetime(date.replace("Z", "+00:00"))
    return converted_date


def _build_update_struct(data: dict):
    """returns Update struct"""
    update = Update(
        data["organisasjonsnummer"],
        data["endringstype"],
        _convert_brreg_date(data["dato"]),
    )
    return update


def _build_unit_record(update: Update, fact: dict, download_date: datetime):
    """returns row in dict form
    NB: may delete field in fact"""
    fact.pop("_links", None)
    fact.get("organisasjonsform", {}).pop("_links", None)
    record = {}
    record["organisasjonsnummer"] = update.orgnr
    record["endringstype"] = update.change
    record["oppdatert_tid_kilde"] = update.last_modified
    record["api_versjon"] = API_VERSION
    record["data"] = dict_to_string(fact)
    record["sha256_hash"] = string_to_sha256_hash(record["data"] + record["oppdatert_tid_kilde"].isoformat())
    record["lastet_dato"] = download_date
    record["kildesystem"] = API_NAME
    return record


def _get_unit_record_from_update_single(update: Update, unit_name: str, download_date: datetime):
    """returns a unit record
    makes a single request to get the latest fact for a single orgnr"""
    url = _BASE_URL + "/" + unit_name + "/" + update.orgnr
    headers = _build_headers(unit_name)
    response = requests.get(url, headers=headers, proxies={}, timeout=100)
    fact = response.json()
    return _build_unit_record(update, fact, download_date)


def _get_unit_record_from_update_batch(orgnr_update_lkp: dict[str, Update], unit_name: str, download_date: datetime, page_size: int = 500):
    """Returns {orgnr: record} constructed by searching for details for orgs in given {orgnr: update}
    NB: the dict of updates may have elements removed.
    Org details will not be found if the org has been deleted at any point in the past,
    as this seems to remove them from the search endpoint.
    """
    url = _BASE_URL + "/" + unit_name
    params = {
        "organisasjonsnummer": ",".join(orgnr for orgnr in orgnr_update_lkp),
        "sort": "organisasjonsnummer,ASC",
    }
    headers = _build_headers(unit_name)
    list_key = unit_name
    orgnr_record_lkp: dict = {}
    for facts in PagedRequestForEmbeddedList(url, params, headers, {}, page_size, list_key, timeout=100):
        orgnr_record_lkp |= {
            fact["organisasjonsnummer"]:
                _build_unit_record(orgnr_update_lkp.pop(fact["organisasjonsnummer"]), fact, download_date)
            for fact in facts
        }

    return orgnr_record_lkp


def get_latest_records_for_unit(download_date: datetime, last_modified_date: datetime, unit_name: str, page_size=500):
    """params:
        last_modified_date: smallest update date
        unit_name: enheter | undereneheter
    returns list of records"""
    url = _BASE_URL + "/oppdateringer/" + unit_name
    headers = _build_headers("oppdatering." + unit_name)
    list_key = "oppdaterte" + unit_name.capitalize()
    params = {"dato": last_modified_date.isoformat(timespec="milliseconds") + "Z"}
    orgnr_record_lkp: dict = {} # {orgnr from latest update for that orgnr: latest fact for that orgnr}
    for updates in PagedRequestForEmbeddedList(url, params, headers, {}, page_size, list_key, timeout=100):
        # only keep the latest updates for each orgnr
        # since updates is already sorted with ascending update id, we can just overwrite
        orgnr_update_lkp = {update.orgnr: update for update in map(_build_update_struct, updates)}

        old_length = len(orgnr_update_lkp)
        orgnr_record_lkp_batch = _get_unit_record_from_update_batch(orgnr_update_lkp, unit_name, download_date)
        new_length = len(orgnr_update_lkp)
        print(f"found {old_length - new_length} of {old_length} orgs with batched search")
        print("appending remaining using single requests")
        orgnr_record_lkp_batch |= {
            orgnr: _get_unit_record_from_update_single(update, unit_name, download_date)
            for orgnr, update in orgnr_update_lkp.items()
        }

        orgnr_record_lkp |= orgnr_record_lkp_batch

    return list(orgnr_record_lkp.values())


def stream_latest_records_for_unit_from_file(download_date: datetime, unit_name: str, batch_size: int = 1000) -> Generator[list, None, None]:
    """yields [records] from large file
        must be run some time after 5
    """
    assert datetime.today().hour > 5, "too early"
    updated_date_str = datetime.today().replace(hour=5, minute=0, second=0).isoformat(timespec="milliseconds")+"Z"
    url = _BASE_URL + "/" + unit_name + "/" + "lastned"
    headers = _build_headers(unit_name, "gzip")
    print("requesting filestream from api")
    with requests.get(url, headers=headers, proxies={}, stream=True, timeout=100) as response:
        response.raise_for_status()
        print("decompressing filestream")
        with gzip.open(response.raw, "rb") as file:
            records = []
            print("iterating over json objects")
            for record in ijson.items(file, "item"):  # type: ignore
                records.append(
                    _build_unit_record(
                        _build_update_struct(
                            {
                                "organisasjonsnummer": record["organisasjonsnummer"],
                                "endringstype": "INIT",
                                "dato": updated_date_str
                            }
                        ),
                        record,
                        download_date,
                    )
                )
                if len(records) >= batch_size:
                    yield records
                    records = []
            if len(records) > 0:
                yield records
