import logging
from pathlib import Path

import requests
import typer
import xlsxwriter

ENDPOINT = "https://api.elsevier.com/content/search/scopus"
DEFAULT_OUTPUT_FILENAME = "scopus.xlsx"
MAX_NUMBER_OF_RESULTS_PER_REQUEST = 25


def scopus_search(
        query: str = typer.Argument(..., help="A query as described in https://dev.elsevier.com/sc_search_tips.html\n"
                                              "For example, 'TITLE(magic sets)'"),
        api_key: str = typer.Option(..., "--api-key", "-k", envvar="SCOPUS_API_KEY",
                                    help="Your Scopus API key from https://dev.elsevier.com/"),
        number_of_results: int = typer.Option(MAX_NUMBER_OF_RESULTS_PER_REQUEST, "--number-of-results", "-n",
                                              help="The number of wanted results"),
        output_filename: Path = typer.Option(DEFAULT_OUTPUT_FILENAME, "--output-filename", "-o",
                                             help="The path to the output file to be produced (must be writable)"),
        with_log: bool = typer.Option(False, "--with-log", "-l", help="Print logging information"),
) -> None:
    if with_log:
        logging.getLogger().setLevel(logging.INFO)
    logging.info(f"Starting SCOPUS search for query {query} (up to {number_of_results} results)")
    keys = set()
    entries = []
    while len(entries) < number_of_results:
        logging.info(f"Results so far: {len(entries)}")
        res = requests.get(ENDPOINT, params={
            "query": query,
            "apiKey": api_key,
            "start": len(entries),
            "count": MAX_NUMBER_OF_RESULTS_PER_REQUEST,
        })
        if res.status_code != 200:
            print(f"Unexpected status code: {res.status_code}")
            break

        data = res.json()['search-results']
        if 'entry' not in data:
            logging.info(f"No results in the last query. All results already retrieved.")
            break

        data = data['entry']
        for index, entry in enumerate(data):
            keys.update(entry.keys())
            entries.append(entry)
        logging.info(f"Added {len(data)} results")

        if len(data) < MAX_NUMBER_OF_RESULTS_PER_REQUEST:
            logging.info(f"There was space for more results, but have not been found. All results already retrieved.")
            break

    keys = list(sorted(keys))
    logging.info(f"Writing {len(entries)} results to {output_filename}")
    rows = [[str(key) for key in keys]]
    for entry in entries:
        rows.append([str(entry[key]) if key in entry.keys() else None for key in keys])

    with xlsxwriter.Workbook(output_filename) as workbook:
        worksheet = workbook.add_worksheet()
        for index, row in enumerate(rows):
            worksheet.write_row(index, 0, row)
