#!/usr/bin/env python3

"""
Script to download MEX & MAVEN data.
"""

import functools
import re
import shutil
import string
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple
from urllib.parse import unquote

import arrow
import numpy
import requests
import spiceypy as spice
import yaml
from bs4 import BeautifulSoup
from pudb import set_trace as bp  # noqa: F401
from tqdm import tqdm
from urlpath import URL as Url

import radiocc
from radiocc.model import KernelVersion, ProcessType
from radiocc.utils import form_choice, print_validation, raise_error


def update_ROSE_query_id(URL: Url, CHANGES_ON_QUERY: Callable[[Url], Url]) -> Url:
    """To update URL."""
    QUERIES = dict(URL.form)
    QUERIES["id"] = str(CHANGES_ON_QUERY(Url(QUERIES["id"][0])))
    return URL.with_query(QUERIES)


# Planetary Data Science
# Radio Occultation Science Experiment
URL_PDS = Url("https://pds-ppi.igpp.ucla.edu")
PDS_URLPATH_SEARCH = "search/view"
PDS_URLPATH_DOWNLOAD = "ditdos/write"
PDS_QUERY = Url("pds://PPI")
URL_MAVEN_ROSE_ROOT_SEARCH = (
    (URL_PDS / PDS_URLPATH_SEARCH).add_query(f="yes").add_query(id=PDS_QUERY)
)
URL_MAVEN_ROSE_ROOT_DOWNLOAD = (URL_PDS / PDS_URLPATH_DOWNLOAD).add_query(id=PDS_QUERY)

# Different bundles exists.
TEMPLATE_MAVEN_ROSE_BUNDLE = string.Template("maven.rose.${BUNDLE}")

# Bundles:
# + raw (l0)
# + derived (l2)
# + calibrated (l3)
MAVEN_ROSE_BUNDLE_DATA_PATHS = dict(
    raw="data/rsr",
    calibrated="data/sky",
    # derived="data/edp",
)

# Create a URL for each ROSE bundle.
URLS_MAVEN_ROSE_SEARCH = {
    BUNDLE: update_ROSE_query_id(
        URL_MAVEN_ROSE_ROOT_SEARCH,
        lambda x: x / TEMPLATE_MAVEN_ROSE_BUNDLE.substitute(BUNDLE=BUNDLE) / DATA_PATH,
    )
    for (BUNDLE, DATA_PATH) in MAVEN_ROSE_BUNDLE_DATA_PATHS.items()
}

URL_MAVEN_SPICE = Url(
    "https://naif.jpl.nasa.gov/pub/naif/pds/pds4/maven/maven_spice/spice_kernels/mk"
)

URLS = dict(
    MAVEN=(
        dict(
            ROSE=URLS_MAVEN_ROSE_SEARCH,
            SPICE=URL_MAVEN_SPICE,
        )
    ),
    # MEX=None,
)

MAVEN_MK_RGX = r"maven_\d{4}_v\d{2}\.tm"
MAVEN_MK_RGX_GROUP = r"maven_(\d{4})_v(\d{2})\.tm"
REGEX_TEMPLATE_MAVEN_ROSE_YEARS = string.Template("${DATA_PATH}/\\d{4}")
REGEX_TEMPLATE_MAVEN_ROSE_YEAR_GROUP = string.Template("${DATA_PATH}/(\\d{4})")
REGEX_TEMPLATE_MAVEN_ROSE_MONTHS = string.Template("${DATA_PATH}/\\d{4}/\\d{2}")
REGEX_TEMPLATE_MAVEN_ROSE_MONTH_GROUP = string.Template("${DATA_PATH}/\\d{4}/(\\d{2})")
REGEX_TEMPLATE_MAVEN_ROSE_DATA = string.Template(
    "${DATA_PATH}/\\d{4}/\\d{2}/\\w+_\\d{8}T\\d{6}_\\w+"
)
REGEX_TEMPLATE_MAVEN_ROSE_DATA_GROUP = string.Template(
    "${DATA_PATH}/\\d{4}/\\d{2}/\\w+_(\\d{8}T\\d{6})_\\w+"
)
MAVEN_RADIO_DATA_RGX = dict(l0=r"\w+_rsr_\w+.dat", l2=r"\w+_sky_\w+.tab")
MAVEN_RADIO_DATA_RGX_TIME_GROUP = dict(
    l0=r"\w+_rsr_(\d{8}T\d{6})_\w+.dat", l2=r"\w+_sky_(\d{8}T\d{6})_\w+.tab"
)

DTPOOL_METHOD = "KERNELS_TO_LOAD"

TIMEOUT = 10.0
START_INDEX = 0
DIRNAME_PATTERN_SLICE = slice(0, -1)


def parse_maven_meta_kernel_name(META_KERNEL_NAME: str) -> Optional[Tuple[int, int]]:
    """Find MAVEN meta kernel year and name from its name."""
    RGX = re.search(MAVEN_MK_RGX_GROUP, META_KERNEL_NAME)
    if RGX is not None:
        (YEAR, VERSION) = RGX.groups()
        return (int(YEAR), int(VERSION))
    return None


def fetch_file(URL: Url, PATH: Path, DESCRIPTION: str = "") -> bool:
    """Fetch file online at URL and place it at PATH."""
    # Only download if the file does not exist locally.
    FILE_EXISTS = PATH.is_file()
    if not FILE_EXISTS:
        RESPONSE = requests.get(URL, stream=True, allow_redirects=True, timeout=TIMEOUT)

        # Raise for 4xx codes.
        if RESPONSE.status_code != 200:
            RESPONSE.raise_for_status()
            raise_error(
                MESSAGE=f"Request to {URL} returned status code {RESPONSE.status_code}",
                ERROR=RuntimeError,
            )

        # Create parents dir if not existing already.
        PATH.parent.mkdir(parents=True, exist_ok=True)

        # Loading bar customisation.
        FILE_SIZE = int(RESPONSE.headers.get("content-length", 0))
        DESC_UNKNOWN_SIZE = " (Unknown total file size)" if FILE_SIZE == 0 else ""
        DESC = f"{DESCRIPTION} {DESC_UNKNOWN_SIZE}"

        # Decompress if needed.
        RESPONSE.raw.read = functools.partial(RESPONSE.raw.read, decode_content=True)

        # Download to temporary path to ensure file has been downloaded entirely.
        TEMPORARY_PATH = (
            radiocc.cfg.to_process / radiocc.TEMPORARY_DOWNLOAD_DIRECTORY / PATH.name
        )
        TEMPORARY_PATH.parent.mkdir(parents=True, exist_ok=True)

        # In case wanna change bar format.
        # bar_format = (
        #     "{desc}: {percentage:3.0f}%|"
        #     "{bar:20}"
        #     "| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
        # )

        # Save to file.
        with tqdm.wrapattr(
            RESPONSE.raw,
            "read",
            total=FILE_SIZE,
            desc=DESC,
            # bar_format=bar_format,
        ) as R_RAW:
            with TEMPORARY_PATH.open("wb") as F:
                shutil.copyfileobj(R_RAW, F)

        # Once downloaded, move temporary path to final path.
        TEMPORARY_PATH.rename(PATH)

    return FILE_EXISTS


def find_kernels_to_load(PATH: Path) -> List[str]:
    """Find the list of kernels to load from a meta kernel."""
    # Load variables contained in the meta kernels into the kernel pool.
    # Thus, we can access the list of kernels to load.
    spice.ldpool(str(PATH))

    # Get the number of kernels to load.
    (NUMBER_KERNELS, _) = spice.dtpool(DTPOOL_METHOD)

    # Fetch the complete list of kernels to load.
    KERNELS = spice.gcpool(DTPOOL_METHOD, START_INDEX, NUMBER_KERNELS)

    print_validation(f"Found {NUMBER_KERNELS} dependent kernels in the meta kernel.")

    # Apparently mypy considers KERNELS as Any, so make sure it does is a list...
    if type(KERNELS) == list:
        return KERNELS
    else:
        raise NotImplementedError()


def download_kernels(META_KERNEL: str) -> None:
    """Download SPICE kernels."""
    # Clean temporary directory and create it.
    TMP_PATH = radiocc.cfg.to_process / radiocc.TEMPORARY_DOWNLOAD_DIRECTORY
    if TMP_PATH.exists():
        for PATH in TMP_PATH.iterdir():
            PATH.unlink()
    TMP_PATH.mkdir(parents=True, exist_ok=True)

    # The name of the kernels that were not download because already existing locally
    # will be listed here.
    list_already_existing_kernels: List[str] = []

    # URL to download MAVEN SPICE meta kernel.
    URL_SPICE = URLS[radiocc.cfg.mission.name]["SPICE"]

    # Path to save meta kernel.
    SPICE_PATH = radiocc.cfg.to_process / radiocc.SPICE_MAVEN_DIRECTORY

    # Download it.
    PATH_MK = SPICE_PATH / META_KERNEL
    DO_EXIST = fetch_file(URL_SPICE / META_KERNEL, PATH_MK)

    if DO_EXIST:
        list_already_existing_kernels.append(
            str(PATH_MK.relative_to(str(SPICE_PATH.parent)))
        )

    # Get list of kernels to load.
    KERNELS = find_kernels_to_load(PATH_MK)

    # Fetch kernels.
    for INDEX, KERNEL in enumerate(KERNELS):
        KERNEL_URL = Url(string.Template(KERNEL).substitute(KERNELS=URL_SPICE.parent))
        KERNEL_LOCAL = f"{KERNEL_URL.parent.name}/{KERNEL_URL.name}"
        KERNEL_PATH = SPICE_PATH.parent / KERNEL_LOCAL

        DO_EXIST = fetch_file(
            KERNEL_URL, KERNEL_PATH, DESCRIPTION=f"[{INDEX}] {KERNEL_LOCAL}"
        )
        if DO_EXIST:
            list_already_existing_kernels.append(
                str(KERNEL_PATH.relative_to(str(SPICE_PATH.parent)))
            )

    print("\nThese files were already present on your system:")
    print(
        "".join(
            f"+ [{INDEX}] {NAME}\n"
            for (INDEX, NAME) in enumerate(list_already_existing_kernels)
        )
    )


def find_ROSE_data_in_bundle(URL: Url, BUNDLE: str) -> Iterable[str]:

    # Get URL content.
    print(f"Fetching {unquote(str(URL))}...")
    RESPONSE = requests.get(URL, timeout=TIMEOUT)
    SOUP = BeautifulSoup(RESPONSE.text, "html.parser")

    # Complete regex template from bundle.
    REGEX_DATA = REGEX_TEMPLATE_MAVEN_ROSE_DATA.substitute(
        DATA_PATH=MAVEN_ROSE_BUNDLE_DATA_PATHS[BUNDLE]
    )

    # List MAVEN available data.
    return (HREF.get("href") for HREF in SOUP.find_all(href=re.compile(REGEX_DATA)))


def find_ROSE_data(DATE: arrow.Arrow) -> Dict[str, Iterable[str]]:
    """
    Download radio-science data from date.

    The date contains year and month information.
    """
    URLS_DATA = URLS["MAVEN"]["ROSE"]

    return {
        BUNDLE: find_ROSE_data_in_bundle(
            update_ROSE_query_id(
                URL, lambda x: x / str(DATE.year) / f"{DATE.month:02d}"
            ),
            BUNDLE,
        )
        for (BUNDLE, URL) in URLS_DATA.items()
    }


def get_relative_time(LEVEL: str, DATA: str) -> Any:
    """Compute relative time."""

    RGX_GROUPS = re.search(MAVEN_RADIO_DATA_RGX_TIME_GROUP[LEVEL], DATA)

    if RGX_GROUPS is None:
        raise NotImplementedError

    return abs(
        radiocc.cfg.date.total_seconds - arrow.get(RGX_GROUPS.group(1)).total_seconds
    )


def select_radio_data(RADIO_DATA: Dict[str, Iterable[str]]) -> Dict[str, str]:
    """Select which date to consider for the data."""
    RADIO_DATA_SELECTED: Dict[str, str] = dict()

    for (LEVEL, DATA_POSSIBILITIES_ITER) in RADIO_DATA.items():
        DATA_POSSIBILITIES = list(DATA_POSSIBILITIES_ITER)

        # In interactive mode, take the radio science data automatically.
        if not radiocc.cfg.interactive_download:
            # Find delta-time between each date and the date in config file.
            RELATIVE_TIMES = [
                get_relative_time(LEVEL, DATA) for DATA in DATA_POSSIBILITIES
            ]

            # Get the closest date.
            INDEX_CLOSEST = numpy.argmin(RELATIVE_TIMES)
            RADIO_DATA_SELECTED[LEVEL] = DATA_POSSIBILITIES[INDEX_CLOSEST]

        # Otherwise, ask the user which radio data to pick.
        else:
            DATA_CHOICE = form_choice(
                "\nWhich radio science data to pick?", DATA_POSSIBILITIES
            )
            RADIO_DATA_SELECTED[LEVEL] = DATA_POSSIBILITIES[DATA_CHOICE]

    return RADIO_DATA_SELECTED


def get_csv_url_from_ROSE_data_query(QUERY: str) -> Tuple[str, Url]:
    QUERIES = Url(QUERY).form
    QUERY_DATA = QUERIES["id"][0]
    FILE = Url(QUERIES["id"][0]).name
    return FILE, URL_MAVEN_ROSE_ROOT_DOWNLOAD.with_query(id=QUERY_DATA, f="csv")


def download_ROSE(
    DATE: arrow.Arrow,
) -> Tuple[Path, radiocc.model.RadioDataType]:
    """
    Download radio-science data from date.

    The date contains year and month information.
    """
    # Get radio data to download for l0 & l2.
    RADIO_DATA = find_ROSE_data(DATE)
    SELECTED = select_radio_data(RADIO_DATA)

    # Get data type.
    if radiocc.cfg.interactive_download:
        POSSIBILITIES_RADIO_DATA_TYPE = list(radiocc.model.RadioDataType)
        POSSIBILITIES_RADIO_DATA_TYPE_STR = [
            TYPE.value for TYPE in POSSIBILITIES_RADIO_DATA_TYPE
        ]
        RADIO_DATA_TYPE_CHOICE = form_choice(
            "\nIs it egress or ingress data?", POSSIBILITIES_RADIO_DATA_TYPE_STR
        )
        TYPE = POSSIBILITIES_RADIO_DATA_TYPE[RADIO_DATA_TYPE_CHOICE]
    else:
        # Determine radio date type.
        TYPE = radiocc.cfg.radio_data_type

    # Use date of calibrated bundle for folder name.
    REGEX_DATA_GROUP = REGEX_TEMPLATE_MAVEN_ROSE_DATA_GROUP.substitute(
        DATA_PATH=MAVEN_ROSE_BUNDLE_DATA_PATHS["calibrated"]
    )
    RGX_GROUPS = re.search(REGEX_DATA_GROUP, SELECTED["calibrated"])

    if RGX_GROUPS is None:
        raise NotImplementedError
    DATE_L2 = arrow.get(RGX_GROUPS.group(1))

    # Create directory to store them.
    DIRNAME = radiocc.MAVEN_DIRNAME_TEMPLATE.substitute(
        DATE=DATE_L2.format(radiocc.DATE_FMT_FOLDER)
    )
    PATH = radiocc.cfg.to_process / DIRNAME

    # Check if directory already exists.
    if PATH.is_dir():
        raise_error(f'Directory "{PATH.resolve()}" already exists.')

    # Download them.
    list_already_downloaded: List[str] = []

    TOTAL = len(SELECTED.keys())

    for (INDEX, (_, QUERY)) in enumerate(SELECTED.items()):
        FILE, URL = get_csv_url_from_ROSE_data_query(QUERY)
        DID_EXIST = fetch_file(
            URL,
            PATH / f"{FILE}.csv",
            DESCRIPTION=f"+ [{INDEX+1}/{TOTAL}] {FILE}",
        )

        if DID_EXIST:
            list_already_downloaded.append(FILE)

    return PATH, TYPE


def find_spice_file_possibilities() -> Dict[int, Dict[int, str]]:
    """
    Find available years for SPICE input data.

    Return hashmap of every versions per year to meta kernels and meta kernels.
    """
    # URL to download MAVEN SPICE meta kernel.
    URL_SPICE = URLS[radiocc.cfg.mission.name]["SPICE"]

    # Get URL content.
    print(f"Fetching {unquote(str(URL_SPICE))}...")
    RESPONSE = requests.get(URL_SPICE, timeout=TIMEOUT)
    SOUP = BeautifulSoup(RESPONSE.text, "html.parser")

    # List MAVEN meta kernels.
    META_KERNELS = (
        HREF.get_text() for HREF in SOUP.find_all(href=re.compile(MAVEN_MK_RGX))
    )

    # Parse the list of meta kernels to have a hashmap of every versions per year.
    META_KERNELS_ATTRS: Dict[int, Dict[int, str]] = dict()
    for MK in META_KERNELS:
        MK_PARSED = parse_maven_meta_kernel_name(MK)

        if MK_PARSED is None:
            continue

        YEAR, VERSION = MK_PARSED

        if YEAR not in META_KERNELS_ATTRS.keys():
            META_KERNELS_ATTRS[YEAR] = dict()

        META_KERNELS_ATTRS[YEAR][VERSION] = MK

    # Check that actually the list of meta kernels is not empty.
    if not META_KERNELS_ATTRS:
        raise_error("Did not find any meta kernel.")

    return META_KERNELS_ATTRS


def find_years_rse() -> List[int]:
    """Find available years for RSE input data."""
    URLS_BUNDLES = URLS["MAVEN"]["ROSE"]
    YEARS = []
    for (BUNDLE, URL) in URLS_BUNDLES.items():
        # Get URL content.
        print(f"Fetching {unquote(str(URL))}...")
        RESPONSE = requests.get(URL, timeout=TIMEOUT)
        SOUP = BeautifulSoup(RESPONSE.text, "html.parser")

        # Complete regex template from bundle.
        REGEX_YEARS = REGEX_TEMPLATE_MAVEN_ROSE_YEARS.substitute(
            DATA_PATH=MAVEN_ROSE_BUNDLE_DATA_PATHS[BUNDLE]
        )
        REGEX_YEAR_GROUP = REGEX_TEMPLATE_MAVEN_ROSE_YEAR_GROUP.substitute(
            DATA_PATH=MAVEN_ROSE_BUNDLE_DATA_PATHS[BUNDLE]
        )
        # List MAVEN available years.
        YEARS.append(
            [
                int(
                    re.search(  # type: ignore [union-attr]
                        REGEX_YEAR_GROUP, HREF.get("href")
                    ).group(1)
                )
                for HREF in SOUP.find_all(href=re.compile(REGEX_YEARS))
            ]
        )

    # Check that actually the list of years is not empty.
    if not YEARS:
        raise_error("Did not find any year.")

    # Find the intersection between the years of the different MAVEN ROSE data.
    return list(
        set(YEARS.pop()).intersection(*map(set, YEARS))  # type: ignore [arg-type]
    )


def find_months_rse(YEAR: int) -> List[int]:
    """Find available months for RSE input data at specific year."""
    URLS_BUNDLES = URLS["MAVEN"]["ROSE"]
    MONTHS = []
    for (BUNDLE, URL) in URLS_BUNDLES.items():
        # Get URL content.
        URL_YEAR = update_ROSE_query_id(URL, lambda x: x / str(YEAR))
        print(f"Fetching {unquote(str(URL_YEAR))}...")
        RESPONSE = requests.get(URL_YEAR, timeout=TIMEOUT)
        SOUP = BeautifulSoup(RESPONSE.text, "html.parser")

        # Complete regex template from bundle.
        REGEX_MONTHS = REGEX_TEMPLATE_MAVEN_ROSE_MONTHS.substitute(
            DATA_PATH=MAVEN_ROSE_BUNDLE_DATA_PATHS[BUNDLE]
        )
        REGEX_MONTH_GROUP = REGEX_TEMPLATE_MAVEN_ROSE_MONTH_GROUP.substitute(
            DATA_PATH=MAVEN_ROSE_BUNDLE_DATA_PATHS[BUNDLE]
        )

        # List MAVEN available data per month
        MONTHS.append(
            [
                int(
                    re.search(  # type: ignore [union-attr]
                        REGEX_MONTH_GROUP, HREF.get("href")
                    ).group(1)
                )
                for HREF in SOUP.find_all(href=re.compile(REGEX_MONTHS))
            ]
        )

    # Check that actually the list of years is not empty.
    if not MONTHS:
        raise_error("Did not find any month from the selected year.")

    # Find the intersection between the month possibilities.
    return list(
        set(MONTHS.pop()).intersection(*map(set, MONTHS))  # type: ignore [arg-type]
    )


def select_year(YEARS: List[int]) -> int:
    """Select which date to consider for the data."""
    # In interactive mode, take the year from configured date.
    if not radiocc.cfg.interactive_download:
        if radiocc.cfg.date.year in YEARS:
            YEAR = radiocc.cfg.date.year
        else:
            YEARS_STR = "".join(f"+ {YEAR}\n" for YEAR in YEARS)
            raise_error(
                "The year of the configured date does not match available data.\n"
                f"Asked: {radiocc.cfg.date}\n"
                f"Available: \n{YEARS_STR}"
            )
    # Otherwise, ask the user which year to pick.
    else:
        YEAR_CHOICE = form_choice("\nWhich year to pick?", YEARS)
        YEAR = YEARS[YEAR_CHOICE]

    return YEAR


def select_month(MONTHS: List[int]) -> int:
    """Select which date to consider for the data."""

    # In interactive mode, take the month from configured date.
    if not radiocc.cfg.interactive_download:
        if radiocc.cfg.date.month in MONTHS:
            MONTH = radiocc.cfg.date.month
        else:
            MONTHS_STR = "".join(f"+ {MONTH}\n" for MONTH in MONTHS)
            raise_error(
                "The month of the configured date does not match available data.\n"
                f"Asked: {radiocc.cfg.date}\n"
                f"Available: \n{MONTHS_STR}"
            )
    # Otherwise, ask the user which year to pick.
    else:
        MONTH_CHOICE = form_choice("Which month to pick?", MONTHS)
        MONTH = MONTHS[MONTH_CHOICE]

    return MONTH


def select_meta_kernel(VERSIONS: Dict[int, str]) -> str:
    """Find a select a kernel version to obtain the meta kernel name."""
    # In interactive mode, take the the version from configuration.
    if not radiocc.cfg.interactive_download:
        if radiocc.cfg.kernel_version == KernelVersion.LATEST:
            VERSION = max(VERSIONS)
        else:
            VERSION = min(VERSIONS)
        KERNEL = VERSIONS[VERSION]
    # Otherwise, ask the user which version to pick.
    else:
        VERSION_CHOICE = form_choice(
            "Which meta kernel version to pick?", VERSIONS.keys()
        )
        VERSION = list(VERSIONS.keys())[VERSION_CHOICE]

        # Get corresponding kernel.
        KERNEL = VERSIONS[VERSION]

    return KERNEL


def select_files_by_date_and_version() -> Tuple[arrow.Arrow, str]:
    """
    Select which files to download regarding the configuration.

    Return an Arrow date containing year and month information, and the meta kernel
    file chosen.
    """
    # Find possible years and versions for SPICE meta kernels.
    META_KERNELS_ATTRS = find_spice_file_possibilities()

    # Find possible years from RSE data.
    YEARS_RSE = find_years_rse()

    # Get intersection of SPICE and RSE year lists and select one.
    COMMON_YEARS = list(set(META_KERNELS_ATTRS.keys()) & set(YEARS_RSE))
    YEAR = select_year(COMMON_YEARS)

    # Find possible months from RSE and select one.
    MONTHS = find_months_rse(YEAR)
    MONTH = select_month(MONTHS)

    # Find a select a kernel version to obtain the meta kernel name.
    MK = select_meta_kernel(META_KERNELS_ATTRS[YEAR])

    DATE = arrow.get(YEAR, MONTH, 1)
    DATE_DISPLAY = "YYYY/MMMM"

    print_validation(
        f"Found meta kernel: {MK}, and RSE data from: {DATE.format(DATE_DISPLAY)}."
    )

    return DATE, MK


def proceed() -> None:
    """Download input data: SPICE kernels & RSE."""
    if radiocc.cfg.mission == ProcessType.MEX:
        raise NotImplementedError()

    [DATE, META_KERNEL] = select_files_by_date_and_version()

    download_kernels(META_KERNEL)
    PATH, TYPE = download_ROSE(DATE)

    # Create to_process descriptor.
    descriptor = (
        radiocc.process_descriptor.DescriptorBuilder()
        .meta_kernel(META_KERNEL)
        .radio_data_type(TYPE)
        .build()
    )

    # Save config in directory.
    with (PATH / radiocc.process_descriptor.DESCRIPTOR_FILE_NAME).open("w") as F:
        yaml.dump(descriptor.to_dict(), F)
