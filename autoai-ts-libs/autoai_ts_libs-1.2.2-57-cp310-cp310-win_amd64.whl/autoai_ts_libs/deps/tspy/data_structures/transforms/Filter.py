from autoai_ts_libs.deps.tspy.data_structures.transforms.ShapeChangingMapper import ShapeChangingMapper


class Filter(ShapeChangingMapper):
    def __init__(self, f):
        super().__init__(f)

    def result_is_numpy(self, input_before_apply, input_after_apply, types_set):
        return type(input_before_apply) in types_set

    def handle_input_numpy(self, tts_reference, values_reference, tt, input_before_apply, input_after_apply):
        if input_after_apply:
            tts_reference.append(tt)
            values_reference.append(input_before_apply)

    def handle_input_object(self, builder_reference, tt, input_before_apply, input_after_apply):
        if input_after_apply:
            builder_reference.add(tt, input_before_apply)

    def apply_lambda(self, value):
        return self._f(value)
