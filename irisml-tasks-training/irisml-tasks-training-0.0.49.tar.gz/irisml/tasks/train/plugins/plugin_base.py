class PluginBase:
    def on_train_start(self, trainer, model):
        pass

    def on_train_end(self, trainer, model):
        pass

    def on_train_epoch_start(self, trainer, model, epoch_index) -> bool:
        """If False is returned, the training will be stopped. Useful for early stopping."""
        return True

    def on_train_epoch_end(self, trainer, model, epoch_index):
        pass

    def on_train_batch_start(self, trainer, model, batch, batch_index):
        """Returns a modified batch."""
        return batch

    def on_train_batch_end(self, trainer, model, loss, batch, batch_index):
        pass

    def on_train_backward_start(self, trainer, model, loss):
        """Returns a modified loss."""
        return loss

    def on_train_backward_end(self, trainer, model):
        pass

    def on_optimizer_step_start(self, trainer, model, optimizer):
        """Returns an updated optimizer."""
        return optimizer

    def on_validation_start(self, trainer, model):
        pass

    def on_validation_end(self, trainer, model):
        pass

    def on_validation_batch_start(self, trainer, model, batch, batch_index):
        """Returns a modified batch."""
        return batch

    def on_validation_batch_end(self, trainer, model, loss, batch, batch_index):
        pass

    def forward_context(self):
        pass
