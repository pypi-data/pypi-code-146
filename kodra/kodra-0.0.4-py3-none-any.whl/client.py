import random
from typing import Optional, Tuple

import pandas
import requests
from requests_toolbelt.multipart import encoder
from tqdm import tqdm

"""
This library can be used to interact with the Kodra web application for a
limited set of workflows. Users need to provide valid authentication tokens
in order to successfully communicate with Kodra. The primary workflow that is
supported for now is uploading Pandas Dataframe objects to an existing Kodra
project.

Usage:

import pandas
from kodra import Kodra

df = pandas.DataFrame({'name': ['John Smith', 'Alice', 'Bob'],
                       'department': ['engineering', 'finance', 'marketing'],
                       'tenure (years)': ['2', '5', '10']})
Kodra().share(
    data=df,
    token="<valid_token>",
    name="<optional_name>"
)

In the above interaction, the user will need to provide a valid upload token obtained
from the Kodra app. The `name` field correspondonds to the dataset name. If the user
does not provide a name, a default one will be created and assigned by Kodra.

"""


def share(
    data: pandas.DataFrame, token: str, name: Optional[str] = None
) -> Tuple[int, str]:
    """Top level method to upload a DataFrame to Kodra with default Client.

    This instantiates a default Client() object and allows the user to upload
    a pandas DataFrame to Kodra with a valid upload token. The core functionality
    is handled by the Client's share() method (see below).

    Usage:
        import kodra
        kodra.share(data=my_dataframe, token=<my_token>, name="Awesome Dataset")

    Args:
        data: The Pandas DataFrame object
        token: Unique Upload Token obtained from Kodra
        name: The name of this dataset (optional)

    Returns:
        A Tuple containing the HTTP status code of the upload request along
        with an error string if any are returned. Examples:
            (200, "")
            (400, "Not Authorized")
    """
    client = Client(base_url="https://kodra.ai")
    return client.share(data=data, token=token, name=name)


class Client:
    """A simple client that interacts with the Kodra backend over HTTP."""

    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        # Used to generate default dataset names for uploads
        self.dataset_name_format = "dataset_{}"
        # TODO: This should be changed for prod.
        self.kodra_url = base_url

    def share(
        self, data: pandas.DataFrame, token: str, name: Optional[str] = None
    ) -> Tuple[int, str]:
        """Upload a Pandas Dataframe object to Kodra as a CSV file.

        Args:
            data: A Pandas DataFrame object containing the data to be uploaded.
            token: The unique Upload Token obtained from the Kodra App
            name: Name for the new dataset.

        Returns:
            A Tuple containing the HTTP status code along with an error string
            if any are returned. Examples:
            (200, "")
            (400, "Not Authorized")

        Raises:
            AssertionError: If the provided data is not a Pandas Dataframe
            ValueError: If the provided data is empty or if the token is empty
        """
        assert isinstance(
            data, pandas.DataFrame
        ), "Provided data is not a Pandas DataFrame"
        if data.empty:
            raise ValueError("Provided DataFrame is empty")
        if not token:
            raise ValueError("Upload token is empty")
        dataset_name = (
            name if name else self.dataset_name_format.format((random.randint(0, 1000)))
        )
        # Convert the DataFrame to CSV for uploading. We are setting index = False
        # since we don't want the dataframe's index column to be included in the CSV.
        csv_data = data.to_csv(index=False)
        multipart_encoder = encoder.MultipartEncoder(
            fields={"file": (dataset_name, csv_data)}
        )
        with tqdm(
            desc=dataset_name,
            total=multipart_encoder.len,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            # Used to display a progress bar for the streaming data upload
            encoder_monitor = encoder.MultipartEncoderMonitor(
                multipart_encoder,
                lambda monitor: progress_bar.update(
                    monitor.bytes_read - progress_bar.n
                ),
            )
            resp = requests.post(
                self.kodra_url.format("api/share/"),
                data=encoder_monitor,
                headers={
                    "Upload-Token": token,
                    "Content-Type": multipart_encoder.content_type,
                },
            )
        return (resp.status_code, resp.reason)
