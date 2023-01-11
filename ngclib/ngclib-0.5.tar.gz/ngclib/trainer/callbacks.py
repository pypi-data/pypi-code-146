"""Callbacks for an NGCTrainer"""
from pathlib import Path
import os
from pytorch_lightning import Callback

class RemovePreviousTrainArtifacts(Callback):
    """Callback to remove the previous trains artifacts (*.tfevents files), if any available"""
    def _on_start(self, log_dir: Path):
        tfevents_files = sorted([str(x) for x in log_dir.glob("*tfevents*")])
        if len(tfevents_files) > 1:
            for file in tfevents_files[0: -1]:
                os.unlink(file)

    def on_train_start(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        """Clean up the .tfevents files, besides the last one."""
        self._on_start(Path(pl_module.logger.log_dir))

    def on_test_start(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        self._on_start(Path(pl_module.logger.log_dir))

class PlotGraph(Callback):
    """Plots the graph at fit/test start"""
    def on_fit_start(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        in_dir = Path(pl_module.logger.log_dir)
        pl_module.base_model.base_graph.draw(in_dir / "graph.png")

    def on_test_start(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        in_dir = Path(pl_module.logger.log_dir)
        pl_module.base_model.base_graph.draw(in_dir / "graph.png")
