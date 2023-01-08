import logging

from azure.cosmos import exceptions

from soccer_sdk_utils.dao.base import DataAccessObject


class ImageDAO(DataAccessObject):
    def __init__(self, **kwargs):
        super().__init__("image", "/id", **kwargs)

    def get_by_url(self, url: str):
        logging.info(f"Fetching image with url {url}")

        try:
            query = f"{self._select_prefix()} i WHERE i.url = '{url}'"
            items = self.container.query_items(
                query=query, enable_cross_partition_query=True
            )

            images = list(items)

            if len(images) == 0:
                return None
            else:
                return images[0]
        except exceptions.CosmosHttpResponseError as err:
            logging.error(err)

            raise err
        except Exception as err:
            logging.error(err)

            raise err
