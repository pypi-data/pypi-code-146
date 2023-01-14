# PROPRIETARY LIBS
import os,sys,time
from decentralizedroutines.RoutineScheduler import RoutineScheduler
from datetime import datetime

import decentralizedroutines.defaults as defaults 
from SharedData.Logger import Logger
logger = Logger(__file__,'master')
from SharedData.SharedDataAWSKinesis import KinesisStreamConsumer,KinesisStreamProducer


if len(sys.argv)>=2:
    SCHEDULE_NAME = str(sys.argv[1])
else:
    #SCHEDULE_NAME = 'SCHEDULES/MASTER'
    Logger.log.error('SCHEDULE_NAME not provided, please specify!')
    raise Exception('missing parameter')


Logger.log.info('Routine schedule starting for %s...' % (SCHEDULE_NAME))


stream_name=os.environ['WORKERPOOL_STREAM']
producer = KinesisStreamProducer(stream_name)

# send git configuration
if ('GIT_USER' not in os.environ) | \
    ('GIT_TOKEN' not in os.environ) |\
    ('GIT_ACRONYM' not in os.environ):
    Logger.log.error('Initializing scheduler %s ERROR missing git parameters'\
        % (SCHEDULE_NAME))
    raise Exception('missing parameter in .env')

GIT_USER=os.environ['GIT_USER']
GIT_TOKEN=os.environ['GIT_TOKEN']
GIT_ACRONYM=os.environ['GIT_ACRONYM']
GIT_SERVER=os.environ['GIT_SERVER']
data = {
    "sender" : "MASTER",
    "target" : "ALL",
    "job" : "gitpwd",    
    "GIT_USER" : GIT_USER,
    "GIT_TOKEN" : GIT_TOKEN,
    "GIT_ACRONYM" : GIT_ACRONYM,
    "GIT_SERVER" : GIT_SERVER
}
producer.produce(data,'command')

Logger.log.info('Sent git credentials')

sched = RoutineScheduler(stream_name)
sched.LoadSchedule(SCHEDULE_NAME)
sched.UpdateRoutinesStatus()

Logger.log.info('Routine schedule STARTED!')
time.sleep(15)
while(True):
    print('',end='\r')
    print('Running Schedule %s' % (str(datetime.now())),end='')
    if sched.schedule['Run Times'][0].date()<datetime.now().date():
        print('')
        print('Reloading Schedule %s' % (str(datetime.now())))
        print('')
        sched.LoadSchedule(SCHEDULE_NAME)
        sched.UpdateRoutinesStatus()

    sched.UpdateRoutinesStatus()
    sched.RunPendingRoutines()    
    time.sleep(15) 