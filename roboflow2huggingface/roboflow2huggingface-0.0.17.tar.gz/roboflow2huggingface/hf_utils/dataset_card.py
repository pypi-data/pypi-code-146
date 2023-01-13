from pathlib import Path
from typing import List
from roboflow2huggingface.roboflow_utils import read_roboflow_info


def export_hf_dataset_card(
    dataset_labels: List[str],
    export_dir: str,
    hf_dataset_id: str,
    task="object-detection",
    roboflow_universe_url: str = None,
):
    """
    Exports a dataset card to the specified directory.

    Args:
        dataset_labels List[str]: The labels of the dataset.
        export_dir (str): Path to the directory to export the dataset card to.
        hf_dataset_id (str,): The Hugging Face dataset ID.
        task (str, optional): The task of the dataset. Defaults to "object-detection".
        roboflow_universe_url (str, optional): The Roboflow Universe URL. Defaults to None.
    """
    license, dataset_url, citation, roboflow_dataset_summary = read_roboflow_info(
        local_data_dir=export_dir, roboflow_universe_url=roboflow_universe_url
    )

    if task == "object-detection":
        load_dataset_line = f'ds = load_dataset("{hf_dataset_id}", name="full")'
    else:
        load_dataset_line = f'ds = load_dataset("{hf_dataset_id}")'

    card = f"""---
task_categories:
- {task}
tags:
- roboflow
- roboflow2huggingface
---

<div align="center">
  <img width="640" alt="{hf_dataset_id}" src="https://huggingface.co/datasets/{hf_dataset_id}/resolve/main/thumbnail.jpg">
</div>

### Dataset Labels

```
{dataset_labels}
```

### How to Use

- Install [datasets](https://pypi.org/project/datasets/):

```bash
pip install datasets
```

- Load the dataset:

```python
from datasets import load_dataset

{load_dataset_line}
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
