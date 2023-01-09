from __future__ import annotations

import os
from datetime import datetime
from mongoengine import connect, Document, DateTimeField, StringField, IntField, ObjectIdField, ListField, DictField
from typing import Dict, Tuple
from .mongo_repository import to_object_id, UserMongoRepository

connect(host=os.environ.get('MONGO_CONNECTION_STRING', 'mongodb://127.0.0.1:27017/'), db="lgt_admin", alias="lgt_admin")
connect(host=os.environ.get('MONGO_CONNECTION_STRING', 'mongodb://127.0.0.1:27017/'), db="lgt_leads", alias="lgt_leads")


class GlobalUserConfiguration(Document):
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)
    created_by = ObjectIdField(required=False)
    updated_by = ObjectIdField(required=False)
    dedicated_bots_days_to_remove = IntField(required=True)

    meta = {"db_alias": "lgt_admin"}

    @staticmethod
    def get_config() -> GlobalUserConfiguration:
        items = list(GlobalUserConfiguration.objects())
        if not items:
            # create default config
            GlobalUserConfiguration(
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                dedicated_bots_days_to_remove=10
            ).save()
            items = list(GlobalUserConfiguration.objects())
        return items[-1]


class UserTrackAction(Document):
    user_id = ObjectIdField(required=True)
    action = StringField(required=True)
    metadata = StringField(required=False)
    created_at = DateTimeField(required=True)
    meta = {"indexes": ["user_id"], "db_alias": "lgt_admin"}

    @staticmethod
    def get_aggregated() -> Dict[str, Tuple[datetime, datetime]]:
        pipeline = [
            {
                "$group": {
                    "_id": "$user_id",
                    "last_action_at": {"$max": "$created_at"},
                    "first_action_at": {"$min": "$created_at"}
                }
            }]

        result = list(UserTrackAction.objects.aggregate(*pipeline))

        return {str(item.get("_id")): (item["first_action_at"], item["last_action_at"]) for item in result}

    @staticmethod
    def get_ws_monitoring_logs(email: str, action_subtype: str, from_date: datetime, to_date: datetime,
                               workspace=None) -> list[UserTrackAction]:

        pipeline = {'action': {'$regex': f"^monitoring.*{action_subtype}$"}}

        if email:
            user = UserMongoRepository().get_by_email(email)
            pipeline['user_id'] = to_object_id(user.id)

        if from_date:
            start = datetime(from_date.year, from_date.month, from_date.day)
            pipeline['created_at__gte'] = start

        if to_date:
            end = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59)
            pipeline['created_at__lte'] = end

        if workspace:
            pipeline['metadata'] = {'$regex': f"^{workspace}:"}

        return list(UserTrackAction.objects(**pipeline))

    @staticmethod
    def get_daily_user_actions(user_id: str = None, from_date: datetime = None, to_date: datetime = None) -> \
            Dict[str, Dict[str, Dict[str, int]]]:
        pipeline = [
            {
                '$match': {
                    'action': {
                        '$regex': '^monitoring.*(?:(channel|workspace))$'
                    }
                }
            },
            {
                '$group': {
                    '_id': {
                        'date': {
                            '$dateFromParts': {
                                'day': {
                                    '$dayOfMonth': '$created_at'
                                },
                                'month': {
                                    '$month': '$created_at'
                                },
                                'year': {
                                    '$year': '$created_at'
                                }
                            }
                        },
                        'action': '$action',
                        'user_id': '$user_id'
                    },
                    'count': {
                        '$sum': 1
                    }
                }
            }
        ]

        if user_id:
            pipeline.insert(0, {"$match": {"user_id": to_object_id(user_id)}})

        if from_date:
            beginning_of_the_day = datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
            pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

        if to_date:
            end_of_the_day = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
            pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

        analytics = list(UserTrackAction.objects.aggregate(*pipeline))

        result = {}
        for item in analytics:
            date = item["_id"]["date"].strftime('%Y-%m-%d')
            user_id = str(item["_id"]["user_id"])

            if date not in result:
                result[date] = {}
            if user_id not in result[date]:
                result[date][user_id] = {}

            result[date][user_id][item["_id"]["action"]] = item["count"]

        return result


class DelayedJob(Document):
    created_at = DateTimeField(required=True)
    scheduled_at = DateTimeField(required=True)
    job_type = StringField(required=True)
    data = StringField(required=True)
    jib = StringField(required=True)
    executed_at: DateTimeField(required=False)

    meta = {"indexes": ["-scheduled_at", "jib"], "db_alias": "lgt_admin"}


class UserCreditStatementDocument(Document):
    meta = {"indexes": [("user_id", "created_at"),
                        ("user_id", "created_at", "action")], "db_alias": "lgt_leads"}

    user_id = ObjectIdField(required=True)
    created_at = DateTimeField(required=True)
    balance = IntField(required=True)
    action = StringField(required=True)
    lead_id = StringField(required=False)
    attributes = ListField(field=StringField(), required=False)


class UserFeedLead(Document):
    meta = {"indexes": ["user_id", "created_at", ("user_id", "created_at")],
            "db_alias": "lgt_leads"}
    user_id = ObjectIdField(required=True)
    lead_id = StringField(required=True)
    text = StringField(required=True)
    created_at = DateTimeField(required=True)
    full_message_text = StringField(required=True)


class LeadChat(Document):
    meta = {"indexes": ["sender_id", "user_id", ("sender_id", "user_id")],
            "db_alias": "lgt_admin"}
    created_at = DateTimeField(required=True)
    sender_id = StringField(required=True)
    workspace = StringField(required=True)
    user_id = ObjectIdField(required=True)
    chat_history = ListField(field=DictField(), required=True)

    @staticmethod
    def create_or_update(sender_id: str, user_id: str, workspace: str, chat_history: list) -> LeadChat:
        lead_chat = LeadChat.objects(sender_id=sender_id,
                                     user_id=to_object_id(user_id)).update_one(set__workspace=workspace,
                                                                               set__created_at=datetime.utcnow(),
                                                                               set__chat_history=chat_history,
                                                                               upsert=True)

        return lead_chat
