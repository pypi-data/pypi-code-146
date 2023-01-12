import logging
import pickle
import os
import argparse
import multiprocessing as mp

import numpy as np
import pandas as pd
from tqdm.auto import tqdm

import capon
from capon.datasets.common import get_resource_path
from capon import datasets
from capon import backends


# logging.getLogger("capon").setLevel(logging.INFO)

exchange_name = "nasdaq"
# exchange_name = "otc"


def load_config(path, create=False, nasdaq=True, otc=False):
    if create:
        indexes_symbols = datasets.load_stock_indexes()["symbol"].tolist()
        exchanges = {
            "indexes": indexes_symbols,
        }

        if nasdaq:
            metadata = datasets.load_metadata()
            screener_metadata = backends.nasdaq.screener()
            print(f"{len(screener_metadata):,} stocks were screened.")

            nasdaq_symbols = np.unique(screener_metadata["symbol"]).tolist()
            print(f"{len(nasdaq_symbols):,} stocks tickers.")
            # nasdaq_symbols = list(
            #     set.union(set(metadata["symbol"]), set(screener_metadata["symbol"]))
            # )

            if not True:  # Enrich with SP-500
                sp500_history = pd.read_csv(
                    "/Users/eyalgal/Library/CloudStorage/Dropbox/Work/fusion/code/fpai/markets/resources/sp500_component_history.2022-10-12.csv",
                    index_col="date",
                )
                # nasdaq_symbols = sorted(
                #     np.unique(nasdaq_symbols + sp500_history.columns.tolist())
                # )
                nasdaq_symbols = sorted(
                    pd.DataFrame(
                        {
                            "symbol_raw": np.unique(
                                nasdaq_symbols + sp500_history.columns.tolist()
                            )
                        }
                    )
                    .assign(
                        symbol=lambda df: df["symbol_raw"]
                        .str.replace(".", "-")
                        .str.replace("/", "-")
                        .str.replace("^", "-P")
                        .str.strip()
                    )["symbol"]
                    .unique()
                )

                print(
                    f"{len(nasdaq_symbols):,} stocks tickers after enriching with historical SP500 ({sp500_history.shape[1]:,} tickers)."
                )

            exchanges["nasdaq"] = nasdaq_symbols

        if otc:
            otc_metadata = backends.otcmarkets.screener()
            otc_symbols = list(otc_metadata["symbol"])

            exchanges["otc"] = otc_symbols

        os.makedirs(path, exist_ok=True)

        exchanges_filename = f"{path}/exchange.pickle"
        print(f"Saving {exchanges_filename}..")
        with open(exchanges_filename, "wb") as handle:
            pickle.dump(exchanges, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        exchanges_filename = f"{path}/exchange.pickle"
        print(f"Loading {exchanges_filename}..")
        with open(exchanges_filename, "rb") as handle:
            exchanges = pickle.load(handle)

    print("exchanges:", {k: len(v) for k, v in exchanges.items()})
    return exchanges


def fetch(ticker, range="10y"):
    # ticker = ticker.replace(".", "-").replace("/", "-")
    try:
        # return capon.stock(ticker, range=range, interval="1d")
        # return backends.yahoo.history(
        #     ticker, start_date="1995-01-01", end_date="2025-01-01", interval="1d"
        # )

        start_date, end_date = "1980-01-01", "2025-01-01"
        # start_date, end_date = "1980-01-01", "2022-10-07"

        return capon.stock(
            ticker, start_date=start_date, end_date=end_date, interval="1d"
        )
    except:
        return None


def get_history(required_symbols, path):
    assert len(set(required_symbols)) == len(
        required_symbols
    ), "required_symbols contains duplicated symbols"

    pool = mp.Pool(mp.cpu_count())
    stocks = pd.concat(
        tqdm(pool.imap(fetch, required_symbols), total=len(required_symbols)),
        ignore_index=True,
    )
    pool.close()

    stocks = stocks.dropna(subset=["close", "adjclose"], how="all").assign(
        timestamp=lambda df: pd.to_datetime(df["timestamp"], utc=True).dt.date
    )

    stocks_filename = f"{path}/" + "capon.history.{}.{}-{}.x{:05}.({}).csv.gz".format(
        exchange_name,
        stocks["timestamp"].min().strftime("%y%m%d"),
        stocks["timestamp"].max().strftime("%y%m%d"),
        stocks["symbol"].nunique(),
        pd.Timestamp.now().strftime("%y%m%d.%H%M%S"),
    )

    print(f"Saving {stocks_filename}..")
    stocks.to_csv(stocks_filename, index=False, compression="gzip")

    missing_symbols = set(required_symbols) - set(stocks["symbol"].unique())
    print(f"{len(missing_symbols)} symbols were not found: {missing_symbols}")

    pd.DataFrame({"symbol": required_symbols}).assign(
        downloaded=lambda df: df["symbol"].isin(stocks["symbol"])
    ).to_csv(stocks_filename.replace(".csv.gz", ".LOG.csv"), index=False)


def get_metadata(required_symbols, path):
    pool = mp.Pool(mp.cpu_count())
    metadata = pd.concat(
        tqdm(
            pool.imap(backends.nasdaq.metadata, required_symbols),
            total=len(required_symbols),
        ),
        axis=1,
        ignore_index=True,
    ).T
    pool.close()

    metadata = metadata.drop("module_title", axis=1).dropna(how="all")
    metadata_filename = f'{path}/capon.metadata.{exchange_name}.x{metadata["symbol"].nunique():05}.({pd.Timestamp.now().strftime("%y%m%d.%H%M%S")}).csv.gz'

    print(f"Saving {metadata_filename}..")
    metadata.to_csv(metadata_filename, index=False, compression="gzip")


def get_dividends(required_symbols, path):
    pass


def download(args):
    dataset_id = args.id
    do_create_config = False

    if dataset_id is None:
        dataset_id = pd.Timestamp.now().strftime("%y%m%d.%H%M%S")
        print(f'new dataset_id: "{dataset_id}"')
        do_create_config = True

    # path = get_resource_path(f"../../outputs/capon-data/__raw_{dataset_id}")
    path = os.path.expanduser(
        f"~/Downloads/fp-datasets/capon/capon-data/__raw_{dataset_id}"
    )
    print(f"path: {path}")

    if True:
        print("\nConfiguration..")
        exchanges = load_config(path, create=do_create_config)

    required_symbols = list(np.unique(exchanges[exchange_name] + exchanges["indexes"]))
    if args.debug:
        required_symbols = required_symbols[:20]
    print(f"{len(required_symbols):,} required symbols")

    if True:
        print("\nDownloading history..")
        get_history(required_symbols, path=path)

    if True:
        print("\nDownloading metadata..")
        get_metadata(required_symbols, path=path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--id",
        default=None,
        type=str,
        help="Dataset id. If None, a new will be created.",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Debug mode (for a fast running time)."
    )
    args = parser.parse_args()

    if args.debug:
        print(f"args: {args}")

    download(args)


if False:
    stocks = pd.read_csv(
        "~/Dropbox/PhD/Code/capon/outputs/metadata/raw_220705.101823/capon.history.nasdaq.120702-220704.x07859.(220705.105016).csv.gz"
    )
    metadata = pd.read_csv(
        "~/Dropbox/PhD/Code/capon/outputs/metadata/raw_220705.101823/capon.metadata.nasdaq.x07878.csv.gz"
    )

    set(metadata["symbol"]) - set(stocks["symbol"])
    """
    {'ASCBR',
    ...
    'EAI',
    'ECC           ',
    'ECOM          ',
    'EMP',
    """

    import glob

    last_dataset_folder = sorted(
        glob.glob(get_resource_path(f"../../outputs/capon-data/*"))
    )[-1]
    last_dataset_history = glob.glob(f"{last_dataset_folder}/*.history.*.csv.gz")[0]

    print(f"Loading {last_dataset_history.split('/')[-1]}")
    stocks = pd.read_csv(last_dataset_history)
    stocks["timestamp"].agg(["min", "max"])
    stocks.groupby(["symbol"])["timestamp"].agg(["min", "max", "count"])

if False:
    start_date, end_date = "1980-01-01", "2022-10-07"
    capon.stock("AMZN", start_date=start_date, end_date=end_date, interval="1d")
