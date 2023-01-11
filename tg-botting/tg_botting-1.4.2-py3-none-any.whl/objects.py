import datetime
import json
from enum import Enum

from .user_utils import username_cahce, user_cache

class Command:
    def __init__(self,func,name,description=None,aliases=None,usage=None,roles=None,ignore_filter=False,has_arts=False):
        self.func = func
        self.name = name
        self.roles = roles
        self.description = description
        self.aliases = aliases
        self.usage = usage
        self.ignore_filter = ignore_filter
        self.has_arts=has_arts

class CallbackQuery:
    def __init__(self, bot, payload):

        self.id = payload.get('id')
        self.user = User(payload.get('from'))
        self.message = Message(bot, payload.get('message'))
        self.chat_instance = payload.get('chat_instance')
        self.data = payload.get('data') if 'data' in payload else None

class KButton:
    def __init__(self, text: str, callback_data=None, url=None):
        self.text = text
        self.url = url
        self.callback_data = callback_data

    def to_dict(self):
        dic = {
            'text': self.text
        }
        if self.url:
            dic.update({'url': self.url})
        if self.callback_data:
            dic.update({'callback_data': self.callback_data})
        return dic


class Keyboard:
    def __init__(self, resize=False, one_time=False, selective=False):
        self.inline_keyboard_button = []
        self.resize = resize
        self.one_time = one_time
        self.selective = selective

    def add_button(self, button: KButton):
        self.inline_keyboard_button.append(button)

    def to_dict(self):
        dic = []
        for button in self.inline_keyboard_button:
            dic.append(button.to_dict())

        dic_ = [dic]
        dic1 = {
            'inline_keyboard': dic_,
            'resize_keyboard': self.resize,
            'one_time_keyboard': self.one_time,
            'selective': self.selective
        }
        return dic1


class Message:
    def __init__(self, bot, payload):
        self.message_id = payload.get('message_id')
        self.user = User(payload.get('from'))
        self.chat = Chat(payload.get('chat'))
        self.reply_to_message = Message(bot, payload.get('reply_to_message')) if payload.get(
            'reply_to_message') else None
        self.is_self = payload.get('is_self') if 'is_self' in payload else False
        self.photo = Photo(payload.get('photo')[len(payload.get('photo')) - 1]) if 'photo' in payload else None
        self.sticker = Sticker(payload.get('sticker')) if 'sticker' in payload else None
        self.bot = bot
        self.date = datetime.datetime.fromtimestamp(payload.get('date'))
        self.text = payload.get('text') or payload.get('caption')
        self.edit_date = datetime.datetime.fromtimestamp(payload.get('edit_date')) if 'edit_date' in payload else None
        self.new_chat_member = User(payload.get('new_chat_member')) if 'new_chat_member' in payload else None
        self.media_group_id = payload.get('media_group_id') if 'media_group_id' in payload else -1
        try:
            if 'entities' in payload:
                self.entities = [Entity(p) for p in payload.get('entities')]
            else:
                self.entities = []
        except Exception:
            self.entities = []


    async def delete_message(self):
        return await self.bot.delete_message(self.chat.id,self.message_id)

    def get_text(self) -> str:
        return self.text

    async def send_photo(self,photo_id:str,**kwargs):
        return await self.bot.send_photo(self.chat.id,photo_id,**kwargs)

    async def send(self,text: str, reply_markup=None, **kwargs):
        return await self.bot.send_message(self.chat.id, text, reply_markup, **kwargs)

    async def get_appeal(self, offset=1):
        count = 1
        for s in self.text.split(' '):
            if s.startswith('@'):
                if count == offset:
                    return await User.load(self.chat.id, s, self.bot)

                else:
                    count += 1

    async def edit(self, text: str, **kwargs):
        if self.user.is_bot:
            data = {
                'chat_id': self.chat.id,
                'message_id': self.message_id,
                'text': text
            }
            data.update(kwargs)
            rs = await self.bot.tg_request('editMessageText', True, **data)
            return Message(self.bot, rs.get('result'))

    async def reply(self, text, reply_markup=None, photo=None,parse_mode=None, **kwargs):
        data = {
            'chat_id': self.chat.id or kwargs['chat_id'],
            'reply_to_message_id': self.message_id
        }
        if parse_mode:
            data['parse_mode'] = parse_mode
        if reply_markup:
            data['reply_markup'] = json.dumps(reply_markup.to_dict())
        if photo:
            data['caption'] = text
            data.pop('chat_id')
            return await self.send_photo(photo,**data)

        data['text'] = text
        if self.chat.id != self.message_id:
            del data["reply_to_message_id"]
        rs = await self.bot.tg_request('sendMessage', True, **data)
        return rs.get('ok')





class Sticker:
    def __init__(self, payload):
        self.width = payload.get('width')
        self.height = payload.get('height')
        self.emoji = payload.get('emoji')
        self.set_name = payload.get('set_name')
        self.is_animated = payload.get('is_animated')
        self.is_video = payload.get('is_video')
        self.type = payload.get('type')
        self.thumb = Photo(payload.get('thumb'))
        self.file_id = payload.get('file_id')
        self.file_unique_id = payload.get('file_unique_id')


class Photo:
    def __init__(self, payload):
        self.file_id = payload.get('file_id')
        self.file_unique_id = payload.get('file_unique_id')
        self.file_size = payload.get('file_size')
        self.width = payload.get('width')
        self.height = payload.get('height')


class User:
    def __init__(self, payload):
        self.id = payload.get('id')
        self.is_bot = payload.get('is_bot')
        self.first_name = payload.get('first_name')
        self.last_name = payload.get('last_name')
        self.username = payload.get('username')
        self.language_code = payload.get('language_code')

    @staticmethod
    async def load(chat_id: int, username, bot):
        if username in username_cahce:
            return user_cache.get(username_cahce.get(username))
        else:
            rs = await bot.pyrogram.get_chat_member(chat_id, username)
            user = await User.parse_user(rs.user)
            user_cache.update({user.id: user})
            username_cahce.update({username: user.id})
            return user

    @staticmethod
    async def parse_user(us):
        user = User({})
        user.id = us.id
        user.is_self = us.is_self
        user.is_bot = us.is_bot
        user.first_name = us.first_name
        user.last_name = us.last_name
        user.username = us.username
        return user

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

class Entity:
    def __init__(self, payload):
        self.user = User(payload.get('user'))
        self.offset = payload.get('offset')
        self.length = payload.get('length')
        self.type = payload.get('type')



class UserChat:
    def __init__(self, payload):
        self.first_name = payload.get('first_name')
        self.last_name = payload.get('last_name')
        self.username = payload.get('username')


class GroupChat:
    def __init__(self, payload):
        self.title = payload.get('title')
        self.all_members_are_administrators = payload.get('all_members_are_administrators')


class Chat:
    def __init__(self, payload):
        self.id = payload.get('id')
        self.type = payload.get('type')
        if type == 'private':
            self.chatObj = UserChat(payload)
        elif type == 'group':
            self.chatObj = GroupChat(payload)


class ChatActions(Enum):
    TYPING = "typing"
    UPLOAD_PHOTO = 'upload_photo'
    RECORD_VIDEO = 'record_video'
    UPLOAD_VIDEO = 'upload_video'
    RECORD_AUDIO = 'record_audio'
    UPLOAD_AUDIO = 'upload_audio'
    UPLOAD_DOCUMENT = 'upload_document'
    FIND_LOCATION = 'find_location'


class UserProfilePicture:
    def __init__(self, payload):
        self.count = payload.get('total_count')
        self.photos = [Photo(photo) for photo in payload.get('photos')[0]]
