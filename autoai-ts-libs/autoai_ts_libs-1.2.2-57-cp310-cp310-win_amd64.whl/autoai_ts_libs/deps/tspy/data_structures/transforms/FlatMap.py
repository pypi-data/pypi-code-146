from autoai_ts_libs.deps.tspy.data_structures.transforms.ShapeChangingMapper import ShapeChangingMapper


class FlatMap(ShapeChangingMapper):
    def result_is_numpy(self, input_before_apply, input_after_apply, types_set):
        return len(input_after_apply) != 0 and input_after_apply[0] in types_set

    def handle_input_numpy(self, tts_reference, values_reference, tt, input_before_apply, input_after_apply):
        for v in input_after_apply:
            tts_reference.append(tt)
            values_reference.append(v)

    def handle_input_object(self, builder_reference, tt, input_before_apply, input_after_apply):
        for v in input_after_apply:
            builder_reference.add(tt, v)

    def apply_lambda(self, value):
        return self._f(value)
