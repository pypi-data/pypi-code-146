import pyarrow as pa

import sarus_data_spec.typing as st


def convert_record_batch(
    record_batch: pa.RecordBatch, _type: st.Type
) -> pa.Array:

    if str(_type.protobuf().WhichOneof('type')) not in ['struct', 'union']:
        return record_batch.column(0)

    names = list(_type.children().keys())
    if _type.protobuf().HasField('union'):
        # A Sarus Union is modelled a a Struct with an additional
        # `field_selected` field
        names.append('field_selected')

    return pa.StructArray.from_arrays(record_batch.columns, names=names)
