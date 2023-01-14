import pymongo
class Mixin:
    def search_scheduled_transfers_mongo(self, transfer_type, gte, lte, start_date, end_date, 
        skip, limit, sort_on='amount', sort_direction=-1):
        
        sort_direction = pymongo.ASCENDING if sort_direction == 1 else pymongo.DESCENDING
        sort_condition = { '$sort':      { 'amount_ccd': sort_direction} } if sort_on =='amount' else { '$sort':      { 'blockInfo.blockSlotTime': sort_direction} }
        type_contents_condition = ['transferWithSchedule']
        pipeline = [
            {
                '$match': { 'type.contents': { '$in': type_contents_condition } }
            }, 
            
            { '$set': {
                "amount_ccd": {
                    '$sum': {
                        '$first': {
                            '$map': {
                                'input': "$result.events",
                                'as': "event",
                                'in': {
                                    '$map': {
                                    'input': "$$event.amount",
                                    'as': "amount",
                                    'in': {
                                        '$divide': [{'$toDouble': {'$last': "$$amount"} }, 1000000]
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            },
            { '$match':     { 'amount_ccd': { '$gte': gte } } },
            { '$match':     { 'amount_ccd': { '$lte': lte } } },
            { "$match":     {"blockInfo.blockSlotTime": {"$gte": start_date, "$lt": end_date } } },
            sort_condition,
            {'$facet': {
            'metadata': [ { '$count': 'total' } ],
            'data': [ { '$skip': int(skip) }, { '$limit': int(limit) } ]
            }},
            {'$project': { 
                'data': 1,
                'total': { '$arrayElemAt': [ '$metadata.total', 0 ] }
            }
            }
        ]

        return pipeline

    def search_transfers_mongo(self, transfer_type, gte, lte, start_date, end_date, 
        skip, limit, sort_on='amount', sort_direction=-1, memo_only=False):
        
        sort_direction = pymongo.ASCENDING if sort_direction == 1 else pymongo.DESCENDING
        sort_condition = { '$sort':      { 'amount_ccd': sort_direction} } if sort_on =='amount' else { '$sort':      { 'blockInfo.blockSlotTime': sort_direction} }
        type_contents_condition = ['transferWithMemo'] if memo_only else ['transfer','transferWithMemo']
        pipeline = [
            {
                '$match': { 'type.contents': { '$in': type_contents_condition } }
            }, 
            { '$addFields': 
                { 'amount_ccd': 
                { '$first' :
                    {
                    '$map':
                        {
                        'input': "$result.events",
                        'as': "events",
                        'in': { '$trunc': { '$divide': [{'$toDouble': '$$events.amount'}, 1000000] } }
                        }
                    }
                }
                }
            },
            { '$match':     { 'amount_ccd': { '$gte': gte } } },
            { '$match':     { 'amount_ccd': { '$lte': lte } } },
            { "$match":     {"blockInfo.blockSlotTime": {"$gte": start_date, "$lt": end_date } } },
            sort_condition,
            {'$facet': {
            'metadata': [ { '$count': 'total' } ],
            'data': [ { '$skip': int(skip) }, { '$limit': int(limit) } ]
            }},
            {'$project': { 
                'data': 1,
                'total': { '$arrayElemAt': [ '$metadata.total', 0 ] }
            }
            }
        ]

        return pipeline

    def search_txs_hashes_for_account_as_sender(self, account_id):
        pipeline = [
            {
                '$match': { 'sender': { '$eq': account_id } }
            }
        ]
        return pipeline

    def search_txs_hashes_for_account_as_receiver(self, account_id):
        pipeline = [
            {
                '$match': { 'receiver': { '$eq': account_id } }
            }
        ]
        return pipeline

    def search_txs_hashes_for_account_as_sender_with_params(self, account_id, start_block, end_block):
        pipeline = [
            {
                '$addFields': {
                    'canonical_address': {
                        '$substr': [
                            '$sender', 0, 29
                        ]
                    }
                }
                },  
            { '$match': { 'canonical_address': { '$eq': account_id[:29] } 
                } 
            },
            { "$match":     {"blockHeight": {"$gt": start_block, "$lte": end_block } } },
        ]
        return pipeline

    def search_txs_hashes_for_account_as_receiver_with_params(self, account_id, start_block, end_block):
        pipeline = [
            {
                '$addFields': {
                    'canonical_address': {
                        '$substr': [
                            '$receiver', 0, 29
                        ]
                    }
                }
                },  
            { '$match': { 'canonical_address': { '$eq': account_id[:29] } 
                } 
            },
            { "$match":     {"blockHeight": {"$gt": start_block, "$lte": end_block } } },
        ]
        return pipeline

    def search_txs_in_hash_list(self, tx_hashes):
        pipeline = [
            {
                '$match': { '_id': { '$in': tx_hashes } }
            }
        ]
        return pipeline

    def search_txs_in_transactions(self, start_block, end_block):
        pipeline = [
            { "$match":     {"blockInfo.blockHeight": {"$gt": start_block, "$lte": end_block } } },
        ]
        return pipeline

    def heights_with_transactions_after(self, start_block):
        pipeline = [
            { "$match":     {"blockHeight": {"$gt": start_block } } },
            {"$project":    {"_id": 0, "blockHeight": 1}}
        ]
        return pipeline

    def search_txs_non_finalized(self):
        pipeline = [
            { "$match":     {"blockInfo.finalized": False} },
            
        ]
        return pipeline