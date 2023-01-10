import os
import requests
import csv
import json
from typing import Union
from datetime import datetime
from .config import Frequency, AssetType, AssetUrl


APIKEY = os.environ.get("VINTER_API_KEY", None)

class VinterAPI:
    def __init__(self, api_key: str, asset_type: str):
        """This function takes in an api_key and asset_type and sets them as attributes of the class

        Parameters
        ----------
        api_key : str
            Your API key.
        asset_type : str
            The type of asset you want to get data for. This can be one of the following:
            ["multi_assets", "single_assets"]
        """
        self.api_key = api_key
        self.asset_type = asset_type
        self.frequencies = [frequency.value for frequency in Frequency]
        self.valid_asset_types = [asset_type.value for asset_type in AssetType]
        self.valid_symbols = None
        self.validate_asset_type()

    def get_all_active_symbols(self) -> dict:
        """This function returns a dictionary of all the active symbols

        Returns
        -------
            A dictionary of all the active symbols

        """
        url = None
        for asset_url in AssetUrl:
            if (
                asset_url.value["asset_type"].value == self.asset_type
                and asset_url.value["frequency"] is None
            ):
                url = asset_url.value["url"]
                break

        if url is None:
            raise ValueError(
                f"The asset type must be in {self.valid_asset_types}"
            )

        headers = {}
        response = requests.get(url, headers=headers)
        data = response.json()["data"]
        self.valid_symbols = [symbol["symbol"] for symbol in data]
        return data

    def populate_valid_symbols(self) -> None:
        """This function populates the valid_symbols attribute of the class with a list of all the
        active symbols

        Returns
        -------

        """
        self.valid_symbols = [symbol["symbol"] for symbol in self.get_all_active_symbols()]

    def validate_asset_type(self) -> None:
        """If the asset type is not a valid asset_type , then raise a
        ValueError

        """
        if self.asset_type not in self.valid_asset_types:
            raise ValueError(
                f"The asset type must be one of the following : {self.valid_asset_types}"
            )

    def validate_symbol_frequency(self, symbol: str) -> str:
        """This function takes in a symbol and returns the symbol with the frequency appended to it.

        Parameters
        ----------
        symbol : str
            The symbol of the asset you want to get data for.

        Returns
        -------
            The symbol with the frequency appended to it.

        """
        sym_frequency = symbol.split("-")[-1]

        if sym_frequency not in self.frequencies:
            raise ValueError(
                "The frequency must be one of the following valid frequencies: {}".format(
                    self.frequencies
                )
            )

        self.frequency = sym_frequency

        return symbol, sym_frequency

    def get_url_by_asset_type(self, symbol: str) -> str:
        """This function takes in a symbol and returns the url to use to get the data

        Parameters
        ----------
        symbol : str
            The symbol of the asset you want to get data for.

        Returns
        -------
            The url to use to get the data

        """

        symbol, frequency = self.validate_symbol_frequency(symbol)

        url = None
        for asset_url in AssetUrl:
            if (
                asset_url.value["asset_type"].value == self.asset_type
                and asset_url.value["frequency"].value == frequency
            ):
                url = asset_url.value["url"]
                break

        if url is None:
            raise ValueError("The URL could not be found.")

        return url

    def get_latest_data(self, symbol: str, limit: int = 1) -> dict:
        """It takes a symbol and a limit as parameters, and returns a dictionary of the latest data for
        that symbol

        Parameters
        ----------
        symbol : str
            The symbol of the asset you want to get data for.
        limit : int
            The number of data points to return.

        Returns
        -------
            A dictionary of the latest data for the symbol and limit.

        """
        url = self.get_url_by_asset_type(symbol=symbol)

        params = {"symbol": symbol, "limit": limit}
        headers = {"Authorization": self.api_key}
        response = requests.get(url, params=params, headers=headers)

        response.raise_for_status()

        data = response.json()["data"]

        if len(data) == 0:
            if self.valid_symbols is None:
                self.populate_valid_symbols()

            if symbol not in self.valid_symbols:
                raise ValueError(
                    f"The symbol is not a present in the list of active symbols for asset_type {self.asset_type}."
                )
                
            raise ValueError("No data was found for the symbol: {}".format(symbol))

        return data

    def get_latest_value(self, symbol: str) -> float:
        """This function takes in a symbol and returns the latest value for that symbol

        Parameters
        ----------
        symbol : str
            The symbol of the asset you want to get data for.

        Returns
        -------
            The latest value for the symbol

        """
        data = self.get_latest_data(symbol=symbol)
        return data[0]["value"]

    def _get_active_asset_data(self, symbol: str) -> dict:
        """This function returns the data for the active asset

        Parameters
        ----------
        symbol : str
            The symbol of the asset you want to get data for.

        Returns
        -------
            A dictionary of the data for the active asset

        """

        symbol, frequency = self.validate_symbol_frequency(symbol)
        
        data = self.get_all_active_symbols()

        output = {}

        for asset in data:
            if asset["symbol"] == symbol:
                output = asset
                break

        if len(output) == 0:

            if symbol not in self.valid_symbols:
                raise ValueError(
                    f"The symbol is not a present in the list of active symbols for asset_type {self.asset_type}."
                )

            raise ValueError("No data was found for the symbol: {}".format(symbol))

        return output

    def get_current_rebalance_weight(self, symbol: str) -> dict:
        """This function returns the current rebalance weight of multi_assets symbol

        Returns
        -------
            Weight of the current rebalance of the multi_assets symbol
            
            OR
            
            ValueError if the symbol is not a present in the list of active symbols for asset_type multi_assets

        """

        if self.asset_type != AssetType.MULTI_ASSET.value:
            raise ValueError(
                f"The asset type must be {AssetType.MULTI_ASSET.value} to use this function"
            )

        output = ""

        data = self._get_active_asset_data(symbol=symbol)

        if "weights" in data:
            output = data["weights"]

        if output == "" or output is None:
            raise ValueError("No data was found for the symbol: {}".format(symbol))

        return output

    def get_contributions(self, symbol: str) -> dict:
        """This function returns the contributions of the single_assets symbol

        Returns
        -------
            A dictionary of the contributions of the single_assets symbol

            OR

            ValueError if the symbol is not a present in the list of active symbols for asset_type single_assets

        """

        if self.asset_type != AssetType.SINGLE_ASSET.value:
            raise ValueError(
                f"The asset type must be {AssetType.SINGLE_ASSET.value} to use this function"
            )

        output = ""

        data = self._get_active_asset_data(symbol=symbol)

        if "contrib" in data:
            output = data["contrib"]

        if output == "" or output is None:
            raise ValueError(
                f"The symbol {symbol} does not have any contributions associated with it."
            )

        return output

    def get_previous_rebalance_date(self, symbol: str) -> Union[str, None]:
        """This function returns the previous rebalance date of multi_assets symbol

        Returns
        -------
            Date of the previous rebalance of the multi_assets symbol
            
            OR
            
            ValueError if the symbol is not a present in the list of active symbols for asset_type multi_assets
            
            OR
            
            None if the symbol Rebalance is not scheduled

        """

        if self.asset_type != AssetType.MULTI_ASSET.value:
            raise ValueError(
                f"The asset type must be {AssetType.MULTI_ASSET.value} to use this function"
            )

        output = ""

        data = self._get_active_asset_data(symbol=symbol)

        if "previous_rebalance_date" in data:
            output = data["previous_rebalance_date"]

        return output

    def get_previous_review_date(self, symbol: str) -> Union[str, None]:
        """This function returns the previous review date of multi_assets symbol

        Returns
        -------
            Date of the previous review of the multi_assets symbol
            
            OR
            
            ValueError if the symbol is not a present in the list of active symbols for asset_type multi_assets
            
            OR
            
            None if the symbol Review is not scheduled

        """

        if self.asset_type != AssetType.MULTI_ASSET.value:
            raise ValueError(
                f"The asset type must be {AssetType.MULTI_ASSET.value} to use this function"
            )

        output = ""

        data = self._get_active_asset_data(symbol=symbol)

        if "previous_review_date" in data:
            output = data["previous_review_date"]

        return output

    def get_next_review_date(self, symbol: str) -> Union[str, None]:
        """This function returns the next review date of multi_assets symbol

        Returns
        -------
            Date of the next review of the multi_assets symbol
            
            OR
            
            ValueError if the symbol is not a present in the list of active symbols for asset_type multi_assets
            
            OR
            
            None if the symbol Review is not scheduled

        """

        if self.asset_type != AssetType.MULTI_ASSET.value:
            raise ValueError(
                f"The asset type must be {AssetType.MULTI_ASSET.value} to use this function"
            )

        output = ""

        data = self._get_active_asset_data(symbol=symbol)

        if "next_review_date" in data:
            output = data["next_review_date"]

        return output

    def get_next_rebalance_date(self, symbol: str) -> Union[str, None]:
        """This function returns the next rebalance date of multi_assets symbol

        Returns
        -------
            Date of the next rebalance of the multi_assets symbol
            
            OR
            
            ValueError if the symbol is not a present in the list of active symbols for asset_type multi_assets
            
            OR
            
            None if the symbol Rebalance is not scheduled

        """

        if self.asset_type != AssetType.MULTI_ASSET.value:
            raise ValueError(
                f"The asset type must be {AssetType.MULTI_ASSET.value} to use this function"
            )

        output = ""

        data = self._get_active_asset_data(symbol=symbol)

        if "next_rebalance_date" in data:
            output = data["next_rebalance_date"]

        return output

    def get_next_rebalance_weight(self, symbol: str) -> Union[str, None]:
        """This function returns the next rebalance weight of multi_assets symbol

        Returns
        -------
            Weight of the next rebalance of the multi_assets symbol
            
            OR
            
            ValueError if the symbol is not a present in the list of active symbols for asset_type multi_assets
            
            OR
            
            ValueError if the next rebalance date is in the future

            OR

            None if the symbol Rebalance is not scheduled

        """

        if self.asset_type != AssetType.MULTI_ASSET.value:
            raise ValueError(
                f"The asset type must be {AssetType.MULTI_ASSET.value} to use this function"
            )

        output = ""

        data = self._get_active_asset_data(symbol=symbol)

        if "next_rebalance_weights" in data:
            output = data["next_rebalance_weights"]

        if output is None:

            if data["next_rebalance_date"] is None:
                raise ValueError(
                    "The next rebalance date is not scheduled, therefore the next rebalance weight is not available"
                )

            reb_date = datetime.strptime(data["next_rebalance_date"], "%Y-%m-%d")

            if reb_date > datetime.utcnow():
                raise ValueError(
                    "The next rebalance date is in the future, therefore the next rebalance weight is not available"
                )
            else:
                raise ValueError(
                    "The next rebalance weight is not available, please contact support"
                )

        return output


    def get_data_by_date(self, symbol: str, dates: Union[str, list]) -> dict:
        """This function takes in a symbol and a date and returns a dictionary of the data for that date

        This function is only for daily data.
        
        Parameters
        ----------
        symbol : str
            The symbol of the asset you want to get data for.
        date : str | list
            The date of the data you want to get. format: YYYY-MM-DD

        Returns
        -------
            A dictionary of the data

        """
        symbol, frequency = self.validate_symbol_frequency(symbol)

        if frequency != Frequency.DAILY.value:
            raise ValueError("The frequency must be daily to use this function.")

        if isinstance(dates, str):
            dates = [dates]

        # Validate Dates with regex pattern & Date validation
        self.validate_dates(dates)

        output = []
        
        data = self.get_latest_data(symbol=symbol, limit=2000)   

        for date in dates:
            date_data = []
            for candle in data:
                candle_date = candle["created_at"].split("T")[0]
                if candle_date == date:
                    date_data.append(candle)

            if len(date_data) == 0:
                print(
                    "No data was found for the symbol: {} and date: {}".format(
                        symbol, date
                    )
                )

            output.extend(date_data)

        return output

    def validate_dates(self, dates: list) -> None:
        """It raises a ValueError if any of the dates in the dates list are not in the format YYYY-MM-DD

        Parameters
        ----------
        dates
            A list of dates in the format YYYY-MM-DD

        """
        for date in dates:
            # Validate that the date is a valid date
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise ValueError(
                    "The date must be in the format YYYY-MM-DD. The date: {} is not in the correct format.".format(
                        date
                    )
                )

    def save_data_to_file(
        self, data: dict, filename: str, file_type: str = "csv", seprator: str = ","
    ) -> None:
        """This function takes in a dictionary of data and a filename and saves the data to a csv file

        Parameters
        ----------
        data : dict
            A dictionary of data to save to a csv file.
        filename : str
            The name of the file to save the data to.
        file_type : str
            The type of file to save the data to. This can be one of the following:
            ["csv", "json"]
        seprator : str
            The seprator to use when saving the data to the csv file.

        """
        file_type = file_type.lower()
        if file_type not in ["csv", "json"]:

            raise ValueError("The file type must be either csv or json")

        if file_type == "json":
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            return

        elif file_type == "csv":
            with open(filename, "a") as f:
                csv.DictWriter(
                    f, data[0].keys(), delimiter=seprator, lineterminator="\n"
                ).writeheader()  # write the header

                for row in data:
                    # Make Sure dict and list are converted to JSON string
                    for key, value in row.items():
                        if isinstance(value, (dict, list)):
                            row[key] = json.dumps(value)

                    csv.DictWriter(
                        f, row.keys(), delimiter=seprator, lineterminator="\n"
                    ).writerow(row)


if __name__ == "__main__":
    vinter = VinterAPI(APIKEY, "single_assets")

    active_symbols = vinter.get_all_active_symbols()

    get_next_rebalance_date = vinter.get_next_rebalance_date("btc-usd-p-d")

    print(get_next_rebalance_date)

    # data = vinter.get_data_by_date(
    #     "btc-usd-p-d", ["2022-12-04", "2022-12-09", "2022-12-17"]
    # )

    # print(data)

    # all_active_symbol = [asset["symbol"] for asset in vinter.get_all_active_symbols()]

    # selected_symbol = "btc-usd-p-d"


    # # Get the latest value of the asset
    # data = vinter.get_data_by_date(selected_symbol, ["2022-12-04", "2022-12-09"])

    # for asset in data:
    #     print("The price of {} on {} is {}".format(selected_symbol, asset["created_at"], asset["value"]))
