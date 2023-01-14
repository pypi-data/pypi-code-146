# implements a decentralized routines worker 
# connects to worker pool
# broadcast heartbeat
# listen to commands
# environment variables:
# SOURCE_FOLDER
# WORKERPOOL_STREAM
# GIT_SERVER
# GIT_USER
# GIT_ACRONYM
# GIT_TOKEN

import os,sys,psutil,time,json,boto3,subprocess
from importlib.metadata import version
import numpy as np
from pathlib import Path
from threading import Thread

import decentralizedroutines.defaults as defaults 
from SharedData.Logger import Logger
logger = Logger(r'decentralizedroutines\worker',user='worker')
from SharedData.SharedDataAWSKinesis import KinesisStreamConsumer,\
    KinesisStreamProducer
from decentralizedroutines.worker_lib import send_command,install_repo,\
    restart_program,run_routine

Logger.log.info('Initializing decentralizedroutines worker version %s...' % \
    (version('decentralizedroutines')))

routines = []
consumer = KinesisStreamConsumer(os.environ['WORKERPOOL_STREAM'])
producer = KinesisStreamProducer(os.environ['WORKERPOOL_STREAM'])
SLEEP_TIME = int(os.environ['SLEEP_TIME'])

Logger.log.info('decentralizedroutines worker version %s STARTED!' % \
    (version('decentralizedroutines')))

while True:
    try:
            
        for routine in routines:
            if ('process' in routine):
                if (routine['process'] is None):
                    if routine['process'].poll() is not None:
                        routines.remove(routine)
            elif (not routine['thread'].is_alive()):
                routines.remove(routine)


        if not consumer.consume():            
            consumer.get_stream()
            Logger.log.error('Cannot consume workerpool messages!')
            time.sleep(5)


        for record in consumer.stream_buffer:    
            print('Received:'+str(record))    
            
            command = record
            if ('job' in command) & ('target' in command):
                if ((command['target']==os.environ['USER_COMPUTER'])\
                     | (command['target']=='ALL')):
                    
                    if command['job'] == 'command':                    
                        send_command(command['command'])

                    elif command['job'] == 'gitpwd':      
                        if 'GIT_USER' in command:
                            os.environ['GIT_USER'] = command['GIT_USER']              
                        if 'GIT_TOKEN' in command:
                            os.environ['GIT_TOKEN'] = command['GIT_TOKEN']
                        if 'GIT_ACRONYM' in command:
                            os.environ['GIT_ACRONYM'] = command['GIT_ACRONYM']
                        if 'GIT_SERVER' in command:
                            os.environ['GIT_SERVER'] = command['GIT_SERVER']
                        Logger.log.info('Updated git parameters!')

                    elif command['job'] == 'routine': 
                        start_time = time.time()
                        routine = {
                            'command':command,
                            'thread':None,
                            'process':None,
                            'start_time':start_time,
                        }                     
                        thread = Thread(target=run_routine,args=(command,routine))
                        routine['thread'] = thread
                        routines.append(routine)
                        thread.start()
                        
                    elif command['job'] == 'install':
                        start_time = time.time()
                        routine = {
                            'command':command,
                            'thread':None,
                            'start_time':start_time,
                        }                     
                        thread = Thread(target=install_repo,args=(command,routine))
                        routine['thread'] = thread
                        routines.append(routine)
                        thread.start()

                    elif command['job'] == 'status': 

                        Logger.log.info('Status: %i process' % (len(routines)))
                        for routine in routines:
                            Logger.log.info('Status: running %s/%s %.2fs' % \
                                (routine['command']['repo'],routine['command']['routine'],\
                                    time.time()-routine['command']))

                    elif command['job'] == 'kill':
                        if command['repo']=='ALL':
                            Logger.log.info('Kill: ALL...')
                            for routine in routines:                            
                                try:
                                    routine['process'].kill()
                                except:
                                    pass
                            Logger.log.info('Kill: ALL DONE!')
                        else:
                            for routine in routines:
                                if (routine['command']['repo']==command['repo']) \
                                    & (routine['command']['routine']==command['routine']):
                                    try:
                                        Logger.log.info('Kill: %s/%s %.2fs' % \
                                            (routine['command']['repo'],routine['command']['routine'],\
                                            time.time()-routine['command']))
                                        routine['process'].kill()
                                        Logger.log.info('Kill: %s/%s DONE!' % \
                                            (routine['command']['repo'],routine['command']['routine']))
                                    except:
                                        pass

                    elif command['job'] == 'restart':                    
                        restart_program()                

                    elif command['job'] == 'ping':
                        Logger.log.info('pong')

                    elif command['job'] == 'pong':
                        Logger.log.info('ping')

        consumer.stream_buffer = []
        time.sleep(SLEEP_TIME + SLEEP_TIME*np.random.rand() - SLEEP_TIME/2)

    except Exception as e:
        consumer.stream_buffer = []
        time.sleep(SLEEP_TIME + SLEEP_TIME*np.random.rand() - SLEEP_TIME/2)
        Logger.log.error('Worker ERROR\n%s' % (str(e)))
    