import json
from typing import Dict
from pathlib import Path


def write_to_xcom(dict_value: Dict) -> Dict:
    """Write `dict_value` for XCOM to pass it to the next task

    ref: https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#how-does-xcom-work

    """
    file_save = Path('/airflow/xcom/return.json')
    file_save.parent.mkdir(parents=True, exist_ok=True)

    # Get data from the file if there is some
    if file_save.is_file():
        with file_save.open('r') as fin:
            dict_restored = json.load(fin)

    else:
        dict_restored = dict()

    # Update dict with new data
    dict_restored.update(dict_value)

    # Overwrite file with updated dict
    with file_save.open('w') as fout:
        json.dump(dict_restored, fout)
    return dict_restored
