import webdataset as wds

from ..clients import AssetManagerClient
from ..custom_exceptions import ResponseError


def _identity_transform(x):
    return x

class StreamableSet:
    def __init__(self,
                 set_id: str,
                 sec_requests,
                 sec_wait_for_completion_func,
                 sets_amc: AssetManagerClient,
                 zipfiles_amc: AssetManagerClient,
                 force_recreate: bool = False,
                 shard_size: int = 50000):

        self.set_id = set_id
        self.sec_requests = sec_requests
        self.sec_wait_for_completion_func = sec_wait_for_completion_func
        self.sets_amc = sets_amc
        self.zipfiles_amc = zipfiles_amc
        self._prepare_shards(force_recreate=force_recreate, shard_size=shard_size)

    def _prepare_shards(self, force_recreate=False, shard_size=50000):
        params = {"force_recreate": force_recreate,
                  "shard_size": shard_size}

        resp = self.sec_requests.post(
            "sets/{}/streamable_shards/".format(self.set_id),
            params=params,
            trailing_slash=True)

        if not resp.ok:
            raise ResponseError(
                "Could not start the operation: {}".format(
                    resp.content))

        job_id = resp.json().get("job_id")
        if job_id:
            # Shards already exist
            self.sec_wait_for_completion_func(job_id)

    def pytorch_dataloader(self,
                           asset_transform=_identity_transform,
                           metadata_transform=_identity_transform,
                           annotation_transform=_identity_transform,
                           shuffle: bool = False,
                           num_workers: int = 1,
                           batch_size: int = 1,
                           shuffle_buffer: int = 1000):
        import torch

        sets_metadata = self.sets_amc.get_metadata(self.set_id)
        tarfile_ids = sets_metadata.get("streamable_shards")
        tarfile_urls = self.zipfiles_amc.get_url_in_batch(ids=tarfile_ids)
        num_assets_in_dataset = tarfile_ids[0].split("_shard")[0].split(self.set_id)[-1].split("_")[1]

        dataset = wds.WebDataset(list(tarfile_urls.values()),
                                 handler=wds.handlers.warn_and_continue).decode("pil")
        if shuffle:
            dataset.shuffle(shuffle_buffer)

        # Explicit batching in the dataset
        dataset = dataset.to_tuple("input.jpg;input.jpeg;input.png;input.tiff;",
                                   "metadata.json",
                                   "annotations.json")

        dataset.map_tuple(asset_transform, metadata_transform, annotation_transform)
        dataset = dataset.batched(batch_size)
        dataset = dataset.with_length(num_assets_in_dataset)

        # dataset = dataset.batched(batch_size)
        dataloader = torch.utils.data.DataLoader(dataset,
                                                 batch_size=None,
                                                 num_workers=num_workers)

        return dataloader