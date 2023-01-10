from Bubot.Core.Obj import Obj
from Bubot.Helpers.ActionDecorator import async_action
from Bubot.Helpers.ExtException import ExtException, AccessDenied, KeyNotFound, Unauthorized
from Bubot.Helpers.Helper import ArrayHelper


class User(Obj):
    name = 'user'
    file = __file__

    @property
    def db(self):
        return 'Bubot'

    @classmethod
    async def find_by_cert(cls, storage, cert, create=False):
        data = cert.get_user_data_from_cert()
        self = cls(storage)
        try:
            data = await self.find_by_keys(data['keys'])
            self.init_by_data(data)
        except KeyError:
            if create:
                self.init_by_data(data)
                await self.update()
            else:
                raise KeyError
        return self

    @async_action
    async def add_auth(self, data, *, _action=None, **kwargs):
        session = kwargs.get('session', {})
        user_id = session.get('user')
        try:
            _action.add_stat(await self.find_user_by_auth(data['type'], data['id']))
            raise ExtException(message='Такой пользователь уже зарегистрирован')
        except Unauthorized:
            pass
        if user_id:
            try:
                _action.add_stat(await self.find_by_id(user_id, projection={'_id': 1, 'auth': 1}))
                _action.add_stat(await self.push('auth', data))
            except KeyError:
                session['user'] = None
        else:
            self.data = {
                'title': data['id'],
                'auth': [data]
            }
            res = _action.add_stat(await self.update())
            return res

    @async_action
    async def update_auth(self, auth_data, *, _action=None, **kwargs):
        _action.add_stat(await self.update({
            '_id': self.obj_id,
            'auth.$[auth]': auth_data
        }, array_filters=[
            {'auth.type': auth_data['type']}
        ]))

    @async_action
    async def find_user_by_auth(self, _type, _id, *, _action=None, **kwargs):
        # self.add_projection(kwargs)
        # kwargs['projection']['auth'] = True
        res = _action.add_stat(await self.list(
            where={
                'auth.type': _type,
                'auth.id': _id,
            },
            _form=None,
            limit=1
        ))
        if not res:
            raise Unauthorized()
        i = ArrayHelper.find_by_key(res[0]['auth'], _type, 'type')
        if i < 0:
            raise Unauthorized()
        user_data = res[0]
        auth = user_data.pop('auth')
        self.init_by_data(user_data)
        return auth[i]

    def get_default_account(self):
        accounts = self.data.get('account', [])
        if not accounts:
            return 'Bubot'

        _account = self.data.get('last_account')
        if _account is None:
            _account = accounts[0]
        return _account

    @classmethod
    @async_action
    async def check_right(cls, **kwargs):
        action = kwargs['_action']
        try:
            storage = kwargs['storage']
            user_ref = kwargs['user']
            account_id = kwargs['account']
            object_name = kwargs['object']
            level = kwargs['level']
            params = kwargs.get('params', {})
        except KeyError as key:
            raise KeyNotFound(detail=str(key))
        try:
            user = cls(storage, account_id=account_id, form='AccessRight')
            action.add_stat(await user.find_by_id(user_ref['_ref'].id))
            rights = user.data.get('right')
        except Exception as err:
            raise AccessDenied(parent=err)
        if not rights:
            raise AccessDenied(detail='Empty access list')
        try:
            _level = rights[object_name]['level']
        except Exception:
            raise AccessDenied(detail=object_name)
        if _level < level:
            raise AccessDenied(detail=object_name)
        pass
