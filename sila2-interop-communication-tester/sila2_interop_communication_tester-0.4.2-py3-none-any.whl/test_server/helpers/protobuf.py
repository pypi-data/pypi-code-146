from sila2_interop_communication_tester.grpc_stubs import SiLAFramework_pb2


def duration_from_seconds(seconds: float) -> SiLAFramework_pb2.Duration:
    seconds, rest = divmod(seconds, 1)
    return SiLAFramework_pb2.Duration(seconds=int(seconds), nanos=int(rest * 1e9))
