"""
This module defines the classes that supports the common structure
for ML Tasks of assets.
"""

from pydantic import BaseModel, Field, Extra
from typing import List, Dict, Union, Optional, Sequence
from enum import Enum
from functools import reduce
import numpy as np


class TaskEventTaxonomyEnum(Enum):
    """An event produced by a task, can be classified within this
    taxonomy.

    For example, for a ML task that recognizes the normal operation
    of a machine, the prediction output could be 'NormalOperation'.
    This output could be categorized as `Harmless`.
    """
    Detrimental = 'Detrimental'
    Harmless = 'Harmless'
    Neutral = 'Neutral'


class ClassificationLabelDefinition(BaseModel):
    labels: Dict[str, tuple]
    label_to_int: Optional[Dict[frozenset, int]]
    int_to_label: Optional[Dict[int, tuple]]
    label_to_category: Optional[Dict[str, str]]

    class Config:
        require_by_default = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        labels_list = list(sorted([category for category in self.labels.values()]))
        labels = np.array(np.meshgrid(*labels_list)).T.reshape(-1, len(labels_list))
        self.label_to_int = {frozenset(label.tolist()): i for i, label in enumerate(labels)}
        self.int_to_label = {i: tuple(label.tolist()) for i, label in enumerate(labels)}

        # initializes label to category map
        self.label_to_category = dict(
            reduce(
                list.__add__,
                [list(zip(lbls, [category]*len(lbls))) for category, lbls in self.labels.items()]
            )
        )

    def json(self, **kwargs):
        return super().json(exclude={"label_to_int", "int_to_label"}, **kwargs)

    def dic(self, **kwargs):
        return super().dict(exclude={"label_to_int", "int_to_label"}, **kwargs)

    def categories(self) -> List[str]:
        return list(self.labels.keys())

    def get_labels_in_category(self, category: str) -> List[str]:
        return self.labels[category]

    def is_valid_label_seq(self, label_seq: Sequence) -> True:
        """Returns true if the Set value of label_seq contains a valid label,
        independently of the sequence order."""
        seq_set = frozenset(label_seq)
        return seq_set in self.label_to_int


class AssetTask(BaseModel):
    """
    Args:
        label_def: The definition for the event labels of the task.

        task_id: A unique task_id under a given tenant asset.

        asset_id: The asset_id to which this task is associated.

        task_data: A string path in storage for the task model data.

        edges: The list of edges logical ids that feed this tasks as
            signal inputs.

        schema_: A Dictionary of Edges to expected Perception name and
            table name.

    A example of a schema would be:

    """
    label_def: ClassificationLabelDefinition
    task_type: str
    task_id: str
    asset_id: str = Field(alias='machine_id')
    task_data: Optional[str]
    edges: List[str]
    schema_: Dict[str, Dict[str, Dict[str, Union[bool, List]]]] = Field(alias='schema')
    parameters: Dict

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/602#issuecomment-503189368
        allow_population_by_field_name = True

    def json(self, **kwargs):
        return super().json(exclude={"label_def": {"label_to_int", "int_to_label"}}, **kwargs)

    def dic(self, **kwargs):
        return super().dict(exclude={"label_def": {"label_to_int", "int_to_label"}}, **kwargs)


class AssetStateCondition(Enum):
    OPTIMAL = "OPTIMAL"
    OPERATIONAL = "OPERATIONAL"
    UNDEFINED = "UNDEFINED"
    CRITICAL = "CRITICAL"
    GOOD = "GOOD"


class AssetState(BaseModel):
    events: List[str]
    asset_id: str
    condition: AssetStateCondition
    observation_timestamp: int
    tenant_id: str
    partition_timestamp: str
