import requests
import aiohttp
import asyncio
import websockets
import json
import io
from urllib import parse
from requests import Response
from websockets.client import WebSocketClientProtocol

from .methods import SlackMethods


class SlackClient:
    base_url = 'https://slack.com/api/'
    token: str
    cookies: dict
    socket: WebSocketClientProtocol

    def __init__(self, token: str, cookies):
        self.token = token

        if isinstance(cookies, list):
            self.cookies = {cookie['name']: cookie['value'] for cookie in cookies}
        else:
            self.cookies = cookies

    def join_channels(self, channels):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = asyncio.gather(*[self.join_channel_async(channel) for channel in channels])
        results = loop.run_until_complete(tasks)
        loop.close()
        return results

    def leave_channels(self, channels):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = asyncio.gather(*[self.leave_channel_async(channel) for channel in channels])
        results = loop.run_until_complete(tasks)
        loop.close()
        return results

    async def join_channel_async(self, channel):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}{SlackMethods.conversations_join}?{self.__channel_payload(channel)}'
            async with session.post(url=url, cookies=self.cookies) as response:
                return await response.json()

    async def leave_channel_async(self, channel):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}{SlackMethods.conversations_leave}?{self.__channel_payload(channel)}'
            async with session.post(url=url, cookies=self.cookies) as response:
                return await response.json()

    def upload_file(self, file, file_name):
        payload = {"content": file, "filename": file_name}
        headers = {'Authorization': f"Bearer {self.token}"}
        return requests.post(f"{self.base_url}{SlackMethods.upload_file}", data=payload,
                             headers=headers, cookies=self.cookies).json()

    def download_file(self, file_url) -> Response:
        headers = {'Authorization': f"Bearer {self.token}"}
        return requests.get(file_url, headers=headers, cookies=self.cookies)

    def delete_file(self, file_id: str):
        payload = {"file": file_id}
        headers = {'Authorization': f"Bearer {self.token}"}
        return requests.post(f"{self.base_url}{SlackMethods.delete_file}", data=payload,
                             headers=headers, cookies=self.cookies).json()

    def share_files(self, files_ids: list, channel: str, text: str = None) -> dict:
        payload = {
            "files": ','.join(files_ids),
            "channel": channel,
        }
        if text:
            payload["blocks"] = json.dumps([{"type": "rich_text", "elements": [
                {"type": "rich_text_section", "elements": [{"type": "text", "text": text}]}]}])

        headers = {'Authorization': f"Bearer {self.token}"}
        return requests.post(f"{self.base_url}{SlackMethods.share_files}", data=payload,
                             headers=headers, cookies=self.cookies).json()

    def get_profile(self, user_id: str = None):
        url = f'{self.base_url}{SlackMethods.profile_get}?{self.__token_payload()}'
        if user_id:
            url += f"&user={user_id}"

        return requests.get(url=url, cookies=self.cookies).json()

    def update_profile(self, profile):
        url = f'{self.base_url}{SlackMethods.profile_set}?{self.__update_profile_payload(profile)}'
        return requests.post(url=url, cookies=self.cookies).json()

    def update_profile_photo(self, photo_url):
        url = f'{self.base_url}{SlackMethods.profile_set_photo}'
        with requests.get(photo_url) as img_resp:
            if img_resp.status_code != 200:
                raise Exception(f"Invalid url: {photo_url}")
            image = io.BytesIO(img_resp.content)

            files = {"image": image}
            headers = {"Authorization": f"Bearer {self.token}"}

            return requests.post(url=url, files=files, headers=headers, cookies=self.cookies, verify=False).json()

    def get_conversations_list(self):
        url = f'{self.base_url}{SlackMethods.conversations_list}?' \
              f'{self.__conversation_list_payload(["public_channel"])}'
        result = requests.get(url=url, cookies=self.cookies).json()
        if result["ok"]:
            result["channels"] = [ch for ch in result["channels"]
                                  if ch.get('is_channel')
                                  and not ch.get('is_archived')
                                  and not ch.get('is_frozen')]

        return result

    def get_im_list(self):
        url = f'{self.base_url}{SlackMethods.conversations_list}?{self.__conversation_list_payload(["im"])}'
        return requests.get(url=url, cookies=self.cookies).json()

    def im_open(self, user: str):
        url = f'{self.base_url}{SlackMethods.conversations_open}?{self.__im_open_payload(user)}'
        return requests.post(url=url, cookies=self.cookies).json()

    def delete_message(self, channel: str, ts: str):
        url = f'{self.base_url}{SlackMethods.chat_delete}?{self.__delete_message_payload(channel, ts)}'
        return requests.post(url=url, cookies=self.cookies).json()

    def conversations_info(self, channel: str):
        url = f'{self.base_url}{SlackMethods.conversations_info}?{self.__conversation_info_payload(channel)}'
        return requests.post(url=url, cookies=self.cookies).json()

    def update_message(self, channel: str, ts: str, text: str, file_ids: str):
        url = f'{self.base_url}{SlackMethods.chat_update}?{self.__update_message_payload(channel, ts, text, file_ids)}'
        return requests.post(url=url, cookies=self.cookies).json()

    def conversations_history(self, channel: str, ts: str = None):
        url = f'{self.base_url}{SlackMethods.conversations_history}?{self.__channel_payload(channel, ts)}'
        return requests.get(url=url, cookies=self.cookies).json()

    def conversations_replies(self, channel: str, ts: str):
        url = f'{self.base_url}{SlackMethods.conversations_replies}?{self.__ts_payload(channel, ts)}'
        return requests.get(url=url, cookies=self.cookies).json()

    def get_presense(self, user: str = None):
        url = f'{self.base_url}{SlackMethods.users_get_presence}?{self.__presense_payload(user)}'
        return requests.get(url=url, cookies=self.cookies).json()

    def post_message(self, channel: str, text: str):
        url = f'{self.base_url}{SlackMethods.chat_post_message}?{self.__post_message_payload(channel, text)}'
        return requests.post(url=url, cookies=self.cookies).json()

    def post_message_schedule(self, channel: str, text: str, post_at: int):
        url = f'{self.base_url}{SlackMethods.chat_schedule_message}?{self.__post_scheduled_message_payload(channel, text, post_at)}'
        return requests.post(url=url, cookies=self.cookies).json()

    def users_list(self, cursor=None, limit: int = 1000):
        url = f'{self.base_url}{SlackMethods.users_list}?{self.__token_payload()}'
        if cursor:
            url += f'&cursor={cursor}'

        if limit:
            url += f'&limit={limit}'

        return requests.get(url=url, cookies=self.cookies).json()

    def user_info(self, user: str):
        url = f'{self.base_url}{SlackMethods.users_info}?{self.__user_info_payload(user)}'
        return requests.get(url=url, cookies=self.cookies).json()

    def get_reactions(self, channel: str, ts: str):
        url = f'{self.base_url}{SlackMethods.reactions_get}?{self.__get_reactions_payload(channel, ts)}'
        return requests.get(url=url, cookies=self.cookies).json()

    def check_email(self, email: str, user_agent: str) -> bool:
        payload = {'email': email}
        headers = {'User-Agent': user_agent}
        response = requests.post(f"{self.base_url}/{SlackMethods.check_email}", params=payload, headers=headers)
        if response.status_code != 200:
            return False
        return response.json()['ok']

    def confirm_email(self, email: str, user_agent: str, locale: str = 'en-US') -> bool:
        payload = {'email': email, 'locale': locale}
        headers = {'User-Agent': user_agent}
        response = requests.post(f"{self.base_url}/{SlackMethods.confirm_email}", params=payload, headers=headers)
        if response.status_code != 200:
            return False
        return response.json()['ok']

    def confirm_code(self, email: str, code: str, user_agent: str) -> requests.Response:
        payload = {'email': email, 'code': code}
        headers = {'User-Agent': user_agent}
        return requests.post(f"{self.base_url}/{SlackMethods.confirm_code}", params=payload, headers=headers)

    def find_workspaces(self, user_agent: str) -> requests.Response:
        headers = {'User-Agent': user_agent}
        response = requests.post(f"{self.base_url}/{SlackMethods.find_workspaces}",
                                 cookies=self.cookies, headers=headers)
        return response

    def create_shared_invite(self):
        expiration = '36000'
        max_signups = '100'
        payload = {
            'expiration': expiration,
            'max_signups': max_signups
        }
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{self.base_url}/{SlackMethods.create_shared_invite}", headers=headers,
                                 cookies=self.cookies, params=payload)
        return response
    def rtm_connect(self, callback):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.__consumer(callback))
        loop.run_forever()

    async def __consumer(self, callback):
        url = f'{self.base_url}{SlackMethods.rtm_connect}?{self.__token_payload()}'
        response = requests.get(url=url, cookies=self.cookies).json()
        web_socket_url = response['url']
        async with websockets.connect(uri=web_socket_url) as websocket:
            self.socket = websocket
            async for message in websocket:
                await callback(json.loads(message))

    def __token_payload(self):
        return parse.urlencode({'token': self.token})

    def __user_info_payload(self, user):
        payload = {
            'token': self.token,
            'user': user
        }
        return parse.urlencode(payload)

    def __post_message_payload(self, channel, text):
        payload = {
            'token': self.token,
            'channel': channel,
            'text': text
        }
        return parse.urlencode(payload)

    def __post_scheduled_message_payload(self, channel, text, post_at):
        payload = {
            'token': self.token,
            'channel': channel,
            'text': text,
            'post_at': post_at
        }
        return parse.urlencode(payload)

    def __update_message_payload(self, channel, ts, text, file_ids):
        payload = {
            'parse': 'none',
            'token': self.token,
            'channel': channel,
            'ts': ts,
            'text': text,
            'file_ids': file_ids
        }
        return parse.urlencode(payload)

    def __conversation_info_payload(self, channel):
        payload = {
            'token': self.token,
            'channel': channel,
            'include_num_members': "true"
        }
        return parse.urlencode(payload)

    def __delete_message_payload(self, channel, ts):
        payload = {
            'token': self.token,
            'channel': channel,
            'ts': ts
        }
        return parse.urlencode(payload)

    def __conversation_list_payload(self, types: list):
        payload = {
            'token': self.token,
            'types': ','.join(types)
        }
        return parse.urlencode(payload)

    def __im_open_payload(self, user: str):
        payload = {
            'token': self.token,
            'users': user,
            'types': 'im'
        }
        return parse.urlencode(payload)

    def __update_profile_payload(self, profile):
        payload = {
            'token': self.token,
            'profile': profile
        }
        return parse.urlencode(payload)

    def __channel_payload(self, channel, ts=None):
        payload = {
            'token': self.token,
            'channel': channel
        }

        if ts:
            payload["ts"] = ts
            payload["limit"] = 1
            payload["inclusive"] = True

        return parse.urlencode(payload)

    def __presense_payload(self, user: str = None):
        payload = {
            'token': self.token,
        }

        if user:
            payload["user"] = user
        return parse.urlencode(payload)

    def __ts_payload(self, channel: str, ts: str):
        payload = {
            'token': self.token,
            'channel': channel,
            'ts': ts
        }
        return parse.urlencode(payload)

    def __get_reactions_payload(self, channel, ts):
        payload = {
            'token': self.token,
            'full': True,
            'channel': channel,
            'timestamp': ts
        }
        return parse.urlencode(payload)
