import os

mq_arry = os.environ['MQ_URL'].split('/')
coll = mq_arry[-1] if len(mq_arry) > 1 else 'realtime'
MQ_URL = 'amqp://' + mq_arry[0] + '/{0}?heartbeat=3600'.format(coll)

NTN_URL = 'mongodb://' + os.environ['NTN_URL']
NTN_COLL = NTN_URL.split('/')[-1]

IREY_URL = 'mongodb://' + os.environ['IREY_URL']
IREY_COLL = IREY_URL.split('/')[-1]