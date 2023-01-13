import deeplake
from indra import api
import numpy as np
import pytest
from indra import api
from .utils import tmp_datasets_dir

def test_png_chunk_bug(tmp_datasets_dir):
    ds = deeplake.dataset(tmp_datasets_dir / "png_chunk_issue", overwrite=True)
    ds.create_tensor("image", htype="image", chunk_compression="png")
    ds.image.append(np.random.randint(0, 255, (200, 200, 4), np.uint8))
    ids = api.dataset(str(tmp_datasets_dir / "png_chunk_issue"))
    assert np.all(ids.tensors[0][0] == ds.image[0].numpy())

def test_tiled_bmask_bug():
    coco_train = api.dataset("hub://activeloop/coco-train")
    assert coco_train.tensors[2].name == "masks"
    _ = coco_train.tensors[2][34866]

def test_non_string_commit_message(tmp_datasets_dir):
    ds = deeplake.dataset(tmp_datasets_dir / "non_string_commit", overwrite=True)
    with ds:
        ds.create_tensor("labels", htype="class_label")
        ds.labels.append(1)
        ds.commit(["array commit message"])
        ds.labels.append(2)
    ids = api.dataset(str(tmp_datasets_dir / "non_string_commit"))
    assert len(ids) == 2
    ids.checkout("firstdbf9474d461a19e9333c2fd19b46115348f")
    assert len(ids) == 1
    ids.checkout(ds.pending_commit_id)
    assert len(ids) == 2