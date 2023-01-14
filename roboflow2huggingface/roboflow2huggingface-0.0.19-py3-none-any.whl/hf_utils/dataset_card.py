from pathlib import Path
import json
from typing import List
from roboflow2huggingface.roboflow_utils import read_roboflow_info


def export_hf_dataset_card(
    dataset_labels: List[str],
    export_dir: str,
    hf_dataset_id: str,
    task="object-detection",
    roboflow_universe_url: str = None,
    split_name_to_num_samples: dict = None,
):
    """
    Exports a dataset card to the specified directory.

    Args:
        dataset_labels List[str]: The labels of the dataset.
        export_dir (str): Path to the directory to export the dataset card to.
        hf_dataset_id (str,): The Hugging Face dataset ID.
        task (str, optional): The task of the dataset. Defaults to "object-detection".
        roboflow_universe_url (str, optional): The Roboflow Universe URL. Defaults to None.
        split_name_to_num_samples (dict, optional): A dictionary mapping split names to the number of samples in the split. Defaults to None.
    """
    Path(export_dir).mkdir(parents=True, exist_ok=True)

    hf_task = "image-segmentation" if task == "instance-segmentation" else task

    # export split_name_to_num_samples as json
    if split_name_to_num_samples is not None:
        with open(f"{export_dir}/split_name_to_num_samples.json", "w") as f:
            json.dump(split_name_to_num_samples, f)

    # parse reboflow info
    (
        license,
        dataset_url,
        citation,
        roboflow_dataset_summary,
        roboflow_tags,
    ) = read_roboflow_info(
        local_data_dir=export_dir, roboflow_universe_url=roboflow_universe_url
    )

    # generate tags string line by line
    roboflow_tags_str = ""
    for ind, roboflow_tag in enumerate(roboflow_tags):
        roboflow_tags_str += f"- {roboflow_tag}"
        if ind != len(roboflow_tags) - 1:
            roboflow_tags_str += "\n"

    if split_name_to_num_samples is not None:
        num_samples_line = f"""
### Number of Images

```json
{split_name_to_num_samples}
```
"""
    else:
        num_samples_line = ""

    card = f"""---
task_categories:
- {hf_task}
tags:
- roboflow
- roboflow2huggingface
{roboflow_tags_str}
---

<div align="center">
  <img width="640" alt="{hf_dataset_id}" src="https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/thumbnail.jpg">
</div>

### Dataset Labels

```
{dataset_labels}
```

{num_samples_line}

### How to Use

- Install [datasets](https://pypi.org/project/datasets/):

```bash
pip install datasets
```

- Load the dataset:

```python
from datasets import load_dataset

ds = load_dataset("{hf_dataset_id}", name="full")
example = ds['train'][0]
```

### Roboflow Dataset Page
[{dataset_url}]({dataset_url}?ref=roboflow2huggingface)

### Citation

```
{citation}
```

### License
{license}

### Dataset Summary
{roboflow_dataset_summary}
"""

    with open(Path(export_dir) / "README.md", "w") as f:
        f.write(card)
