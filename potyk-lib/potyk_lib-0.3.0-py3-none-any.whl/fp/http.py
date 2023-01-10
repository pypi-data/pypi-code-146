import dataclasses
from typing import Callable, Tuple, Union, Any, TypeVar, Generic, Optional, Protocol

__all__ = [
    'Json', 'StatusCode', 'Response',
    'HttpRes', 'WithToJson',
]

Json = Union[dict, list]
StatusCode = Code = int
Response = Tuple[Json, StatusCode]
IdType = TypeVar('IdType')
HttpResT = TypeVar('HttpResT')


@dataclasses.dataclass
class MsgResp:
    msg: str = ''


@dataclasses.dataclass
class IdResp(Generic[IdType]):
    id: IdType


class WithToJson(Protocol):
    def to_json(self):
        ...


@dataclasses.dataclass()
class HttpRes(Generic[HttpResT]):
    success: bool
    resp: HttpResT
    code: Optional[int] = None

    def __post_init__(self):
        self.code = self.code or (200 if self.success else 400)

    @classmethod
    def ok(cls, resp=None, code=None, **kwargs):
        return cls(success=True, resp=resp or {}, code=code)

    @classmethod
    def err(cls, resp=None, code=None, **kwargs):
        return cls(success=False, resp=resp or {}, code=code)

    @classmethod
    def ok_msg(cls, msg='', code=None):
        return cls.ok(MsgResp(msg), code)

    @classmethod
    def err_msg(cls, msg='', code=None):
        return cls.err(MsgResp(msg), code)

    @classmethod
    def ok_id(cls, id_: IdType, code=None):
        return cls.ok(IdResp(id_), code)

    @classmethod
    def safe(cls, callable_: Callable[[], 'HttpRes'], ):
        try:
            return cls.ok(callable_())
        except Exception as e:
            return cls.err_msg(str(e))

    def flatten(self):
        if isinstance(self.resp, HttpRes):
            return self.resp
        else:
            return self

    def and_then(self, res: Callable[[], 'HttpRes']):
        return res() if self.success else self

    def or_else(self, res: Callable[[], 'HttpRes']):
        return self if self.success else res()

    @property
    def as_response(self) -> Response:
        return self.to_json(), self.code

    def to_json(self):
        def resp_to_json(resp):
            return (
                resp.to_json() if hasattr(resp, 'to_json') else
                (dataclasses.asdict(resp) if dataclasses.is_dataclass(resp) else
                 resp)
            )

        return (
            list(map(resp_to_json, self.resp)) if isinstance(self.resp, list) else
            resp_to_json(self.resp)
        )


def test_HttpRes():
    assert HttpRes.ok_msg('ok').as_response == ({'msg': 'ok'}, 200)
    assert HttpRes.err_msg('err').as_response == ({'msg': 'err'}, 400)
    assert HttpRes.ok_id('ok').as_response == ({'id': 'ok'}, 200)
    assert HttpRes.ok_id('ok').and_then(lambda: HttpRes.ok_msg('sam')).as_response == ({'msg': 'sam'}, 200)
    assert HttpRes.err_msg('err').and_then(lambda: HttpRes.ok_id('sam')).as_response == ({'msg': 'err'}, 400)
    assert HttpRes.ok_id('ok').or_else(lambda: HttpRes.ok_msg('sam')).as_response == ({'id': 'ok'}, 200)
    assert HttpRes.err_msg('err').or_else(lambda: HttpRes.ok_id('sam')).as_response == ({'id': 'sam'}, 200)

    class WithToJson:
        def to_json(self):
            return {'op': 'oppa'}

    assert HttpRes.ok(WithToJson()).as_response == ({'op': 'oppa'}, 200)
    assert HttpRes.ok([{'ass': 'tities'}]).as_response == ([{'ass': 'tities'}], 200)

    def raises():
        raise ValueError('op')

    assert HttpRes.safe(raises).as_response == ({'msg': 'op'}, 400)

    assert HttpRes.ok(HttpRes.ok_msg('ok')).flatten().as_response == ({'msg': 'ok'}, 200)
