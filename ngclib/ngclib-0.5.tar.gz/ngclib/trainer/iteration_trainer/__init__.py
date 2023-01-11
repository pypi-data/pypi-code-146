"""Init file"""
from .sequential_trainer import SequentialTrainer
from .parallel_trainer import ParallelTrainer
from .base_iteration_trainer import BaseIterationTrainer

# pylint: disable=invalid-name
def NGCIterationTrainer(*args, parallel_training: bool = False, **kwargs) -> BaseIterationTrainer:
    """NGC Iteration Trainer builder"""
    if parallel_training:
        return ParallelTrainer(*args, **kwargs)
    return SequentialTrainer(*args, **kwargs)
