import random

from tecton_proto.common.id_pb2 import Id


class IdHelper:
    @staticmethod
    def to_string(id: Id) -> str:
        return f"{id.most_significant_bits:016x}{id.least_significant_bits:016x}"

    @staticmethod
    def generate_string_id() -> str:
        return "%032x" % random.randrange(16**32)

    @staticmethod
    def generate_id() -> Id:
        return IdHelper.from_string(IdHelper.generate_string_id())

    @staticmethod
    def from_string(s) -> Id:
        res = Id()

        res.most_significant_bits = int(s[:16], 16)
        res.least_significant_bits = int(s[16:], 16)
        return res
