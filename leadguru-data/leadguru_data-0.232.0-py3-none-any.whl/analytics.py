import datetime
import os
from typing import Optional, List, Dict

from collections import OrderedDict
from dateutil import tz
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient(os.environ.get('MONGO_CONNECTION_STRING', 'mongodb://mongo.default:27017/'))
db = client.lgt_analytics


def _build_date_aggregated_analytics_pipeline(name=None,
                                              started_at: datetime.datetime = None,
                                              ended_at: datetime.datetime = None,
                                              dedicated_bots_ids: [str] = None):
    pipeline = [
        {
            "$sort": {"created_at": 1}
        },
        {
            "$project": {
                "created_at": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}},
                "name": "$name"
            }
        },
        {
            "$group":
                {
                    "_id": "$created_at",
                    "count": {"$sum": 1}
                }
        },
        {
            "$project": {
                "_id": {"$dateFromString": {"format": "%Y-%m-%d", "dateString": "$_id"}},
                "count": "$count"
            }
        },
        {
            "$sort": {"_id": 1}
        },
        {"$limit": 1000}
    ]

    if name:
        pipeline.insert(0, {"$match": {"name": name}})

    if started_at:
        beginning_of_the_day = datetime.datetime(started_at.year, started_at.month, started_at.day, 0, 0, 0, 0)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if ended_at:
        end_of_the_day = datetime.datetime(ended_at.year, ended_at.month, ended_at.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    if dedicated_bots_ids is not None:
        pipeline.insert(0, {"$match": {'extra_id': {'$in': dedicated_bots_ids}}})

    return pipeline


def _build_date_aggregated_user_analytics_pipeline(user_id: str = None,
                                                   started_at: datetime.datetime = None,
                                                   ended_at: datetime.datetime = None,
                                                   include_leadguru: bool = False,
                                                   include_dedicated: bool = False):
    pipeline = [
        {
            '$sort': {'created_at': 1}
        },
        {
            '$project': {
                'created_at':
                    {
                        '$dateToString': {'format': '%Y-%m-%d', 'date': '$created_at'}
                    },
                'name': '$name'
            }
        },
        {
            '$group': {
                '_id':
                    {
                        'created_at': '$created_at',
                        'name': '$name'
                    },
                'count': {'$sum': 1}
            }
        },
        {
            '$project': {
                '_id': {
                    'created_at':
                        {
                            '$dateFromString': {'format': '%Y-%m-%d', 'dateString': '$_id.created_at'}
                        },
                    'name': '$_id.name'
                },
                'count': '$count'
            }
        },
        {'$sort': {'_id.created_at': 1}},
        {'$limit': 1000}
    ]

    if include_leadguru and include_dedicated:
        pass
    elif include_leadguru is True:
        pipeline.insert(0, {"$match": {'extra_id': None}})
    elif include_dedicated is True:
        pipeline.insert(0, {"$match": {'extra_id': {'$ne': None}}})

    if user_id:
        pipeline.insert(0, {"$match": {"data": str(user_id)}})

    if started_at:
        beginning_of_the_day = datetime.datetime(started_at.year, started_at.month, started_at.day, 0, 0, 0, 0)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if ended_at:
        end_of_the_day = datetime.datetime(ended_at.year, ended_at.month, ended_at.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    return pipeline


def _create_result_dic(started_at: datetime.datetime = None, ended_at: datetime.datetime = None):
    analytics_dict = OrderedDict()

    if started_at and ended_at:
        days_range = range(0, (ended_at - started_at).days + 1)
        for day in days_range:
            cur_date = started_at + datetime.timedelta(days=day)
            str_date = f'{cur_date.year}-{cur_date.month:02d}-{cur_date.day:02d}'
            analytics_dict[str_date] = 0

    return analytics_dict


def _prepare_date_analytics_doc(doc, ordered_result_dict: Dict[str, int]):
    for item in doc:
        str_date = f'{item["_id"].year}-{item["_id"].month:02d}-{item["_id"].day:02d}'
        ordered_result_dict[str_date] = item["count"]
    return ordered_result_dict


def get_date_aggregated_user_analytics(user_id: str = None,
                                       started_at: datetime.datetime = None,
                                       ended_at: datetime.datetime = None,
                                       include_leadguru: bool = False,
                                       include_dedicated: bool = False):

    pipeline = _build_date_aggregated_user_analytics_pipeline(started_at=started_at,
                                                              ended_at=ended_at,
                                                              user_id=user_id,
                                                              include_dedicated=include_dedicated,
                                                              include_leadguru=include_leadguru)

    proceeded_messages = list(db['user-message-processed'].aggregate(pipeline))

    received_messages, filtered_messages = [], []
    for doc in proceeded_messages:
        current_list = received_messages if doc['_id']['name'] == '0' else filtered_messages
        current_list.append({'_id': doc['_id']['created_at'], 'count': doc['count']})

    received_messages_dic = _create_result_dic(started_at, ended_at)
    filtered_messages_dic = _create_result_dic(started_at, ended_at)

    return _prepare_date_analytics_doc(received_messages, received_messages_dic), _prepare_date_analytics_doc(
        filtered_messages, filtered_messages_dic)


def get_date_aggregated_analytics(name=None, started_at: datetime.datetime = None, ended_at: datetime.datetime = None,
                                  dedicated_bots_ids: [str] = None, dedicated_bots: bool = False):
    pipeline = _build_date_aggregated_analytics_pipeline(name, started_at, ended_at, dedicated_bots_ids)

    prefix = ''
    if dedicated_bots_ids is not None or dedicated_bots:
        prefix = "dedicated_"

    received_messages = list(db[f'{prefix}received_messages'].aggregate(pipeline))
    filtered_messages = list(db[f'{prefix}filtered_messages'].aggregate(pipeline))

    received_messages_dic = _create_result_dic(started_at, ended_at)
    filtered_messages_dic = _create_result_dic(started_at, ended_at)

    return _prepare_date_analytics_doc(received_messages, received_messages_dic), _prepare_date_analytics_doc(
        filtered_messages, filtered_messages_dic)


# @cached(cache=TTLCache(maxsize=1024, ttl=600))
def get_bots_aggregated_analytics(from_date: datetime.datetime = None,
                                  to_date: datetime.datetime = None,
                                  bot_name: str = None,
                                  dedicated_bot_ids: Optional[List[str]] = None,
                                  bot_names=None):
    pipeline = [
        {
            "$group": {
                "_id": "$name",
                "count": {"$sum": 1}
            }
        },
        {"$limit": 1000}
    ]

    if from_date:
        beginning_of_the_day = datetime.datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if to_date:
        end_of_the_day = datetime.datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    if bot_name:
        pipeline.insert(0, {"$match": {"name": bot_name}})

    if bot_names is not None:
        pipeline.insert(0, {"$match": {"name": {"$in": bot_names}}})

    prefix = ""
    if dedicated_bot_ids is not None:
        pipeline.insert(0, {"$match": {"extra_id": {"$in": dedicated_bot_ids}}})

    if dedicated_bot_ids is not None:
        prefix = "dedicated_"

    received_messages = list(db[f'{prefix}received_messages'].aggregate(pipeline))
    filtered_messages = list(db[f'{prefix}filtered_messages'].aggregate(pipeline))

    received_messages_dic = OrderedDict()
    filtered_messages_dic = OrderedDict()

    for item in received_messages:
        received_messages_dic[item["_id"]] = item["count"]

    for item in filtered_messages:
        filtered_messages_dic[item["_id"]] = item["count"]

    return received_messages_dic, filtered_messages_dic


def get_bots_leads_aggregated_analytics(bot_name=None, collection: str = 'user_leads',
                                        from_date: datetime.datetime = None,
                                        to_date: datetime.datetime = None,
                                        dedicated_only=False,
                                        dedicated_bot_ids: Optional[List[str]] = None,
                                        bot_names=None):
    db = client.lgt_admin
    pipeline = [
        {
            "$group": {
                "_id": "$message.name",
                "count": {"$sum": 1}
            }
        },
        {"$limit": 1000}
    ]

    if from_date:
        beginning_of_the_day = datetime.datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if to_date:
        end_of_the_day = datetime.datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    if bot_name:
        pipeline.insert(0, {"$match": {"message.name": bot_name}})

    if bot_names is not None:
        pipeline.insert(0, {"$match": {"message.name": {'$in': bot_names}}})

    if dedicated_bot_ids is not None:
        pipeline.insert(0, {"$match": {"message.dedicated_slack_options.bot_id": {'$in': dedicated_bot_ids}}})

    if dedicated_only:
        pipeline.insert(0, {"$match": {'message.dedicated_slack_options': {'$exists': True, '$ne': None}}})

    messages = list(db[collection].aggregate(pipeline))

    messages_dict = OrderedDict()

    for item in messages:
        messages_dict[item["_id"]] = item["count"]

    return messages_dict


def get_channel_aggregated_analytics(name,
                                     from_date: datetime.datetime = None,
                                     to_date: datetime.datetime = None,
                                     dedicated_bot_id: Optional[str] = None):
    pipeline = [
        {
            '$match': {
                'name': name
            }
        },
        {
            "$group": {
                '_id': {
                    '$arrayElemAt': [
                        '$attributes', 0
                    ]
                },
                'count': {"$sum": 1}
            }
        },
        {
            '$limit': 1000
        }
    ]

    if from_date:
        beginning_of_the_day = datetime.datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if to_date:
        end_of_the_day = datetime.datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    prefix = ""
    if dedicated_bot_id:
        pipeline.insert(0, {"$match": {"extra_id": dedicated_bot_id}})
        prefix = "dedicated_"

    received_messages = list(db[f'{prefix}received_messages'].aggregate(pipeline))
    filtered_messages = list(db[f'{prefix}filtered_messages'].aggregate(pipeline))

    received_messages_dic = OrderedDict()
    filtered_messages_dic = OrderedDict()

    for item in received_messages:
        received_messages_dic[item["_id"]] = item["count"]

    for item in filtered_messages:
        filtered_messages_dic[item["_id"]] = item["count"]

    return received_messages_dic, filtered_messages_dic


def get_channels_leads_aggregated_analytics(bot_name=None,
                                            from_date: datetime.datetime = None,
                                            to_date: datetime.datetime = None,
                                            collection: str = 'user_leads',
                                            dedicated_bot_id: Optional[str] = None):
    db = client.lgt_admin
    pipeline = [
        {
            '$group': {
                '_id': '$message.channel_id',
                'leads': {
                    '$push': '$id'
                }
            }
        }
    ]
    if bot_name:
        pipeline.insert(0, {"$match": {"message.name": bot_name}})

    if dedicated_bot_id:
        pipeline.insert(0, {"$match": {"message.dedicated_slack_options.bot_id": dedicated_bot_id}})

    if from_date:
        beginning_of_the_day = datetime.datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if to_date:
        end_of_the_day = datetime.datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    messages = list(db[collection].aggregate(pipeline))
    messages_dic = OrderedDict()

    for item in messages:
        messages_dic[item["_id"]] = item["leads"]

    return messages_dic


def get_users_aggregated_analytics(event_type: str = 'user-lead-extended',
                                   from_date: datetime.datetime = None,
                                   to_date: datetime.datetime = None,
                                   email: str = None):
    pipeline = [
        {
            "$group": {
                "_id": "$name",
                "count": {"$sum": 1}
            }
        },
        {"$limit": 1000}
    ]

    if email:
        pipeline.insert(0, {"$match": {"name": email}})

    if from_date:
        beginning_of_the_day = datetime.datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if to_date:
        end_of_the_day = datetime.datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    read_messages = list(db[event_type].aggregate(pipeline))
    read_messages_dic = OrderedDict()

    for item in read_messages:
        read_messages_dic[item["_id"]] = item["count"]

    return read_messages_dic


def get_user_date_aggregated_analytics(email=None, event_type: str = 'user-lead-extended',
                                       started_at: datetime.datetime = None,
                                       ended_at: datetime.datetime = None):
    pipeline = _build_date_aggregated_analytics_pipeline(email, started_at, ended_at)

    messages = list(db[event_type].aggregate(pipeline))
    messages_dic = _create_result_dic(started_at, ended_at)

    for item in messages:
        str_date = f'{item["_id"].year}-{item["_id"].month:02d}-{item["_id"].day:02d}'
        messages_dic[str_date] = item["count"]

    return messages_dic


def get_next_untagged_message():
    pipeline = {"label": None}
    result = db['filtered_messages'].find_one(pipeline)

    return result


def get_user_read_count(lead_ids: [str]):
    pipeline = [
        {
            "$group":
                {
                    "_id": "$data",
                    "count": {"$sum": 1}
                }
        },
        {
            "$match": {
                "_id": {"$in": lead_ids}
            }
        }
    ]
    messages = list(db['user-lead-extended'].aggregate(pipeline))
    result = dict()

    for message in messages:
        result[message['_id']] = message['count']

    return result


def tag_message(message_id, label):
    pipeline = {"_id": ObjectId(message_id)}
    db['filtered_messages'].update(pipeline, {
        "$set": {
            "label": label
        }

    })


def get_events_leads(email, event, from_date, to_date=None):
    pipeline = {
        'name': email,
        'created_at': {'$gte': from_date}
    }

    if to_date:
        end = datetime.datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, tzinfo=tz.tzutc())
        pipeline['created_at']['$lte'] = end

    return list(db[event].find(pipeline))


def get_extended_leads_aggregation(email, from_date, to_date=None):
    event = 'user-lead-extended'
    pipeline = get_event_pipeline(email, from_date, to_date)
    return list(db[event].aggregate(pipeline))


def get_deleted_leads_aggregation(email, from_date, to_date=None):
    event = 'user-lead-deleted'
    pipeline = get_event_pipeline(email, from_date, to_date)
    return list(db[event].aggregate(pipeline))


def get_archived_leads_aggregation(email, from_date, to_date=None):
    event = 'user-lead-archived'
    pipeline = get_event_pipeline(email, from_date, to_date)
    return list(db[event].aggregate(pipeline))


def get_event_pipeline(email, from_date, to_date=None):
    pipeline = [
        {
            "$match": {
                'name': email,
                'created_at': {'$gte': from_date}
            }
        },
        {
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
                }
            }
        },
        {
            "$sort": {"_id": 1}
        }
    ]

    if to_date:
        end = datetime.datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, tzinfo=tz.tzutc())
        pipeline[0]["$match"]["created_at"]['$lte'] = end

    return pipeline
