from time import time
from uuid import uuid4

from aiohttp_session import AbstractStorage, Session as AiohttpSession
from bson import json_util as json

from Bubot.Helpers.ExtException import KeyNotFound
from BubotObj.Session.Session import Session


class SessionStorageMongo(AbstractStorage):
    def __init__(self, app, *, cookie_name="AIOHTTP_SESSION",
                 domain=None, max_age=None, path='/',
                 key_factory=lambda: str(uuid4()),
                 secure=None, httponly=True,
                 encoder=json.dumps, decoder=json.loads
                 ):
        super().__init__(cookie_name=cookie_name, domain=domain,
                         max_age=max_age, path=path, secure=secure,
                         httponly=httponly,
                         encoder=encoder, decoder=decoder)
        self.app = app
        self.handler = Session(app.get('storage'))
        self._key_factory = key_factory

    async def load_session(self, request):
        def empty_session():
            return AiohttpSession(None, data=None, new=True, max_age=self.max_age)

        cookie = self.load_cookie(request)
        if cookie is None:
            return empty_session()
        # key = self._decoder(cookie)
        key = cookie
        if key is None:
            return empty_session()
        try:
            stored_key = key
        except KeyError:
            return empty_session()
        try:
            data = await self.handler.find_by_id(stored_key, _form=None)
            data = data.result
            session_data = {
                'created': data.get('created', data.get('begin')),
                'session': {'user': data.get('user'), 'account': data.get('account')}

            }
            return AiohttpSession(key, data=session_data, new=False, max_age=self.max_age)
        except KeyNotFound:
            return empty_session()

    async def save_session(self, request, response, session):
        key = session.identity
        if key and not session.new and session.empty:  # закрыли сессию
            self.save_cookie(response, None, max_age=session.max_age)
            await self.handler.close(key)
            return

        if key is None:  # гостевая сессия
            key = self._key_factory()
            self.save_cookie(response, key,
                             max_age=session.max_age)
        else:
            if session.new:
                self.save_cookie(response, key, max_age=session.max_age)

        data: dict = self._get_session_data(session)
        max_age = session.max_age
        if max_age is None:
            expire = 0
        elif max_age > 30 * 24 * 60 * 60:
            expire = int(time()) + max_age
        else:
            expire = max_age
        try:
            # stored_key = key['_id']
            stored_key = key
        except Exception:
            raise Exception('Bad session key_factory')

        data['expire'] = expire
        data['_id'] = key
        self.handler.init_by_data(data)
        await self.handler.update()

    async def close(self):
        a = 1
        pass

    def _get_session_data(self, session: AiohttpSession):
        if session.empty:
            return {}

        return {**session._mapping, 'created': session.created}
