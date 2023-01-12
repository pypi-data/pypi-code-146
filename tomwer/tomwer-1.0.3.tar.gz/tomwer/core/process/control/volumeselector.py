from ewokscore.task import Task as EwoksTask


class _VolumeSelectorPlaceHolder(
    EwoksTask, input_names=["volume"], output_names=["volume"]
):
    def run(self):
        self.outputs.volume = self.inputs.volume
