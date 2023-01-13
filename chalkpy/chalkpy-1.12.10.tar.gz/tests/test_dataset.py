import pytest

from chalk.client.dataset import DatasetVersion, load_dataset
from chalk.features import features


@pytest.mark.skip("not implemented fully")
def test_load_dataset():
    @features
    class CRUser:
        id: int
        favorite_color: str
        favorite_number: int

    data = load_dataset(
        uris=["gs://compute-resolver-results/1673236985507958784_b8e031b8-d7a1-4dc9-beef-b5837889a2d9.parquet"],
        version=DatasetVersion.COMPUTE_RESOLVER_OUTPUT_V1,
    )

    print(data)
    assert data == 1
