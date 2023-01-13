from abc import ABC, abstractmethod
import asyncio
import json

class Runner(ABC):

  @abstractmethod
  def solve(self, problem_file: str, spec: dict, **kwargs):
    pass

  @abstractmethod
  def solveBatched(self, problem_file: list, specs: list, **kwargs):
    pass

  @abstractmethod
  async def solveAsync(self, problem_files: str, spec: dict, **kwargs):
    pass

  @abstractmethod
  async def solveBatchedAsync(self, problem_files: list, specs: list, **kwargs):
    pass