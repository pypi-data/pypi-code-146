from pathlib import Path
from typing import List
from roboflow2huggingface.roboflow_utils import read_roboflow_info


def export_hf_dataset_card(
    dataset_labels: List[str],
    export_dir: str,
    task="object-detection",
    roboflow_universe_url: str = None,
):
    """
    Exports a dataset card to the specified directory.

    Args:
        dataset_labels List[str]: The labels of the dataset.
        export_dir (str): Path to the directory to export the dataset card to.
        task (str, optional): The task of the dataset. Defaults to "object-detection".
        roboflow_universe_url (str, optional): The Roboflow Universe URL. Defaults to None.
    """
    license, dataset_url, citation, roboflow_dataset_summary = read_roboflow_info(
        local_data_dir=export_dir, roboflow_universe_url=roboflow_universe_url
    )

    card = f"""---
task_categories:
- {task}
tags:
- roboflow
---

### Roboflow Dataset Page
[{dataset_url}]({dataset_url}?ref=roboflow2huggingface)

### Dataset Labels

```
{dataset_labels}
```

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
