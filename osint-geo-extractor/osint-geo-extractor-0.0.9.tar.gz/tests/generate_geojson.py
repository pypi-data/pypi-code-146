import json
import os

from geo_extractor.extractors import (
    BellingcatExtractor,
    CenInfoResExtractor,
    DefmonExtractor,
    DefmonSpreadsheetExtractor,
    GeoConfirmedExtractor,
    # ReukraineExtractor,
    TextyExtractor,
    format_as_geojson,
)

from geo_extractor.constants import RAW_DATA_FILENAMES

TEST_DATA_FOLDER = 'test_data'
TEST_DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    TEST_DATA_FOLDER
)

def load(filename):
    with open(os.path.join(TEST_DATA_PATH, filename), 'r') as f:
        return json.load(f)


defmon_raw = load(RAW_DATA_FILENAMES.DEFMON)

with open(os.path.join(
        TEST_DATA_PATH, RAW_DATA_FILENAMES.DEFMON_CSV
        ), 'r') as f:
    defmon_spreadsheet = f.read()

d = DefmonSpreadsheetExtractor()
events = d.extract_events(defmon_spreadsheet)

events_geojson = format_as_geojson(events)
print(events_geojson)
