import json
from abc import ABC, abstractmethod
from hashlib import md5
from pathlib import Path
from typing import List, Optional, Sequence, Tuple, Type, TypeVar, Union

import numpy as np


def determine_load_path(
    base_path_list: Sequence[Path],
    robot_name: Optional[str] = None,
    urdf_path: Optional[Path] = None,
    criterion: str = "time_stamp",
) -> Path:

    dir_path_list = []
    for base_path in base_path_list:
        base_path = base_path.expanduser()
        dir_path_list.extend(base_path.iterdir())

    urdf_md5sum: Optional[str] = None
    if urdf_path is not None:
        urdf_path = urdf_path.expanduser()
        assert urdf_path.exists()
        with urdf_path.open(mode="r") as f:
            urdf_string = f.read()
        urdf_md5sum = md5(urdf_string.encode("utf8")).hexdigest()

    best_dir_path: Optional[Path] = None
    best_score = -np.inf
    for dir_path in dir_path_list:
        if not dir_path.name.startswith("pretrained"):
            continue
        json_path = dir_path / "metadata.json"
        with json_path.open(mode="r") as f:
            json_dict = json.load(f)

        # check robot name match
        if robot_name is not None:
            if json_dict["robot_name"] != robot_name:
                continue

        # check urdf md5sum match
        if urdf_md5sum is not None:
            if json_dict["urdf_md5sum"] != urdf_md5sum:
                continue

        if criterion == "time_stamp":
            score = json_dict["time_stamp"]
        elif criterion == "valid_loss":
            score = json_dict["valid_loss"]
        else:
            assert False, "no such criterion {}".format(criterion)

        if best_score < score:
            best_score = score
            best_dir_path = dir_path

    assert best_dir_path is not None, "no pretrained model found matching condition"

    return best_dir_path


InferencerT = TypeVar("InferencerT", bound="SelColInferencerBase")


class SelColInferencerBase(ABC):
    joint_names: List[str]
    eval_joint_indices: Optional[np.ndarray]  # int
    _context: Optional[np.ndarray]

    @classmethod
    def load(
        cls: Type[InferencerT],
        base_path: Union[Path, Sequence[Path]],
        eval_joint_names: Optional[List[str]] = None,
        robot_name: Optional[str] = None,
        urdf_path: Optional[Path] = None,
        criterion: str = "time_stamp",
    ) -> InferencerT:
        if not isinstance(base_path, Sequence):
            base_path = [base_path]
        load_path = determine_load_path(base_path, robot_name, urdf_path, criterion)
        return cls.load_from_path(load_path, eval_joint_names)

    @classmethod
    @abstractmethod
    def load_from_path(
        cls: Type[InferencerT], dir_path: Path, eval_joint_names: Optional[List[str]] = None
    ) -> InferencerT:
        ...

    @abstractmethod
    def infer(self, q: np.ndarray, with_grad: bool = False) -> Tuple[float, np.ndarray]:
        ...

    def set_context(self, q: np.ndarray) -> None:
        assert len(q) == self.dof
        self._context = q

    @property
    def dof(self) -> int:
        return len(self.joint_names)

    @property
    def eval_dof(self) -> int:
        if self.eval_joint_indices is None:
            return self.dof
        else:
            return len(self.eval_joint_indices)
