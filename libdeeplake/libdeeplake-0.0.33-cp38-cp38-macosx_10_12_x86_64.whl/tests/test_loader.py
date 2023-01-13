from indra import api
from indra.pytorch.loader import Loader
from .constants import MNIST_DS_NAME, CIFAR10_DS_NAME, IMAGENET_DS_NAME
import torch
import deeplake
import numpy as np
from indra.pytorch.helper_fns import transform_fn
from torchvision import transforms
from tqdm import tqdm
import pytest
from .utils import tmp_datasets_dir
from .constants import COCO_DS_NAME

CORRUPTED_DS_NAME = "collision"

TFORM = transforms.Compose(
    [
        transforms.ToPILImage(),  # Must convert to PIL image for subsequent operations to run
        transforms.RandomRotation(20),  # Image augmentation
        transforms.ToTensor(),  # Must convert to pytorch tensor for subsequent operations to run
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
    ]
)


def _cpp_transform(sample):
    sample["images"] = TFORM(sample["images"])
    return sample


@pytest.mark.outdated
def test_on_with_s3_path_loader():
    cpp_ds = api.dataset("s3://hub-2.0-datasets-n/cars/")[0:100]
    hub_ds = deeplake.load("s3://hub-2.0-datasets-n/cars/")[0:100]

    for i in range(100):
        np.testing.assert_array_equal(hub_ds.images[i].numpy(), cpp_ds.tensors[0][i])


@pytest.mark.outdated
def test_mnist_batch_equality():
    cpp_ds = api.dataset(MNIST_DS_NAME)[0:100]
    hub_ds = deeplake.load(MNIST_DS_NAME)[0:100]

    def transform_fn(item):
        return item

    cpp_iter = iter(
        Loader(
            cpp_ds,
            batch_size=1,
            transform_fn=transform_fn,
            num_threads=1,
        )
    )

    hub_iter = iter(hub_ds.pytorch(transform=transform_fn, batch_size=1))

    for _ in range(10):
        a = next(cpp_iter)
        b = next(hub_iter)
        torch.equal(a["images"], b["images"])
        torch.equal(a["labels"], b["labels"])


@pytest.mark.outdated
def test_cifar10_batch_equality():
    cpp_ds = api.dataset(CIFAR10_DS_NAME)[0:100]
    hub_ds = deeplake.load(CIFAR10_DS_NAME)[0:100]

    cpp_iter = iter(
        Loader(
            cpp_ds,
            batch_size=1,
            transform_fn=_cpp_transform,
            num_threads=1,
            tensors=[],
        )
    )

    hub_iter = iter(
        hub_ds.pytorch(transform={"images": TFORM, "labels": None}, batch_size=1)
    )

    for i in range(10):
        torch.equal(next(cpp_iter)["images"], next(hub_iter)["images"])


@pytest.mark.outdated
def test_cifar10_batch_with_multiple_workersequality():
    cpp_ds = api.dataset(CIFAR10_DS_NAME)[0:100]
    hub_ds = deeplake.load(CIFAR10_DS_NAME)[0:100]

    cpp_iter = iter(
        Loader(
            cpp_ds,
            batch_size=1,
            transform_fn=_cpp_transform,
            num_threads=2,
            tensors=[],
        )
    )

    hub_iter = iter(
        hub_ds.pytorch(
            num_workers=2, transform={"images": TFORM, "labels": None}, batch_size=1
        )
    )

    for i in range(10):
        torch.equal(next(cpp_iter)["images"], next(hub_iter)["images"])


@pytest.mark.outdated
def test_data_loader_tensor_extraction():
    ds = api.dataset(MNIST_DS_NAME)[0:10]

    def collate_fn(batch):
        return batch

    try:
        ld = ds.loader(tensors=["aa"])
    except KeyError:
        pass

    it = iter(ds.loader(tensors=["images"], batch_size=1))

    for item in it:
        assert len(item[0].keys()) == 1
        assert item[0].get("images", None) is not None


@pytest.mark.outdated
def test_data_loader_drop_last():
    ds = api.dataset(MNIST_DS_NAME)[0:10]

    ld1 = ds.loader(drop_last=True, batch_size=3)
    assert len(ld1) == 3

    ld2 = ds.loader(drop_last=False, batch_size=3)
    assert len(ld2) == 4


def test_loader_iteration_with_repeated_samples():
    slice_ = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] * 100
    ds = api.dataset(MNIST_DS_NAME)[slice_]

    ld = ds.loader(batch_size=4)

    for _, _ in enumerate(ld):
        pass


def create_corrupted_collision(tmp_datasets_dir):
    ds = deeplake.dataset(tmp_datasets_dir / CORRUPTED_DS_NAME, overwrite=True)
    with ds:
        ds.create_tensor("abc")
        for _ in range(2):
            for i in range(1, 7):
                ds.abc.append(i * np.ones((100 * i, 100 * i)))

        # has 2 chunks, one with 8 samples, one with 4 samples
        enc = ds.abc.chunk_engine.chunk_id_encoder

        # now encoder is pointing to chunk with 4 samples even for first entry, so it will try to read samples, but will fail as chunk only has 4
        enc.array[0][0] = enc.array[1][0]
        enc.is_dirty = True


def test_corrupted_ds_iteration(tmp_datasets_dir):
    create_corrupted_collision(tmp_datasets_dir=tmp_datasets_dir)

    dl = Loader(
        api.dataset(str(tmp_datasets_dir / CORRUPTED_DS_NAME)),
        num_workers=0,
        num_threads=6,
        batch_size=2,
    )

    try:
        for batch in dl:
            pass
    except:
        pass


@pytest.mark.outdated
def test_crash_on_multiple_epochs():
    dl = Loader(
        api.dataset("hub://activeloop/cifar10-train"),
        num_workers=0,
        num_threads=6,
        batch_size=8,
        transform_fn=None,
        tensors=["images"],
    )
    for epoch in range(24):
        for batch in tqdm(dl):
            pass


@pytest.mark.outdated
def test_loader_return_index():
    indices = [0, 10, 100, 11, 43, 98, 40, 400, 30, 50]
    ds = api.dataset(MNIST_DS_NAME)[indices]

    dl = Loader(ds, return_index=True, batch_size=1)
    for idx, item in zip(indices, dl):
        assert np.array([idx], dtype=np.int64) == item["index"][0].numpy()

    dl = Loader(ds, return_index=False, batch_size=1)
    with pytest.raises(KeyError):
        for idx, item in zip(indices, dl):
            assert np.array([idx], dtype=np.int64) == item["index"][0].numpy()


@pytest.mark.parametrize(
    "ds_name, slice",
    [
        (MNIST_DS_NAME, None),
        (CIFAR10_DS_NAME, None),
        (IMAGENET_DS_NAME, slice(0, 1000)),
    ],
)
@pytest.mark.performance
def test_simple_loader(benchmark, ds_name, slice):
    @benchmark
    def ds_loader():
        ds = api.dataset(ds_name)
        if not slice is None:
            ds = ds[slice]
        l = ds.loader(shuffle=False, drop_last=True, batch_size=64)
        for b in iter(l):
            assert len(b) == 64


@pytest.mark.performance
def test_simple_loader_for_coco_(benchmark):
    @benchmark
    def ds_loader():
        for i in range(0, 4):
            ds = api.dataset(COCO_DS_NAME)
            l = ds.loader(shuffle=False, drop_last=True, batch_size=64)
            for b in iter(l):
                pass


@pytest.mark.parametrize(
    "batch_size, num_threads",
    [
        (64, 2),
        (64, 4),
        (512, 2),
        (512, 4),
    ],
)
@pytest.mark.performance
def test_imagenet_1k_batch_vs_threads(benchmark, batch_size, num_threads):
    @benchmark
    def ds_loader():
        api.set_num_threads(num_threads)
        ds = api.dataset(IMAGENET_DS_NAME)
        ds = ds[0:1000]
        l = ds.loader(
            shuffle=False,
            drop_last=True,
            batch_size=batch_size,
            num_threads=num_threads,
        )
        for b in iter(l):
            assert len(b) == batch_size
