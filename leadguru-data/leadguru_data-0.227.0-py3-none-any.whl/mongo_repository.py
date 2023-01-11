import os
import re
from typing import List, Optional

import pymongo
from dateutil import tz
from pymongo import MongoClient
from bson.objectid import ObjectId
from .model import LeadModel, BaseModel, UserLeadModel, UserModel, UserBotCredentialsModel, UserLeadStatusModel, \
    UserResetPasswordModel, AuthorAttributesModel, BotModel, BoardModel, BoardedStatus, Contact, DedicatedBotModel, \
    SlackUserPresenceModel, SlackMemberInformation, UserTemplateModel, LinkedinContact
from datetime import datetime
from collections import OrderedDict
from nameparser import HumanName

client = MongoClient(os.environ.get('MONGO_CONNECTION_STRING', 'mongodb://127.0.0.1:27017/'))


def to_object_id(oid):
    if isinstance(oid, ObjectId):
        return oid
    return ObjectId(oid)


class BaseMongoRepository:
    collection_name = ''
    database_name = 'lgt_admin'
    model: BaseModel = BaseModel()

    def collection(self):
        return client[self.database_name][self.collection_name]

    def _collection(self, collection_name):
        return client[self.database_name][collection_name]

    def insert_many(self, items):
        insert_items = map(lambda x: x.to_dic(), items)
        self.collection().insert_many(insert_items)

    def insert(self, item: BaseModel):
        return self.collection().insert_one(item.to_dic())

    def add(self, item: BaseModel):
        return self.insert(item)

    def delete(self, id):
        res = self.collection().delete_one({'_id': to_object_id(id)})
        return res


class BotMongoRepository(BaseMongoRepository):
    pass

    collection_name = 'bots'
    model = BotModel

    def get_by_id(self, name):
        return BotModel.from_dic(self.collection().find_one({'name': name}))

    def add_or_update(self, bot: BotModel):
        self.collection().update_one({'name': bot.name}, {'$set': bot.to_dic()}, upsert=True)

    def get(self) -> [BotModel]:
        docs = self.collection().find({})
        result = list()

        for doc in docs:
            result.append(BotModel.from_dic(doc))

        return result

    def delete(self, name: str):
        self.collection().delete_many({'name': name})


class UserLeadStatusMongoRepository(BaseMongoRepository):
    collection_name = 'user_lead_statuses'
    model = UserLeadStatusModel

    def update_lead_status(self, user_id, status_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id), '_id': to_object_id(status_id)}

        doc = UserLeadStatusModel.from_dic(self.collection().find_one(pipeline))
        if not doc:
            return None

        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_one(pipeline, {'$set': update_dict})

        if kwargs.get('name', None):
            self._collection('user_leads') \
                .update_many({'user_id': to_object_id(user_id), 'status': doc.name},
                             {'$set': {'status': kwargs.get('name')}})

        return UserLeadStatusModel.from_dic(self.collection().find_one(pipeline))

    def update_status_order(self, user_id, status_ids: [str]):
        status_ids = list(map(lambda x: to_object_id(x), status_ids))
        pipeline = {'user_id': to_object_id(user_id), '_id': {'$in': status_ids}}
        docs = list(map(lambda x: UserLeadStatusModel.from_dic(x), self.collection().find(pipeline)))

        order = 0
        for status_id in status_ids:
            for doc in docs:
                if doc.id == status_id:
                    self.collection().update_one({'user_id': to_object_id(user_id), '_id': status_id},
                                                 {'$set': {'order': order}}, upsert=False)
                    order = order + 1

    def add_default_lead_statuses(self, user_id):
        self.collection().insert_one({'name': 'Draft', 'order': 0, 'user_id': to_object_id(user_id)})
        self.collection().insert_one({'name': 'In Progress', 'order': 1, 'user_id': to_object_id(user_id)})
        self.collection().insert_one({'name': 'Done', 'order': 2, 'user_id': to_object_id(user_id)})

    def add_lead_status(self, user_id, status: UserLeadStatusModel) -> UserLeadStatusModel:
        status.user_id = user_id
        self.collection().insert_one(status.to_dic())

        return UserLeadStatusModel.from_dic(
            self.collection().find_one({'user_id': to_object_id(user_id), 'name': status.name}))

    def delete_lead_status(self, user_id, lead_status_id):
        self.collection().delete_many({'user_id': to_object_id(user_id), '_id': to_object_id(lead_status_id)})

    def get_lead_statuses(self, user_id):
        """

        :rtype: [UserLeadStatusModel]
        """
        result = map(lambda x: UserLeadStatusModel.from_dic(x),
                     self.collection().find({'user_id': to_object_id(user_id)}))
        return list(result)


class UserMongoRepository(BaseMongoRepository):
    collection_name = 'users'
    model = UserModel

    def get(self, _id):
        doc = self.collection().find_one({'_id': to_object_id(_id)})

        if doc:
            return UserModel.from_dic(doc)

        return None

    def get_by_email(self, email: str):
        """

        :param email:
        :return UserModel:
        """

        pipeline = {'email': email}
        doc = self.collection().find_one(pipeline)

        if doc:
            return UserModel.from_dic(doc)

        return None

    def set(self, id, **kwargs):
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_one({'_id': to_object_id(id)}, {'$set': update_dict})

    def inc(self, _id, **kwargs):
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update({'_id': to_object_id(_id)}, {'$inc': update_dict})

    def set_by_email(self, email, **kwargs):
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_one({'email': email}, {'$set': update_dict}, upsert=False)

    def get_users(self, users_ids=None, include_inactive=False):
        pipeline = {}

        if users_ids is not None:
            pipeline['_id'] = {'$in': [to_object_id(id) for id in users_ids]}

        if not include_inactive:
            pipeline['inactive'] = False

        return [UserModel.from_dic(doc) for doc in self.collection().find(pipeline)]


class UserBotCredentialsMongoRepository(BaseMongoRepository):
    collection_name = 'user_bots'
    model = UserBotCredentialsModel

    def set(self, user_id, bot_name, **kwargs):
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_many({'user_id': to_object_id(user_id), 'bot_name': bot_name}, {'$set': update_dict})

    def delete_bot_credentials(self, user_id, bot_name):
        self.collection().delete_many({'user_id': to_object_id(user_id), 'bot_name': bot_name})

    def get_by_creds(self, user_id, bot_name):
        return UserBotCredentialsModel.from_dic(
            self.collection().find_one({'user_id': to_object_id(user_id), 'bot_name': bot_name}))

    def get_bot_credentials(self, user_id):
        pipeline = {'user_id': to_object_id(user_id)}
        return list(
            map(lambda x: UserBotCredentialsModel.from_dic(x), self.collection().find(pipeline).sort([('amp', 1)])))

    def get_active_bots(self, bot_name: str):
        pipeline = {'bot_name': bot_name, "$or": [
            {"invalid_creds": False},
            {"invalid_creds": None},
            {"invalid_creds": {"$exists": False}}]}

        return list(
            map(lambda x: UserBotCredentialsModel.from_dic(x), self.collection().find(pipeline).sort([('amp', 1)])))

    def update_bot_creadentials(self, user_id, bot_name, user_name,
                                password, slack_url, token, cookies, invalid_creds=False) -> UserBotCredentialsModel:
        model = UserBotCredentialsModel()
        model.bot_name = bot_name
        model.user_name = user_name
        model.password = password
        model.slack_url = slack_url
        model.token = token
        model.updated_at = datetime.utcnow(),
        model.user_id = user_id
        model.cookies = cookies
        model.invalid_creds = invalid_creds

        pipeline = {'user_id': to_object_id(user_id), 'bot_name': bot_name}
        set = {'$set': {
            'bot_name': bot_name,
            'user_name': user_name,
            'password': password,
            'updated_at': datetime.utcnow(),
            'user_id': to_object_id(user_id),
            'slack_url': slack_url,
            'token': token,
            'cookies': cookies
        }}

        self.collection().update_one(pipeline, set, upsert=True)
        return UserBotCredentialsModel.from_dic(set['$set'])


class UserLeadMongoRepository(BaseMongoRepository):
    collection_name = 'user_leads'
    model = UserLeadModel

    def get_count(self, user_id, **kwargs):
        pipeline = self.__create_leads_filter(user_id, **kwargs)
        return self.collection().count(pipeline)

    def get_many(self, ids: list, user_id):
        docs = self.collection().find({"id": {'$in': ids}, 'user_id': to_object_id(user_id)})
        if not docs:
            return None
        return [LeadModel.from_dic(lead) for lead in docs]

    def get_leads(self, user_id, skip: int, limit: int, **kwargs) -> [UserLeadModel]:
        pipeline = self.__create_leads_filter(user_id, **kwargs)

        sort_field = kwargs.get('sort_field', 'last_action_at')
        sort_direction = kwargs.get('sort_direction', 'ASCENDING')
        sort_direction = pymongo.ASCENDING if sort_direction == 'ASCENDING' else pymongo.DESCENDING

        # if unread_messaged_only:
        #     pipeline['$where'] = "this.last_message_at " \
        #                          "&& this.chat_history " \
        #                          "&& this.chat_history.length " \
        #                          "&& this.chat_viewed_at < this.last_message_at"

        docs = list(self.collection().find(pipeline).sort([(sort_field, sort_direction)]).skip(skip).limit(limit))
        return [UserLeadModel.from_dic(x) for x in docs]

    def __create_leads_filter(self, user_id, **kwargs):
        pipeline = {'user_id': to_object_id(user_id)}

        if kwargs.get('status') is not None:
            pipeline['status'] = kwargs.get('status', '')

        if kwargs.get('board_id'):
            pipeline['board_id'] = to_object_id(kwargs.get('board_id'))
        elif kwargs.get('board_id') is not None:
            pipeline['$or'] = [{'board_id': ''}, {'board_id': None}]

        archived = kwargs.get('archived')
        from_date = kwargs.get('from_date')
        to_date = kwargs.get('to_date')
        has_followup = kwargs.get('has_followup', None)
        followup_to = kwargs.get('followup_to_date', None)
        followup_from = kwargs.get('followup_from_date', None)
        unread_messaged_only = kwargs.get('unread_messaged_only', False)
        sender_ids = kwargs.get('sender_ids', None)
        text = kwargs.get('text', None)
        stop_words = kwargs.get('stop_words', None)
        tags = kwargs.get('tags', None)
        config = kwargs.get('config', None)
        bots_names = kwargs.get('bots_names', None)
        locations = kwargs.get('locations', None)
        dedicated_bots_ids = kwargs.get('dedicated_bots_ids', None)
        with_chat = kwargs.get('with_chat', None)
        leads_ids = kwargs.get('leads_ids', None)

        pipeline['message.profile.display_name'] = {
            "$ne": "Slackbot"
        }

        if leads_ids is not None:
            pipeline["id"] = {'$in': leads_ids}

        if archived is not None:
            pipeline['archived'] = archived

        if with_chat is not None:
            pipeline['chat_history'] = {'$exists': True, '$ne': []}

        if has_followup is not None:
            pipeline['followup_date'] = {'$ne': None} if has_followup else {'$eq': None}

        if from_date or to_date:
            pipeline['last_action_at'] = {}

        if from_date:
            start = datetime(from_date.year, from_date.month, from_date.day, tzinfo=tz.tzutc())
            pipeline['last_action_at']['$gte'] = start

        if to_date:
            end = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, tzinfo=tz.tzutc())
            pipeline['last_action_at']['$lte'] = end

        if locations and len(locations) > 0:
            pipeline['message.locations'] = {"$in": locations}

        if sender_ids is not None:
            pipeline['message.sender_id'] = {'$in': sender_ids}

        if followup_from or followup_to:
            pipeline['followup_date'] = {}

        if followup_from:
            followup_from = datetime(followup_from.year, followup_from.month, followup_from.day, tzinfo=tz.tzutc())
            pipeline['followup_date']['$gte'] = followup_from

        if followup_to:
            followup_to = datetime(followup_to.year, followup_to.month, followup_to.day, 23, 59, 59, tzinfo=tz.tzutc())
            pipeline['followup_date']['$lte'] = followup_to

        if stop_words:
            pipeline['full_message_text'] = {'$regex': f'^(?!.*({stop_words})).*$', '$options': 'i'}
        elif text:
            pipeline['$text'] = {'$search': text}

        if tags:
            pipeline["tags"] = {"$elemMatch": {"$in": tags}}

        if config:
            pipeline["message.configs"] = {"$elemMatch": {"$all": [f'{config}']}}

        if bots_names is not None:
            pipeline['message.name'] = {'$in': bots_names}

        if dedicated_bots_ids is not None:
            pipeline["message.dedicated_slack_options.bot_id"] = {"$in": dedicated_bots_ids}

        return pipeline

    def get_aggregated_leads(self, user_id, from_date, to_date=None):
        pipeline = [
            {
                '$match': {
                    'user_id': to_object_id(user_id),
                    'created_at': {'$gte': from_date}
                }
            }, {
                '$group': {
                    '_id': {
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
                    'count': {
                        '$sum': 1
                    },
                    'leads': {
                        '$push': {
                            'id': '$id',
                            'created_at': '$created_at'
                        }
                    }
                }
            }, {
                '$sort': {
                    '_id': 1
                }
            }
        ]

        if to_date:
            end = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, tzinfo=tz.tzutc())
            pipeline[0]["$match"]["created_at"]['$lte'] = end

        return list(self.collection().aggregate(pipeline))

    def get_unanswered_leads_ids(self, user_id: str, from_date=None):
        pipeline = [
            {
                '$match':
                    {
                        'user_id': to_object_id(user_id)
                    }
            },
            {
                '$match':
                    {
                        'chat_history': {'$exists': True, '$not': {'$size': 0}}
                    }
            },
            {
                '$project':
                    {
                        'id': 1,
                        'sender_id': "$message.sender_id",
                        'last_message': {'$arrayElemAt': ['$chat_history', 0]}
                    }
            },
            {
                '$addFields':
                    {
                        'is_user_message': {'$ne': ['$sender_id', '$last_message.user']}
                    }
            },
            {
                '$match':
                    {
                        '$and':
                            [
                                {'last_message.text': {'$regex': '\\?'}},
                                {'is_user_message': False}
                            ]
                    }
            }
        ]

        if from_date:
            beginning_of_the_day = datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
            pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

        data = list(self.collection().aggregate(pipeline))
        leads_ids = [item['id'] for item in data]
        return leads_ids

    def get_daily_analytics_by_workspace(self, workspace: str = None,
                                         from_date: datetime = None,
                                         to_date: datetime = None,
                                         user_id: str = None,
                                         dedicated_only: bool = False):
        pipeline = [
            {
                '$project': {
                    'created_at': {
                        '$dateToString': {
                            'format': '%Y-%m-%d',
                            'date': '$created_at'
                        }
                    },
                    'id': '$id'
                }
            },
            {
                '$group': {
                    '_id': '$created_at',
                    'data': {'$push': '$id'}
                }
            },
            {
                '$sort': {'_id': 1}
            }
        ]

        if workspace:
            pipeline.insert(0, {"$match": {"message.name": workspace}})

        if from_date:
            beginning_of_the_day = datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
            pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

        if to_date:
            end_of_the_day = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
            pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

        if user_id:
            pipeline.insert(0, {"$match": {'user_id': user_id}})

        if dedicated_only:
            pipeline.insert(0, {"$match": {'message.dedicated_slack_options': {'$exists': True, '$ne': None}}})

        saved_messages = list(self.collection().aggregate(pipeline))
        saved_messages_dic = OrderedDict()

        for item in saved_messages:
            saved_messages_dic[item["_id"]] = item["data"]

        return saved_messages_dic

    def get_leads_after(self, created_after: datetime) -> [UserLeadModel]:
        docs = self.collection().find({'created_at': {'$gte': created_after}})
        return map(lambda x: UserLeadModel.from_dic(x), docs)

    def add_lead(self, user_id, lead: UserLeadModel) -> None:
        if not lead.created_at:
            lead.created_at = datetime.utcnow()

        if hasattr(lead, "_id"):
            lead._id = ObjectId()

        lead.user_id = user_id
        self.insert(lead)

    def update_lead(self, user_id, route_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id), 'id': route_id}
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        if 'board_id' in update_dict:
            update_dict['board_id'] = to_object_id(update_dict['board_id']) if len(update_dict['board_id']) == 24 \
                else update_dict['board_id']
        self.collection().update_one(pipeline, {'$set': update_dict})

        return UserLeadModel.from_dic(self.collection().find_one(pipeline))

    def update_same_leads(self, user_id, sender_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id), 'message.sender_id': sender_id}
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_many(pipeline, {'$set': update_dict})

    def update_leads_order(self, user_id, lead_ids: [str]):
        pipeline = {'user_id': to_object_id(user_id), 'id': {'$in': lead_ids}}
        docs = list(self.collection().find(pipeline))

        order = 0
        for lead_id in lead_ids:
            for doc in docs:
                if doc['id'] == lead_id:
                    self.collection().update_one({'id': lead_id}, {'$set': {'order': order}}, upsert=False)
                    order = order + 1

    def delete_lead(self, user_id, lead_id: str):
        """

        :param user_id:
        :param lead_id:
        :return: UserLeadModel
        """

        pipeline = {'user_id': to_object_id(user_id), 'id': lead_id}
        self.collection().delete_one(pipeline)

    def get_lead(self, user_id, message_id: str = None, lead_id: str = None):
        """

        :param user_id:
        :param message_id:
        :param lead_id:
        :return: UserLeadModel
        """

        pipeline = {'user_id': to_object_id(user_id)}
        if message_id:
            pipeline['message_id'] = message_id

        if lead_id:
            pipeline['id'] = lead_id

        return UserLeadModel.from_dic(self.collection().find_one(pipeline))


class UserResetPasswordMongoRepository(BaseMongoRepository):
    pass

    collection_name = 'user_reset_passwords'
    model = UserResetPasswordModel

    def get(self, id):
        return UserResetPasswordModel.from_dic(self.collection().find_one({'_id': to_object_id(id)}))

    def delete(self, email):
        self.collection().delete_many({'email': email})

    def add(self, email) -> str:
        model = UserResetPasswordModel()
        model.email = email
        return self.collection().insert_one({'email': email}).inserted_id


class LeadMongoRepository(BaseMongoRepository):
    pass

    database_name = 'lgt_leads'
    collection_name = 'leads'
    model = LeadModel

    def delete(self, id):
        res = self.collection().delete_one({'id': id})
        return res

    def get(self, id):
        result = self.collection().find_one({"id": id})
        if not result:
            return None

        return LeadModel.from_dic(result)

    def get_many(self, ids: list):
        docs = self.collection().find({"id": {'$in': ids}})
        if not docs:
            return None
        return [LeadModel.from_dic(lead) for lead in docs]

    def get_by_sender_id(self, sender_id, exclude_leads: [str], skip: int, limit: int):
        pipeline = {'message.sender_id': sender_id, 'id': {'$nin': exclude_leads}}
        docs = self.collection().find(pipeline).sort([('created_at', pymongo.DESCENDING)]).skip(skip).limit(limit)

        return map(lambda x: LeadModel.from_dic(x), docs)

    def get_by_message_id(self, message_id):
        """

        :rtype: LeadModel
        :param message_id:
        """
        doc = self.collection().find_one({'message_id': message_id})
        if not doc:
            return None

        return LeadModel.from_dic(doc)

    def update(self, id: str, **kwargs):
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_one({'id': id}, {'$set': update_dict}, upsert=False)

    def get_count(self, **kwargs):
        pipeline = self.__create_leads_filter(**kwargs)
        return self.collection().count(pipeline)

    def get_list(self, skip, limit, **kwargs):
        pipeline = self.__create_leads_filter(**kwargs)

        sort_field = kwargs.get('sort_field', 'created_at')
        sort_direction = kwargs.get('sort_direction', 'ASCENDING')
        sort_direction = pymongo.ASCENDING if sort_direction == 'ASCENDING' else pymongo.DESCENDING

        docs = self.collection().find(pipeline).sort([(sort_field, sort_direction)]).skip(skip).limit(limit)
        return map(lambda x: LeadModel.from_dic(x), docs)

    def __create_leads_filter(self, **kwargs):
        pipeline = {"hidden": False}

        from_date: datetime = kwargs.get('from_date')
        to_date: datetime = kwargs.get('to_date')

        country = kwargs.get('country', None)
        user_id = kwargs.get('user_id', None)
        tags = kwargs.get('tags', None)
        text = kwargs.get('text', None)
        stop_words = kwargs.get('stop_words', None)
        exclude_leads = kwargs.get('exclude_leads', None)
        exclude_senders = kwargs.get('exclude_senders', None)
        excluded_channels = kwargs.get('excluded_channels', None)
        sender_ids = kwargs.get('sender_ids', None)
        config = kwargs.get('config', None)
        bots_names = kwargs.get('bots_names', None)
        locations = kwargs.get('locations', None)

        pipeline['message.profile.display_name'] = {
            "$ne": "Slackbot"
        }

        if from_date or to_date:
            pipeline['created_at'] = {}

        if from_date:
            start = from_date.astimezone(tz.tzutc())
            pipeline['created_at']['$gte'] = start

        if to_date:
            end = to_date.astimezone(tz.tzutc())
            pipeline['created_at']['$lte'] = end

        if locations and len(locations) > 0:
            pipeline['message.locations'] = {"$in": locations}

        if country:
            pipeline["message.slack_options.country"] = re.compile(country, re.IGNORECASE)

        if user_id:
            pipeline["$or"] = [
                {"message.dedicated_slack_options": {"$exists": False}},
                {"message.dedicated_slack_options": None},
                {"message.dedicated_slack_options.user_id": f"{user_id}"},
            ]
        else:
            pipeline["user_id"] = {'$exists': False}

        if stop_words:
            pipeline['full_message_text'] = {'$regex': f'^(?!.*({stop_words})).*$', '$options': 'i'}
        elif text:
            pipeline['$text'] = {'$search': text}

        if tags:
            pipeline["tags"] = {"$elemMatch": {"$in": tags}}

        if exclude_leads:
            pipeline['id'] = {'$nin': exclude_leads}

        if exclude_senders:
            pipeline['message.sender_id'] = {'$nin': exclude_senders}

        if excluded_channels:
            pipeline['$and'] = []
            for ws, channels in excluded_channels.items():
                if channels is not None:
                    pipeline['$and'].append(
                        {'$or': [{'message.name': {'$ne': ws}}, {'message.channel_id': {'$nin': channels}}]})

        if sender_ids is not None:
            pipeline['message.sender_id'] = {'$in': sender_ids}

        if config:
            pipeline["message.configs"] = {"$not": {"$elemMatch": {"$nin": config}}}

        if bots_names is not None:
            pipeline['message.name'] = {'$in': bots_names}

        pipeline['message.profile.real_name'] = {'$ne': 'Slackbot'}

        return pipeline

    def get_per_day(self, date: datetime):
        start_day = datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=tz.tzutc())
        end_day = datetime(date.year, date.month, date.day, 23, 59, 59, tzinfo=tz.tzutc())
        docs = self.collection().find({'created_at': {'$gte': start_day, '$lte': end_day}}).sort('created_at', 1)
        return [LeadModel.from_dic(x) for x in docs]

    def get_senders(self, bot_name: str = None, dedicated_bot_id: str = None, limit: int = 500) -> [str]:
        pipeline = [
            {'$sort': {'created_at': -1}},
            {'$group': {'_id': '$message.sender_id'}},
            {'$limit': limit}
        ]

        senders = []
        if bot_name:
            pipeline.insert(0, {"$match": {"message.name": bot_name}})
        elif dedicated_bot_id:
            pipeline.insert(0, {"$match": {"message.dedicated_slack_options.bot_id": dedicated_bot_id}})
        else:
            return senders

        for doc in self.collection().aggregate(pipeline):
            senders.append(doc['_id'])

        return list(set(senders))


class SpamLeadsMongoRepository(LeadMongoRepository):
    pass

    def __init__(self):
        self.collection_name = 'leads_spam'
        self.database_name = 'lgt_leads'


class SpamUserLeadsMongoRepository(UserLeadMongoRepository):
    pass

    def __init__(self):
        self.collection_name = 'leads_spam'
        self.database_name = 'lgt_leads'


class GarbageLeadsMongoRepository(LeadMongoRepository):
    pass

    def __init__(self):
        self.collection_name = 'garbage_leads'
        self.database_name = 'lgt_leads'


class GarbageUserLeadsMongoRepository(UserLeadMongoRepository):
    pass

    def __init__(self):
        self.collection_name = 'garbage_leads'
        self.database_name = 'lgt_leads'


class AuthorAttributesMongoRepository(BaseMongoRepository):
    pass

    collection_name = 'author_attributes'
    model = AuthorAttributesModel

    def get_by_sender_id(self, sender_id):
        return AuthorAttributesModel.from_dic(self.collection().find_one({'sender_id': sender_id}))


class BoardsMongoRepository(BaseMongoRepository):
    pass

    collection_name = 'boards'
    model = BoardModel

    def create_board(self, user_id: str, name: str, **kwargs):
        is_primary = kwargs.get('is_primary', False)

        if is_primary:
            primary_board = self.collection().find_one({'user_id': to_object_id(user_id), 'is_primary': is_primary})
            if primary_board:
                return BoardModel.from_dic(primary_board)

        board = BoardModel()
        board.name = name
        board.created_at = datetime.utcnow()
        board.user_id = to_object_id(user_id)
        board.is_primary = is_primary
        self.collection().insert_one(BoardModel.to_dic(board))

        return BoardModel.from_dic(self.collection().find_one({'user_id': to_object_id(user_id), 'name': name}))

    def add_default_statuses(self, user_id: str, board_id: str):
        pipeline = {'user_id': to_object_id(user_id), '_id': to_object_id(board_id)}
        board = BoardModel.from_dic(self.collection().find_one(pipeline))

        if not board:
            return None

        board.statuses.append(BoardedStatus().from_dic({'name': 'Lead', 'order': 0}))
        board.statuses.append(BoardedStatus().from_dic({'name': 'Prospect', 'order': 1}))
        board.statuses.append(BoardedStatus().from_dic({'name': 'Opportunity', 'order': 2}))
        board.statuses.append(BoardedStatus().from_dic({'name': 'Call', 'order': 3}))
        board.statuses.append(BoardedStatus().from_dic({'name': 'Contract', 'order': 4}))
        board.statuses.append(BoardedStatus().from_dic({'name': 'Refused', 'order': 5}))

        return self.update_board(user_id, board_id, statuses=board.statuses)

    def get(self, user_id: str):
        docs = self.collection().find({'user_id': to_object_id(user_id)}).sort('created_at', 1)
        return map(lambda x: BoardModel.from_dic(x), docs)

    def get_primary(self, user_id: str):
        return BoardModel.from_dic(self.collection().find_one({'user_id': to_object_id(user_id), 'is_primary': True}))

    def get_by_id(self, id: str):
        return BoardModel.from_dic(self.collection().find_one({'_id': to_object_id(id)}))

    def delete_by_id(self, id: str):
        return self.collection().delete_many({'_id': to_object_id(id)})

    def update_board(self, user_id, board_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id), '_id': to_object_id(board_id)}

        if kwargs.get('statuses'):
            kwargs['statuses'] = [status.to_dic() for status in kwargs.get('statuses')
                                  if isinstance(status, BoardedStatus)]

        doc = BoardModel.from_dic(self.collection().find_one(pipeline))
        if not doc:
            return None

        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_one(pipeline, {'$set': update_dict})

        self._collection('user_leads').update_many({'user_id': to_object_id(user_id), 'board_id': to_object_id(doc.id)},
                                                   {'$set': {'board_id': to_object_id(board_id)}})

        return BoardModel.from_dic(self.collection().find_one(pipeline))


class ContactsMongoRepository(BaseMongoRepository):
    pass

    collection_name = 'contacts'

    def get_by_real_name(self, real_name):
        pipeline = {'real_name': real_name}

        docs = self.collection().find(pipeline).sort([('real_name', pymongo.ASCENDING)])
        return [Contact.from_dic(doc) for doc in docs]

    def get_by_name(self, human_name: HumanName):
        pipeline = {'last_name': human_name.last, 'real_name': {'$regex': f'^{human_name.full_name}$', '$options': 'i'}}

        doc = self.collection().find_one(pipeline)
        return Contact.from_dic(doc)


class DedicatedBotRepository(BaseMongoRepository):
    pass

    collection_name = 'dedicated_bots'

    def add_or_update(self, bot: DedicatedBotModel):
        self.collection().update_one({"name": bot.name, "user_id": to_object_id(bot.user_id)}, {'$set': bot.to_dic()},
                                     upsert=True)

    def get_all(self) -> List[DedicatedBotModel]:
        docs = self.collection().find({})
        return [DedicatedBotModel.from_dic(doc) for doc in docs]

    def get_by_user_and_name(self, user_id: str, name: str) -> Optional[DedicatedBotModel]:
        doc = self.collection().find_one({"user_id": ObjectId(f"{user_id}"), "name": f"{name}"})
        return DedicatedBotModel.from_dic(doc)

    def get_user_bots(self, user_id: str) -> List[DedicatedBotModel]:
        docs = self.collection().find({"user_id": ObjectId(f"{user_id}")})
        return [DedicatedBotModel.from_dic(doc) for doc in docs]

    def get_by_id(self, _id: str):
        doc = self.collection().find_one({"_id": to_object_id(f"{_id}")})
        return DedicatedBotModel.from_dic(doc)

    def delete(self, _id: str):
        self.collection().delete_many({'_id': to_object_id(f"{_id}")})


class SlackUserPresenceRepository(BaseMongoRepository):
    collection_name = "slack_user_presence"
    model = SlackUserPresenceModel

    def find(self, users: List[str] = None, bot_names: List[str] = None,
             bot_ids: List[str] = None, status: str = None, updated_from=None) -> List[SlackUserPresenceModel]:

        pipeline = {}
        if users:
            pipeline["user"] = {'$in': users}

        if bot_names:
            pipeline["bot_name"] = {'$in': bot_names}

        if bot_ids:
            pipeline["bot_id"] = {"$in": [to_object_id(bot_id) for bot_id in bot_ids]}

        if status:
            pipeline["status"] = f'{status}'

        if updated_from:
            pipeline['updated_at'] = {'$gte': updated_from}

        query = self.collection().find(pipeline).sort("updated_at", direction=pymongo.DESCENDING)
        return [SlackUserPresenceModel.from_dic(item) for item in query]

    def update(self, bot_name: Optional[str], bot_id: Optional[str], user: str, status: str):
        pipeline = {"user": user}
        if bot_name:
            pipeline["bot_name"] = bot_name

        if bot_id:
            pipeline["bot_id"] = to_object_id(bot_id)

        self.collection().update_one(pipeline, {'$set': {
            "user": user,
            "status": status,
            "updated_at": datetime.utcnow(),
            "bot_name": bot_name,
            "bot_id": to_object_id(bot_id) if bot_id else None
        }}, upsert=True)


class SlackContactUserRepository(BaseMongoRepository):
    collection_name = "slack_contact"
    model = SlackMemberInformation

    def find(self, text: Optional[str], skip: int = 0, limit: int = 1000, **kwargs):
        pipeline = {}
        if text:
            pipeline['$text'] = {'$search': text}

        pipeline = {**pipeline, **kwargs}

        docs = self.collection().find(pipeline).sort([("real_name", pymongo.ASCENDING)]) \
            .skip(skip) \
            .limit(limit)
        return [SlackMemberInformation.from_dic(doc) for doc in docs]

    def get_count_in_workspaces(self):
        pipeline = [
            {
                '$match': {
                    'user': {
                        '$ne': 'USLACKBOT'
                    }
                }
            }, {
                '$group': {
                    '_id': '$workspace',
                    'count': {
                        '$sum': 1
                    }
                }
            }
        ]
        docs = list(self.collection().aggregate(pipeline))
        return {doc['_id']: doc['count'] for doc in docs}


class UserTemplatesRepository(BaseMongoRepository):
    collection_name = "user_templates"
    model = UserTemplateModel

    def get_all(self, user_id: str):
        return [UserTemplateModel.from_dic(doc) for doc in self.collection().find({'user_id': to_object_id(user_id)})]

    def get(self, id: str):
        return UserTemplateModel.from_dic(self.collection().find_one({'_id': to_object_id(id)}))

    def create_or_update(self, template: UserTemplateModel):
        result = self.collection().update_one(
            {"_id": to_object_id(template.id)},
            {'$set': template.to_dic()},
            upsert=True)

        if result.upserted_id:
            template.id = result.upserted_id

        return template

    def delete_by_id(self, id: str):
        return self.collection().find_one_and_delete({'_id': to_object_id(id)})


class LinkedinContactRepository(BaseMongoRepository):
    collection_name = "linkedin_contact"
    model = LinkedinContact

    def find(self, **kwargs):
        docs = self.collection().find({**kwargs})
        return [LinkedinContact.from_dic(doc) for doc in docs]
