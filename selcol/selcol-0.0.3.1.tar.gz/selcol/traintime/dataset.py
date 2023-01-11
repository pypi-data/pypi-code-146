import logging
import os
import pickle
import uuid
from dataclasses import dataclass
from hashlib import md5
from pathlib import Path
from typing import List, Optional, Set, Tuple
from xml.etree import ElementTree

import numpy as np
import tqdm
import trimesh
from skrobot.model.joint import RotationalJoint
from skrobot.model.robot_model import RobotModel
from skrobot.models.urdf import RobotModelFromURDF

logger = logging.getLogger(__name__)


@dataclass
class CollisionManagerWrap:
    _manager: trimesh.collision.CollisionManager
    _check_link_names: List[str]
    _robot_model: RobotModel
    _ignore_pair_set: Set

    @classmethod
    def from_model(
        cls,
        robot_model: RobotModel,
        ignore_link_names: Optional[List[str]] = None,
        use_visual_mesh: bool = True,
    ) -> "CollisionManagerWrap":
        col_manager = trimesh.collision.CollisionManager()

        def has_ignore_name(name: str) -> bool:
            if ignore_link_names is None:
                return False
            for ignore_name in ignore_link_names:
                if ignore_name in name:
                    return True
            return False

        check_link_names = []
        for link in robot_model.link_list:
            if has_ignore_name(link.name):
                continue

            transform = link.worldcoords().T()

            if use_visual_mesh:
                mesh = link.visual_mesh
                if len(mesh) == 0:
                    continue
                assert len(mesh) == 1
                mesh = mesh[0]
            else:
                # I didn't test this feature well.
                mesh = link.collision_mesh
                if mesh is None:
                    continue
            col_manager.add_object(link.name, mesh, transform=transform)
            check_link_names.append(link.name)

        _, ignore_set = col_manager.in_collision_internal(return_names=True)
        return cls(col_manager, check_link_names, robot_model, ignore_set)

    def update(self, robot_model: RobotModel) -> None:
        for link_name in self._check_link_names:
            link = robot_model.__dict__[link_name]
            link.visual_mesh
            transform = link.worldcoords().T()
            self._manager.set_transform(link.name, transform=transform)

    def check_collision(self, ignore: bool = True) -> Set[Tuple[str, str]]:
        _, pairs = self._manager.in_collision_internal(return_names=True)
        if ignore:
            pairs = pairs.difference(self._ignore_pair_set)
        return pairs


def get_random_robot_state(
    robot_model: RobotModel, control_joint_names: Optional[List[str]] = None
) -> np.ndarray:
    if control_joint_names is None:
        control_joint_names = robot_model.joint_names

    angles = []
    for jn in control_joint_names:
        joint = robot_model.__dict__[jn]
        if np.isinf(joint.min_angle) or np.isinf(joint.max_angle):
            assert isinstance(joint, RotationalJoint)
            lb = -np.pi
            ub = np.pi
        else:
            lb = joint.min_angle
            ub = joint.max_angle
        angles.append(np.random.rand() * (ub - lb) + lb)
    return np.array(angles)


@dataclass
class Metadata:
    robot_name: str
    urdf_md5sum: str
    joint_names: List[str]
    ignore_link_names: List[str]


@dataclass
class Chunk:
    header: Metadata
    samples: List[Tuple[np.ndarray, bool]]


@dataclass
class TaskArg:
    cache_path: Path
    urdf_path: Path
    ignore_link_names: List[str]
    joint_names: List[str]
    n_sample: int
    disable_tqdm: bool
    bin_filling: bool = False


# @dataclass
# class BinFillingSampler:
#     evaluator: Callable[[np.ndarray], float]
#     robot_model: RobotModel
#     bins: List[List[np.ndarray]]
#     bin_max_list: List[int]
#     max_failure: int = 1000
#
#     @classmethod
#     def create(
#         cls, f, robot_model: RobotModel, n_sample: int, n_bin: int = 20
#     ) -> "BinFillingSampler":
#         bins = [[] for _ in range(n_bin)]
#         bin_max_list = cls.split_number(n_sample, n_bin)
#         return cls(f, robot_model, bins, bin_max_list)
#
#     @staticmethod
#     def split_number(num, div):
#         return [num // div + (1 if x < num % div else 0) for x in range(div)]
#
#     def value_to_bin_index(self, value: float) -> int:
#         assert value <= 1.0 and value >= 0.0
#         n_bin = len(self.bins)
#         width = 1.0 / n_bin
#         return int(value // width)
#
#     def add(self, idx: int, sample: np.ndarray) -> bool:
#         n_max = self.bin_max_list[idx]
#         already_filled = len(self.bins[idx]) == n_max
#         if already_filled:
#             return False
#         self.bins[idx].append(sample)
#
#         is_filled_now = len(self.bins[idx]) == n_max
#         if is_filled_now:
#             logger.info("bin index {} is filled now".format(idx))
#
#         return True
#
#     def is_terminatd(self) -> bool:
#         for n_max, lst in zip(self.bin_max_list, self.bins):
#             if len(lst) < n_max:
#                 return False
#         return True
#
#     def populate(self):
#         n_total = sum(self.bin_max_list)
#         failure_count = 0
#         with tqdm.tqdm(total=n_total, smoothing=0.0) as pbar:
#             while not self.is_terminatd():
#                 vec = get_random_robot_state(self.robot_model)
#                 self.robot_model.angle_vector(vec)
#                 value = self.evaluator(vec)
#                 bin_idx = self.value_to_bin_index(value)
#                 added = self.add(bin_idx, vec)
#                 if added:
#                     failure_count = 0
#                     pbar.update(1)
#                 else:
#                     failure_count += 1
#                 if failure_count > self.max_failure:
#                     logger.warning("reached max failure count. abort and continue.")
#                     break


def create_raw_dataset_chunk(task_arg: TaskArg):
    assert task_arg.cache_path.exists()
    pid = os.getpid()
    np.random.seed(pid)
    logger.info("set seed to {}".format(pid))
    logger.info("task arg {}".format(task_arg))

    robot_model = RobotModelFromURDF(urdf_file=str(task_arg.urdf_path.expanduser()))
    manager = CollisionManagerWrap.from_model(
        robot_model, ignore_link_names=task_arg.ignore_link_names
    )

    urdf_path = task_arg.urdf_path.expanduser()
    with urdf_path.open(mode="r") as f:
        urdf_string = f.read()
    md5sum = md5(urdf_string.encode("utf8")).hexdigest()
    urdf = ElementTree.fromstring(urdf_string)
    header = Metadata(urdf.attrib["name"], md5sum, task_arg.joint_names, task_arg.ignore_link_names)

    if task_arg.bin_filling:
        assert False
        # cache_basepath = default_cache_basepath()
        # from selcol.neural import load_latest_model  # to avoid circular import

        # model, header = load_latest_model(cache_basepath, "pr2")
        # f, grad = model.as_jit_function()
        # sampler = BinFillingSampler.create(f, robot_model, task_arg.n_sample, n_bin=10)
        # sampler.populate()
        # robot_config_list = []
        # for lst in sampler.bins:
        #     robot_config_list.extend(lst)
    else:
        robot_config_list = []
        for _ in range(task_arg.n_sample):
            vec = get_random_robot_state(robot_model, task_arg.joint_names)
            robot_config_list.append(vec)

    samples: List[Tuple[np.ndarray, bool]] = []
    positive_count = 0
    for robot_config in tqdm.tqdm(robot_config_list, disable=task_arg.disable_tqdm):

        # update config
        for angle, jn in zip(robot_config, task_arg.joint_names):
            robot_model.__dict__[jn].joint_angle(angle)
        manager.update(robot_model)

        # check
        pairs = manager.check_collision()
        colliding = len(pairs) > 0
        samples.append((robot_config, colliding))
        if colliding:
            positive_count += 1

    file_path = task_arg.cache_path / (
        "dataset-{}-{}dof".format(header.robot_name, len(header.joint_names))
        + str(uuid.uuid4())
        + ".pkl"
    )

    logger.info("chunk positive ratio is {}".format(positive_count / len(samples)))
    logger.info("save chunk to {}".format(file_path))
    with file_path.open(mode="wb") as f:
        pickle.dump(Chunk(header, samples), f)
