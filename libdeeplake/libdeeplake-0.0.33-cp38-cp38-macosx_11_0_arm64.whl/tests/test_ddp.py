from indra import api
from indra.pytorch.loader import Loader
from indra.pytorch.helper_fns import transform_fn
import os
import torch.distributed as dist
import torch.multiprocessing as mp


def setup(rank, world_size):
    os.environ["MASTER_ADDR"] = "localhost"
    os.environ["MASTER_PORT"] = "12355"
    dist.init_process_group("gloo", rank=rank, world_size=world_size)


def cleanup():
    dist.destroy_process_group()


def iterate_loader(rank, world_size):
    setup(rank, world_size)
    ds = api.dataset("s3://hub-2.0-datasets/cars/")
    ds.checkout("")
    dsv = ds[0:100]
    dl = Loader(
        dsv,
        batch_size=2,
        shuffle=False,
        transform_fn=transform_fn,
        num_workers=4,
        distributed=True,
    )

    for i, item in enumerate(dl):
        if i % 10 == 0:
            print(f"rank {rank}, batch {i}")

    cleanup()


if __name__ == "__main__":
    world_size = 3
    mp.spawn(iterate_loader, args=(world_size,), nprocs=world_size)
