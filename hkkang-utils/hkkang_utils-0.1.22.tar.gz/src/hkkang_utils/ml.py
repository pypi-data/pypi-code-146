import math
import attrs

from typing import Type

@attrs.define
class Training_context():
    """Syntatic sugar to keep track of training step"""
    Trainer: Type = attrs.field()
    effective_batch_size: int = attrs.field()
    dataloader_batch_size: int = attrs.field()
    eval_freq_estep: int = attrs.field()
    max_estep: int = attrs.field()
    # For counting
    _steps_per_estep: int = attrs.field(init=False, default=None)

    def __enter__(self):
        self.Trainer.step += 1
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @property
    def steps_per_estep(self):
        if not self._steps_per_estep:
            self._steps_per_estep = math.ceil(self.effective_batch_size / self.dataloader_batch_size)
        return self._steps_per_estep

    @property
    def step(self):
        return self.Trainer.step

    @property
    def estep(self):
        return self.Trainer.step // self.steps_per_estep

    @property
    def is_state_to_update(self):
        return self.step != 0 and not (self.step % self.steps_per_estep)

    @property
    def is_state_to_eval(self):
        return self.is_state_to_update and not (self.estep % self.eval_freq_estep)

    @property
    def is_state_to_exit(self):
        return self.estep >= self.max_estep


if __name__ == "__main__":
    Training_context()