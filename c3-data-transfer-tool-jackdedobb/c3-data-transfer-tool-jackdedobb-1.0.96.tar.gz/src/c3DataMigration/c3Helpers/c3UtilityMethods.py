__author__ = 'Jackson DeDobbelaere'
__credits__ = ['Jackson DeDobbelaere']
__maintainer__ = 'Jackson DeDobbealere'
__email__ = 'jackson.dedobbelaere@c3.ai'


#!/usr/bin/env python3
import json
import math
import os
import requests
import xml.etree.ElementTree as ET
from c3DataMigration.c3Helpers import c3Request




def printFormatWrapMaxColumnLength (string, maxColumnPrintLength, printToConsole):
  chunks = [string[i:i+maxColumnPrintLength] for i in range(0, len(string), maxColumnPrintLength)]
  if (printToConsole):
    for chunk in chunks:
      print(chunk)
  return chunks




def printFormatExtraPeriods (prefix, suffix, maxColumnPrintLength, printToConsole):
  customStringPeriods = '.' * (maxColumnPrintLength - len(prefix) - len(suffix))
  if (printToConsole):
    print(prefix + customStringPeriods + suffix)

  return [prefix, customStringPeriods, suffix]




def printFormatExtraDashes (printString, maxColumnPrintLength, printToConsole):
  prefix = '_' * math.floor((maxColumnPrintLength - len(printString) - 2) / 2)
  suffix = '_' * math.ceil((maxColumnPrintLength - len(printString) - 2) / 2)

  if (printToConsole):
    print('\n' + prefix + ' ' + printString + ' ' + suffix)

  return [prefix, printString, suffix]




def getLocalVersionC3DataTransferTool ():
  currentVersion = None
  try:
    commandOutput = os.popen('pip3 show c3-data-transfer-tool-jackdedobb | grep Version').read()
    currentVersion = commandOutput[len('Version: '):].replace('\n', '')
  except:
    pass

  return currentVersion




def getLatestVersionC3DataTransferTool ():
  latestVersion = None
  try:
    url = 'https://pypi.org/rss/project/c3-data-transfer-tool-jackdedobb/releases.xml'
    rssFeed = requests.get(url)
    latestVersion = ET.ElementTree(ET.fromstring(rssFeed.text)).getroot().find('./channel/item/title').text
  except:
    pass
  return latestVersion




def getC3ServerVersionOnEnv (r, errorSleepTimeSeconds):
  url = c3Request.generateServerVersionURL(r)
  errorCodePrefix = 'Unsuccessful getting C3 Server Version'
  request = c3Request.makeRequest(r, errorSleepTimeSeconds, url, None, errorCodePrefix)

  return request.text




def getc3Context (r, errorSleepTimeSeconds):
  url = c3Request.generateTypeActionURL(r, 'JS', 'exec')
  payload = {
    'js': 'c3Context()'
  }
  errorCodePrefix = 'Unsuccessful getting c3Context'
  request = c3Request.makeRequest(r, errorSleepTimeSeconds, url, payload, errorCodePrefix)
  c3Context = json.loads(json.loads(request.text))

  return c3Context




def fetchCountOnType (r, p, c3Type, filterString):
  url = c3Request.generateTypeActionURL(r, c3Type, 'fetchCount')
  payload = {
    'spec': {
      'filter': filterString
    }
  }
  errorCodePrefix = 'Unsuccessful fetchCount of type ' + c3Type
  request = c3Request.makeRequest(r, p.errorSleepTimeSeconds, url, payload, errorCodePrefix)

  return int(request.text)




def retrieveCassandraTypes (r, errorSleepTimeSeconds):
  url = c3Request.generateTypeActionURL(r, 'TagMetadataStore', 'entityTypes')
  payload = {
    'datastoreName': 'cassandra'
  }
  errorCodePrefix = 'Unsuccessful retrieval of cassandra types'
  request = c3Request.makeRequest(r, errorSleepTimeSeconds, url, payload, errorCodePrefix)

  return set([x['typeName'] for x in json.loads(request.text)])




def retrieveLabeledFields (r, c3Type, errorSleepTimeSeconds):
  jsExecCode = """
    var fieldLabelMap = {
      calcFieldArr: [],
      foreignKeyFieldArr: [],
      timedValueHistoryFieldArr: [],
    };
    INSERT_HERE_FOR_FORMAT.fieldTypes().forEach(function(fieldType) {
      var fieldExtensions = fieldType.extensions().db || {};
      var fieldName = fieldType._init.name;
      if (fieldExtensions.calculated != null) {
        fieldLabelMap.calcFieldArr.push(fieldName);
      }
      if (fieldExtensions.fkey != null) {
        fieldLabelMap.foreignKeyFieldArr.push(fieldName);
      }
      if (fieldExtensions.timedValueHistoryField != null) {
        fieldLabelMap.timedValueHistoryFieldArr.push(fieldName);
      }
    });
    fieldLabelMap
  """.replace('INSERT_HERE_FOR_FORMAT', c3Type)

  url = c3Request.generateTypeActionURL(r, 'JS', 'exec')
  payload = {
    'js': jsExecCode
  }
  errorCodePrefix = 'Unsuccessful getting fieldTypes for: ' + c3Type
  request = c3Request.makeRequest(r, errorSleepTimeSeconds, url, payload, errorCodePrefix)
  fieldTypes = json.loads(json.loads(request.text))

  return fieldTypes




def stripMetaAndDerivedFieldsFromRecords (records, fieldLabelMap):
  def removeKeyFromObj (entity, field):
    if field in entity:
      del entity[field]

  calcFieldsToRemove = fieldLabelMap['calcFieldArr']
  fKeyFieldsToRemove = fieldLabelMap['foreignKeyFieldArr']
  tvHistoryFieldsToRemove = fieldLabelMap['timedValueHistoryFieldArr']

  for record in records:
    removeKeyFromObj(record, 'meta')
    removeKeyFromObj(record, 'type')
    removeKeyFromObj(record, 'version')
    removeKeyFromObj(record, 'versionEdits')
    [removeKeyFromObj(record, x) for x in calcFieldsToRemove]
    [removeKeyFromObj(record, x) for x in fKeyFieldsToRemove]
    [removeKeyFromObj(record, x) for x in tvHistoryFieldsToRemove]
