import json
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from cinnaroll_internal.model_upload import prepare_artifact, upload_artifact, MEGABYTE
from cinnaroll_internal.io_formats import IMG
from tests.unit.utils import generate_random_string


# Since this is meant to be run manually on a freshly generated s3_upload_url,
# it is not included in the standard test suite
def main(size_in_mb: float, line_length: int = 80, utf_encoding: int = 16) -> None:
    num_lines = round(size_in_mb * MEGABYTE / (utf_encoding / 8 * line_length))

    infer_func_source_code = generate_random_string(num_lines, line_length)
    infer_global_vars: Dict[str, Any] = {}
    requirements: List[str] = []
    model_input_sample = np.random.rand(1000, 1000)
    infer_func_input_sample = str(
        Path(__file__).parent / "test_data" / "cifar-example.jpg"
    )
    infer_func_input_format = IMG

    cache_dir = Path(__file__).parent / "tmp"
    artifact_path = cache_dir / "artifact.tar.gz"
    model_path = cache_dir / "saved_model"

    prepare_artifact(
        artifact_path,
        model_path,
        infer_func_source_code,
        infer_global_vars,
        requirements,
        model_input_sample,
        infer_func_input_sample,
        infer_func_input_format,
    )
    print(f"Artifact size: {artifact_path.stat().st_size / MEGABYTE :.1f} MB")

    with open("s3_upload_url.json", "r") as f:
        s3_upload_url = json.load(f)

    res = upload_artifact(artifact_path, s3_upload_url)
    print(res)


if __name__ == "__main__":
    main(10)
