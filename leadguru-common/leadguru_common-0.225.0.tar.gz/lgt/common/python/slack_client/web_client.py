import pytz
import requests
import os
from typing import Optional, List, Any
from google.cloud import storage
from pydantic import BaseModel, Extra
from dataclasses import dataclass
from datetime import datetime, timedelta
from lgt_data.model import UserModel, LeadModel, SlackHistoryMessageModel, BotModel
from lgt_data.mongo_repository import UserBotCredentialsMongoRepository, DedicatedBotRepository, BotMongoRepository
from .slack_client import SlackClient

slack_login_url = os.environ.get('SLACK_LOGIN_URL')


@dataclass
class LoginResponse:
    token: str

    """
     [{
            "name": "d-s",
            "value": "1589438217",
            "domain": ".slack.com",
            "path": "/",
            "expires": -1,
            "size": 13,
            "httpOnly": true,
            "secure": true,
            "session": true,
            "sameSite": "Lax"
        }]
    """
    cookies: []


@dataclass()
class LoginResponseV2:
    token: str
    """
     [{
            "name": "d-s",
            "value": "1589438217",
            "domain": ".slack.com",
            "path": "/",
            "expires": -1,
            "size": 13,
            "httpOnly": true,
            "secure": true,
            "session": true,
            "sameSite": "Lax"
        }]
    """
    cookies: []
    error: str
    image: str


class SlackCredentialsResponse(BaseModel, extra=Extra.ignore):
    token: Optional[str]
    slack_url: Optional[str]
    user_name: Optional[str]
    password: Optional[str]
    updated_at: Optional[datetime]
    invalid_creds: bool
    cookies: Optional[Any]


def get_system_slack_credentials(lead: LeadModel, bots: List[BotModel] = None) -> Optional[SlackCredentialsResponse]:
    """

    :rtype: UserBotCredentialsModel
    """

    if lead.is_dedicated_lead():
        dedicated_creds = lead.get_dedicated_credentials()
        return SlackCredentialsResponse(
            token=dedicated_creds.get("token"),
            slack_url=dedicated_creds.get("slack_url"),
            user_name=None,
            password=None,
            updated_at=lead.created_at,
            invalid_creds=False,
            cookies=dedicated_creds.get("cookies"),
        )

    credentials = bots if bots else BotMongoRepository().get()
    cred = next(filter(lambda x: x.name == lead.message.name, credentials), None)

    if not cred or cred.invalid_creds:
        return None

    return SlackCredentialsResponse(**cred.__dict__)


def get_slack_credentials(user: UserModel,
                          route: LeadModel,
                          update_expired=True,
                          user_bots=None,
                          dedicated_bots=None,
                          bots=None) -> Optional[SlackCredentialsResponse]:
    """

    :rtype: UserBotCredentialsModel
    """
    if route.is_dedicated_lead():
        return __get_dedicated_bot_credentials_for_personal_lead(user, route,
                                                                 update_expired=update_expired,
                                                                 dedicated_bots=dedicated_bots)

    cred = __get_dedicated_bot_credentials(user, route,
                                           update_expired=update_expired,
                                           dedicated_bots=dedicated_bots,
                                           bots=bots)
    if cred:
        return cred

    credentials = user_bots if user_bots else list(UserBotCredentialsMongoRepository().get_bot_credentials(user.id))
    cred = next(filter(lambda x: x.bot_name == route.message.name, credentials), None)

    if not cred or cred.invalid_creds:
        return None

    utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    cred_date_time = cred.updated_at.replace(tzinfo=pytz.UTC)
    # we have to update token since it might become outdated
    if update_expired and (utc_now - cred_date_time).days > 5:
        login_response = SlackWebClient.get_access_token(cred.slack_url, cred.user_name, cred.password)
        if not login_response:
            return None

        cred = UserBotCredentialsMongoRepository().update_bot_creadentials(user.id, cred.bot_name,
                                                                           cred.user_name, cred.password,
                                                                           cred.slack_url, login_response.token,
                                                                           login_response.cookies)
    return SlackCredentialsResponse(**cred.__dict__)


def __get_dedicated_bot_credentials(user: UserModel,
                                    lead: LeadModel,
                                    update_expired=True,
                                    dedicated_bots=None,
                                    bots=None) -> Optional[SlackCredentialsResponse]:
    bots = bots if bots is not None else BotMongoRepository().get()
    bot = next(iter([bot for bot in bots if bot.name == lead.message.name]), None)
    if not bot:
        return None

    slack_url = bot.slack_url.strip("/").lower()

    dedicated_bots = dedicated_bots if dedicated_bots is not None else DedicatedBotRepository().get_user_bots(user.id)
    bot = next(iter([bot for bot in dedicated_bots
                     if bot.slack_url.strip("/").lower().replace("http://", "https://") ==
                     slack_url.replace("http://", "https://") and not bot.invalid_creds]), None)

    if not bot:
        return None

    utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    cred_date_time = bot.created_at.replace(tzinfo=pytz.UTC)

    if update_expired and (utc_now - cred_date_time).days > 7:
        login_response = SlackWebClient.get_access_token(bot.slack_url, bot.user_name, bot.password)
        if login_response:
            bot.token = login_response.token
            bot.cookies = login_response.cookies
            bot.updated_at = datetime.utcnow()
            DedicatedBotRepository().add_or_update(bot)

    return SlackCredentialsResponse(
        token=bot.token,
        slack_url=bot.slack_url,
        user_name=bot.user_name,
        password=bot.password,
        updated_at=bot.updated_at,
        invalid_creds=False,
        cookies=bot.cookies,
    )


def get_file_url(blob_path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(SlackFilesClient.bucket_name)
    blob = bucket.get_blob(blob_path)
    if not blob:
        return None
    # valid for 3 days
    return blob.generate_signed_url(timedelta(3))


def __get_dedicated_bot_credentials_for_personal_lead(user: UserModel,
                                                      lead: LeadModel,
                                                      update_expired=True,
                                                      dedicated_bots=None) -> Optional[SlackCredentialsResponse]:
    if not dedicated_bots:
        dedicated_bots = DedicatedBotRepository().get_user_bots(str(user.id))
    bot = next(iter([bot for bot in dedicated_bots
                     if bot.name == lead.message.name and not bot.invalid_creds]), None)
    if not bot:
        return None

    uctnow = datetime.utcnow().replace(tzinfo=pytz.UTC)
    cred_date_time = bot.created_at.replace(tzinfo=pytz.UTC)
    if update_expired and (uctnow - cred_date_time).days > 7:
        login_response = SlackWebClient.get_access_token(bot.slack_url, bot.user_name, bot.password)
        if login_response:
            bot.token = login_response.token
            bot.cookies = login_response.cookies
            bot.updated_at = datetime.utcnow()
            DedicatedBotRepository().add_or_update(bot)

    return SlackCredentialsResponse(
        token=bot.token,
        slack_url=bot.slack_url,
        user_name=bot.user_name,
        password=bot.password,
        updated_at=bot.updated_at,
        invalid_creds=False,
        cookies=bot.cookies,
    )


class SlackMessageConvertService:
    @staticmethod
    def from_slack_response(user_email, bot_name, bot_token, dic, cookies=None):

        """
        :rtype: SlackHistoryMessageModel
        """
        result = SlackHistoryMessageModel()
        result.text = dic.get('text', '')
        result.type = dic.get('type', '')
        result.user = dic.get('user', '')
        result.ts = dic.get('ts', '')
        result.attachments = dic.get('attachments', [])
        result.files = []

        if 'files' in dic:
            for file in dic.get('files'):
                if file.get('mode', '') == "tombstone":
                    continue
                new_file = SlackHistoryMessageModel.SlackFileModel()
                new_file.id = file.get('id')
                new_file.name = file.get('name')
                new_file.title = file.get('title')
                new_file.filetype = file.get('filetype')
                new_file.size = file.get('size')
                new_file.mimetype = file.get('mimetype')

                url_private_download = file.get('url_private_download')
                new_file.download_url = SlackFilesClient.get_file_url(user_email, bot_name, bot_token,
                                                                      new_file.id, url_private_download,
                                                                      new_file.mimetype, cookies)
                result.files.append(new_file)

        js_ticks = int(result.ts.split('.')[0] + result.ts.split('.')[1][3:])
        result.created_at = datetime.fromtimestamp(js_ticks / 1000.0)
        return result


class SlackFilesClient:
    bucket_name = 'lgt_service_file'

    # Consider to cache these file somewhere in the super-fast cache solution
    @staticmethod
    def get_file_url(user_email, bot_name, bot_token, file_id, url_private_download, mimetype, cookies=None):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(SlackFilesClient.bucket_name)
        blob_path = f'slack_files/{user_email}/{bot_name}/{file_id}'
        blob = bucket.get_blob(blob_path)

        if not blob:
            res = requests.get(url_private_download, headers={'Authorization': f'Bearer {bot_token}'}, cookies=cookies)
            if res.status_code != 200:
                raise Exception(
                    f'Failed to download file: {url_private_download} from slack due to response: '
                    f'Code: {res.status_code} Error: {res.content}')
            blob = bucket.blob(blob_path)
            blob.upload_from_string(res.content, content_type=mimetype)

        blob = bucket.get_blob(blob_path)
        # valid for 3 days
        return blob.generate_signed_url(timedelta(3))


class SlackWebClient:
    def __init__(self, token, cookies=None):

        if isinstance(cookies, list):
            cookies = {c['name']: c['value'] for c in cookies}

        self.client = SlackClient(token, cookies)

    def delete_message(self, channel: str, ts: str):
        return self.client.delete_message(channel, ts)

    def update_message(self, channel: str, ts: str, text: str, file_ids=''):
        return self.client.update_message(channel, ts, text, file_ids)

    def get_profile(self, user_id):
        return self.client.user_info(user_id)

    def get_im_list(self):
        return self.client.get_im_list()

    def chat_history(self, channel):
        return self.client.conversations_history(channel)

    def post_message(self, to, text):
        return self.client.post_message(to, text)

    def user_list(self):
        return self.client.users_list()

    def channels_list(self):
        return self.client.get_conversations_list()

    def im_open(self, sender_id):
        return self.client.im_open(sender_id)

    def update_profile(self, profile):
        return self.client.update_profile(profile)

    def channel_join(self, channels):
        return self.client.join_channels(channels)

    def channel_leave(self, channels):
        return self.client.leave_channels(channels)

    def get_reactions(self, channel, ts):
        return self.client.get_reactions(channel, ts)

    def upload_file(self, file, file_name):
        return self.client.upload_file(file, file_name)

    def download_file(self, file_url):
        return self.client.download_file(file_url)

    def delete_file(self, file_id):
        return self.client.delete_file(file_id)

    def share_files(self, files_ids: list, channel: str, text: str = None) -> dict:
        return self.client.share_files(files_ids, channel, text)

    def check_email(self, email: str, user_agent: str) -> bool:
        return self.client.check_email(email, user_agent)

    def confirm_email(self, email: str, user_agent: str, locale: str = 'en-US') -> bool:
        return self.client.confirm_email(email, user_agent, locale)

    def confirm_code(self, email: str, code: str, user_agent: str, ) -> requests.Response:
        return self.client.confirm_code(email, code, user_agent)

    def find_workspaces(self, user_agent: str, ) -> requests.Response:
        return self.client.find_workspaces(user_agent)

    def conversation_replies(self, channel: str, ts: str) -> dict:
        return self.client.conversations_replies(channel, ts)

    def create_shared_invite(self):
        return self.client.create_shared_invite()

    @staticmethod
    def get_access_token_v2(workspace_url, user_name, password, retry=False) -> LoginResponseV2:
        try:
            session = requests.Session()
            resp = session.post(f'{slack_login_url}api/login',
                                json={"slack_workspace": workspace_url, "user_name": user_name, "password": password})

            resp_json = resp.json()
            if resp.status_code == 400:
                # this means invalid credentials
                return LoginResponseV2('', None, resp_json.get('error', None), resp_json.get('image', None))

            if resp.status_code != 200:
                if not retry:
                    print(
                        f'[{workspace_url}] received {resp.status_code} from the slack login component. trying one '
                        f'more time')
                    return SlackWebClient.get_access_token_v2(workspace_url, user_name, password, True)

                return LoginResponseV2("", "", resp_json.get('error', None), resp_json.get('image', None))

            resp_json = resp.json()
            if 'token' not in resp_json:
                return LoginResponseV2("", "", resp_json.get('error', None), resp_json.get('image', ""))

            return LoginResponseV2(resp_json['token'], resp_json['cookies'], "", "")
        except requests.exceptions.ConnectionError:
            print('Connection error')
            raise

    @staticmethod
    def get_access_token(workspace_url, user_name, password, retry=False) -> LoginResponse:
        try:
            session = requests.Session()
            resp = session.post(f'{slack_login_url}',
                                json={"slack_workspace": workspace_url, "user_name": user_name, "password": password})

            if resp.status_code == 400:
                # this means invalid credentials
                return None

            if resp.status_code != 200:
                if not retry:
                    print(
                        f'[{workspace_url}] received {resp.status_code} from the slack login component. trying one '
                        f'more time')
                    return SlackWebClient.get_access_token(workspace_url, user_name, password, True)

                return None

            resp_json = resp.json()
            if 'token' not in resp_json:
                return None

            return LoginResponse(resp_json['token'], resp_json['cookies'])
        except requests.exceptions.ConnectionError:
            print('Connection error')
            raise
