from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, Extra


class DedicatedSlackOptions(BaseModel, extra=Extra.ignore):
    user_id: str
    bot_id: str
    token: str
    workspace: str
    cookies: List[dict]


class SlackMessageProfile(BaseModel, extra=Extra.ignore):
    display_name: Optional[str]
    real_name: Optional[str]
    email: Optional[str]
    skype: Optional[str]
    title: Optional[str]
    phone: Optional[str]
    images: Optional[Dict[str, str]]


class SlackChannelInfo(BaseModel, extra=Extra.ignore):
    id: str
    name: str
    num_members: Optional[int]
    is_general: bool
    is_archived: bool
    name_normalized: str
    created: int


class SlackTimeZone(BaseModel, extra=Extra.ignore):
    tz: str
    tz_label: str
    tz_offset: int


class SlackMessageOptions(BaseModel, extra=Extra.ignore):
    token: str
    ts: str
    country: str
    registration_link: str
    workspace: str
    timezone: SlackTimeZone
    profile: Optional[SlackMessageProfile]
    channel: Optional[SlackChannelInfo]
    cookies: List[dict]


class TelegramProfile(BaseModel, extra=Extra.ignore):
    id: int
    first_name: str
    last_name: str
    username: str
    phone_number: str


class TelegramOptions(BaseModel, extra=Extra.ignore):
    profile: Optional[TelegramProfile]


class AggregatorMessage(BaseModel, extra=Extra.ignore):
    name: str
    message_id: str
    message: str
    channel_id: str
    sender_id: str
    time_stamp: str
    source: str
    created_at: datetime

    telegram_options: Optional[TelegramOptions]
    slack_options: Optional[SlackMessageOptions]
    dedicated_slack_options: Optional[DedicatedSlackOptions]
    profile: Optional[SlackMessageProfile]
