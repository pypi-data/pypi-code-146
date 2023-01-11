__author__ = 'Jackson DeDobbelaere'
__credits__ = ['Jackson DeDobbelaere']
__maintainer__ = 'Jackson DeDobbealere'
__email__ = 'jackson.dedobbelaere@c3.ai'


#!/usr/bin/env python3
import json
import time
from datetime import datetime
from reprint import output
from c3DataMigration.c3Helpers import c3Request
from c3DataMigration.c3Helpers import c3UtilityMethods




def printBatchJobStatuses (p, c3TypeToBatchJobMapping, outputLines, maxColumnPrintLength, typeOfBatchJob=None):
  for idx, c3TypeToBatchJob in enumerate(c3TypeToBatchJobMapping):
    c3Type = c3TypeToBatchJob[0]
    batchJobId = c3TypeToBatchJob[1]['id']
    status = c3TypeToBatchJob[1]['status']
    launchTime = c3TypeToBatchJob[1]['launchTime']
    completionTime = c3TypeToBatchJob[1]['completionTime']
    initialFetchCount = c3TypeToBatchJob[1]['initialFetchCount']
    currentFetchCount = c3TypeToBatchJob[1]['currentFetchCount']

    now = datetime.now()
    elapsedTimeString = 'N/A'
    if (batchJobId != None):
      elapsedTime = now - launchTime
      if (completionTime != None):
        elapsedTime = completionTime - launchTime

      days, seconds = elapsedTime.days, elapsedTime.seconds
      hours = days * 24 + seconds // 3600
      minutes = (seconds % 3600) // 60
      seconds = seconds % 60
      elapsedTimeString = 'Elapsed:' + ':'.join([str(hours).zfill(2) + 'h', str(minutes).zfill(2) + 'm', str(seconds).zfill(2) + 's'])

    suffix = None
    prefix = None
    if (typeOfBatchJob == 'removeAllAsyncAction'):
      prefix = 'Removing ' + c3Type
      removeCounts = 'CASS' + '/' + 'CASS'
      if (c3Type not in p.cassandraTypes):
        removeCounts = '{:,}'.format(initialFetchCount - currentFetchCount) + '/' + '{:,}'.format(initialFetchCount)
      suffix = ': '.join([elapsedTimeString, removeCounts, status])
    elif (typeOfBatchJob == 'importAction'):
      prefix = 'Adding ' + c3Type
      removeCounts = 'CASS' + '/' + '{:,}'.format(initialFetchCount)
      if (c3Type not in p.cassandraTypes):
        removeCounts = '{:,}'.format(currentFetchCount) + '/' + '{:,}'.format(initialFetchCount)
      suffix = ': '.join([elapsedTimeString, removeCounts, status])
    else:
      prefix = 'Checking ' + c3Type
      suffix = ' '.join([elapsedTimeString + ':', status])

    result = c3UtilityMethods.printFormatExtraPeriods(prefix, suffix, maxColumnPrintLength, False)
    outputLines[idx] = ''.join(result)




def createInitialBatchJobStatusEntry (request, c3Type, c3TypeToBatchJobMapping, filterString):
  batchJobId = None
  if ((request.text != None) and (request.text != '')):
    batchJobId = json.loads(request.text)['id']
  c3TypeToBatchJobMapping.append([c3Type, {
    'id':                batchJobId,
    'status':            'submitted',
    'launchTime':        datetime.now(),
    'completionTime':    None,
    'initialFetchCount': None,
    'currentFetchCount': None,
    'fileUrls':          [],
    'filter':            filterString, # Only used for Export Data Job
  }])

  return batchJobId




def waitForBatchJobsToComplete (r, p, c3TypeToBatchJobMapping, jobType, typeOfBatchJob=None):
  jobsStillRunning = [x for x in c3TypeToBatchJobMapping if ((x[1]['id'] != None) and (x[1]['status'] in ['submitted', 'running']))]
  with output(output_type='list', initial_len=len(c3TypeToBatchJobMapping), interval=0) as outputLines:
    while (len(jobsStillRunning) > 0):
      time.sleep(p.refreshPollTimeSeconds)
      for c3TypeToBatchJob in jobsStillRunning:
        c3Type = c3TypeToBatchJob[0]
        url = c3Request.generateTypeActionURL(r, jobType, 'get')
        payload = {
          'this': {
            'id':  c3TypeToBatchJob[1]['id']
          },
          'include': 'run',
        }

        errorCodePrefix = 'Unsuccessful grabbing status of ' + jobType + ' for type ' + c3TypeToBatchJob[0]
        request = c3Request.makeRequest(r, p.errorSleepTimeSeconds, url, payload, errorCodePrefix)

        runStatus = json.loads(request.text)['run']['status']['status']
        c3TypeToBatchJob[1]['status'] = runStatus
        if (runStatus == 'completed'):
          c3TypeToBatchJob[1]['completionTime'] = datetime.now()

        if ((typeOfBatchJob == 'importAction') and ((c3Type not in p.cassandraTypes))):
          c3TypeToBatchJob[1]['currentFetchCount'] = c3UtilityMethods.fetchCountOnType(r, p, c3TypeToBatchJob[0], '')

      printBatchJobStatuses(p, c3TypeToBatchJobMapping, outputLines, p.maxColumnPrintLength, typeOfBatchJob)
      jobsStillRunning = [x for x in c3TypeToBatchJobMapping if ((x[1]['id'] != None) and (x[1]['status'] in ['submitted', 'running']))]
