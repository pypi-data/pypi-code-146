__author__ = 'Jackson DeDobbelaere'
__credits__ = ['Jackson DeDobbelaere']
__maintainer__ = 'Jackson DeDobbealere'
__email__ = 'jackson.dedobbelaere@c3.ai'


#!/usr/bin/env python3
import json
from c3DataMigration.c3Helpers import c3FileSystem
from c3DataMigration.c3Helpers import c3Request
from c3DataMigration.c3Helpers import c3UtilityMethods




def enableQueues (r, p, promptUser=True, listOfQueueNamesToEnable=None):
  if (listOfQueueNamesToEnable == None):
    listOfQueueNamesToEnable = [
      'ActionQueue',
      'BatchQueue',
      'CalcFieldsQueue',
      'MapReduceQueue',
      'ChangeLogQueue',
      'NormalizationQueue',
    ]

  queueNamesToEnable = []
  for queueName in listOfQueueNamesToEnable:
    url = c3Request.generateTypeActionURL(r, queueName, 'isPaused')
    errorCodePrefix = 'Unsuccessful checking status of queue: ' + queueName
    request = c3Request.makeRequest(r, p.errorSleepTimeSeconds, url, None, errorCodePrefix)
    if (json.loads(request.text) == True):
      queueNamesToEnable.append(queueName)

  if ((promptUser == True) and (len(queueNamesToEnable) > 0)):
    string = 'Type (y/yes) to confirm resuming of queues: ' + str(queueNamesToEnable)
    c3UtilityMethods.printFormatWrapMaxColumnLength(string, p.maxColumnPrintLength, True)
    if (not (input().lower() in ['y', 'yes'])):
      print('Exiting script.')
      exit(0)

  for queueName in queueNamesToEnable:
    url = c3Request.generateTypeActionURL(r, queueName, 'resume')
    errorCodePrefix = 'Unsuccessful resuming queue: ' + queueName
    request = c3Request.makeRequest(r, p.errorSleepTimeSeconds, url, None, errorCodePrefix)
    print('Resumed Queue: ' + queueName)




def outputQueueErrors (r, errorSleepTimeSeconds, dataTypeErrorFileLocation, c3Type, batchJobId):
  url = c3Request.generateTypeActionURL(r, 'InvalidationQueueError', 'fetch')

  payload = {
    'spec': {
      'filter': 'targetObjId == "{}"'.format(batchJobId),
      'limit': 2000
    }
  }
  errorCodePrefix = 'Failed to fetch InvalidationQueue errors for ' + c3Type
  request = c3Request.makeRequest(r, errorSleepTimeSeconds, url, payload, errorCodePrefix)

  with open(dataTypeErrorFileLocation, 'w') as f:
    f.write(request.content.decode('utf-8'))




def outputAllQueueErrorsFromMapping (r, p, c3TypeToBatchJobMapping, jobType):
  queueErrorOutputFolder = '/'.join([p.errorOutputFolder, jobType])
  c3FileSystem.wipeLocalDirectory(p, queueErrorOutputFolder, p.promptUsersForWarnings)

  for c3TypeToBatchJob in c3TypeToBatchJobMapping:
    c3Type = c3TypeToBatchJob[0]
    if (c3TypeToBatchJob[1]['status'] in ['failing', 'failed']):
      dataTypeErrorFileLocation = '/'.join([queueErrorOutputFolder, c3Type + '_errors.xml'])
      outputQueueErrors(r, p.errorSleepTimeSeconds, dataTypeErrorFileLocation, c3Type, c3TypeToBatchJob[1]['id'])
      c3UtilityMethods.printFormatExtraPeriods('Generating ' + c3Type, 'DONE', p.maxColumnPrintLength, True)
    else:
      c3UtilityMethods.printFormatExtraPeriods('Generating ' + c3Type, 'NO ERRORS', p.maxColumnPrintLength, True)
