from txp.common.utils.bigquery_utils import get_partition_utc_date


def from_proto_to_json(proto):
    timestamp, index = proto.metadata.package_id.split("_")
    timestamp = int(timestamp)
    index = int(index)
    prev_index = proto.metadata.previous_part_index
    res = []
    for signal in proto.signals:
        row = {
            "data": [],
            "package_timestamp": timestamp,
            "signal_timestamp": signal.timestamp,
            "previous_part_index": prev_index,
            "part_index": index,
            "perception_name": signal.perception_name,
            "edge_logical_id": proto.metadata.edge_descriptor.logical_id,
            "configuration_id": proto.configuration_id,
            "label": "{'label_value': "", 'parameters':{}}",
            "observation_timestamp": proto.metadata.sampling_window.observation_timestamp,
            "gateway_task_id": proto.metadata.sampling_window.gateway_task_id,
            "sampling_window_index": proto.metadata.sampling_window.sampling_window_index,
            "number_of_sampling_windows": proto.metadata.sampling_window.number_of_sampling_windows,
            "tenant_id": proto.metadata.tenant_id,
            "device_type": proto.metadata.edge_descriptor.device_type,
            "sampling_window_observation_time": proto.metadata.sampling_window.observation_time
        }
        row["partition_timestamp"] = str(get_partition_utc_date(row["observation_timestamp"]))
        for i, dimension_signal_sample in enumerate(signal.samples):
            row["data"].append({
                "values": list(dimension_signal_sample.samples),
                "index": i
            })
            i += 1
        res.append(row)
    return res
