from datetime import datetime

from aiohttp_session import get_session, new_session
import time
from bson import ObjectId
from bson.errors import InvalidId

from Bubot.Core.DocumentObj import DocumentObj
from Bubot.Helpers.ActionDecorator import async_action
from Bubot.Helpers.ExtException import ExtException, KeyNotFound


class Session(DocumentObj):
    name = 'session'

    @property
    def db(self):
        return 'Bubot'

    def init(self):
        self.data = {
            "user": None,
            "account": None,
            "date": int(time.time()),
            "end": None
        }

    @classmethod
    @async_action
    async def init_from_request(cls, view, **kwargs):
        action = kwargs['_action']
        _session = await get_session(view.request)
        if not _session or not _session.identity:  # если авторизация происходит под чужой живой сессией грохаем её
            raise KeyNotFound(detail='session')
        self = cls(view.storage)
        action.add_stat(await self.find_by_id(_session.identity, _form=None))
        return action.set_end(self)

    @classmethod
    @async_action
    async def create_from_request(cls, user, view, **kwargs):
        action = kwargs['_action']
        old_session = None
        try:
            old_session = action.add_stat(await cls.init_from_request(view))
            if not old_session.data.get('end'):
                old_user = old_session.data.get('user')
                if old_user:
                    if user.obj_id == old_user['_id']:
                        return old_session
                    else:
                        action.add_stat(await old_session.close(cause='auth other user'))
        except KeyNotFound:
            pass
        data = {
            "user": user.get_link(),
            "account": user.get_default_account(),
            "begin": int(time.time())
        }
        if old_session:
            data['_id'] = old_session.data['_id']
            data['date'] = old_session.data['date']
        self = cls(view.storage)
        self.init_by_data(data)
        action.add_stat(await self.update())
        _session = await new_session(view.request)
        identity = self.get_identity()
        _session.set_new_identity(identity)
        _session['user'] = self.data['user']
        _session['account'] = self.data['account']
        # _session['_id'] = identity
        return self

    @async_action
    async def close(self, uuid=None, **kwargs):
        if uuid:
            await self.find_by_id(uuid)
        self.data['end'] = int(time.time())
        await self.update()

    def get_identity(self):
        return str(self.obj_id)
