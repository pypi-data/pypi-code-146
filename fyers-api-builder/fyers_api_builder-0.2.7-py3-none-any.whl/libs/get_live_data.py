import threading
from datetime import datetime, timedelta

from fyers_api_builder.libs.generate_payload import generate_payload


class GetLiveData:
    data_available_from = datetime.fromisoformat("2017-05-01")
    today = datetime.today()
    yesterday = today - timedelta(days=1)

    def __init__(
        self, client, symbol, fetch_from_epoch, fetch_to_epoch, resolution, interval
    ):
        self.client = client
        self.symbol = symbol
        self.fetch_from_epoch = fetch_from_epoch
        self.fetch_to_epoch = fetch_to_epoch
        self.resolution = resolution
        self.interval = interval
        self.results = []

    def get_data(self):
        payload = generate_payload(
            self.symbol, self.resolution, self.fetch_from_date, self.fetch_to_date
        )

        while True:
            data = self.fetch_data_from_broker(payload)

            items = data["candles"]

            last_item_timestamp = items[-1][0]

            if last_item_timestamp >= self.fetch_to_epoch:
                for item in items:
                    if item[0] <= self.fetch_to_epoch:
                        self.results.append(item)
                break
            else:
                continue

    def run_filters(self):
        if self.fetch_from_epoch < int(self.data_available_from.timestamp()):
            raise Exception(
                "Data only available from %s"
                % self.data_available_from.strftime("%Y-%m-%d")
            )

        if self.fetch_to_epoch > int(self.yesterday.timestamp()):
            raise Exception(
                "History Data only available upto %s"
                % self.yesterday.strftime("%Y-%m-%d")
            )

    def run(self):
        self.run_filters()

        download_thread = threading.Thread(
            target=self.get_data,
            args=(self.fetch_from_epoch, self.fetch_to_epoch),
        )

        download_thread.start()
        download_thread.join()

        return self.results
