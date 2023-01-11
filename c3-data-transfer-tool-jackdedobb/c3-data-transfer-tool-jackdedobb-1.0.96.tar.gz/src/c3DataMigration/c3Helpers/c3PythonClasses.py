__author__ = 'Jackson DeDobbelaere'
__credits__ = ['Jackson DeDobbelaere']
__maintainer__ = 'Jackson DeDobbealere'
__email__ = 'jackson.dedobbelaere@c3.ai'


#!/usr/bin/env python3
from argparse import Namespace
from dataclasses import dataclass, field
from datetime import datetime
from c3DataMigration.c3Helpers import c3UtilityMethods




@dataclass(frozen=True)
class APIParameters:
  # Common
  environmentArguments:     Namespace = Namespace()
  errorOutputFolder:        str = ''
  batchSize:                int = 250
  priority:                 int = 0
  errorSleepTimeSeconds:    int = 15
  refreshPollTimeSeconds:   int = 15
  masterRefreshDataSwitch:  bool = True
  maxColumnPrintLength:     int = 150
  promptUsersForWarnings:   bool = True
  sendDeveloperData:        bool = True
  initialTime:              datetime = datetime.now()
  outerAPICall:             str = ''
  serverVersion:            str = ''
  cassandraTypes:           set = field(default_factory=set)

  # Upload Specific
  dataTypeImports:          list = field(default_factory=list)
  dataUploadFolder:         str = ''
  masterRemoveDataSwitch:   bool = True
  masterUploadDataSwitch:   bool = True

  # Download Specific
  dataTypeExports:          list = field(default_factory=list)
  dataDownloadFolder:       str = ''
  stripMetadataAndDerived:  bool = False
  masterDownloadDataSwitch: bool = True




  def _validateAndAssignFieldInDict (self, dictionary, field, fieldParams):
    retBool = True

    if (fieldParams['required']):
      retBool = retBool and (field in dictionary)
      retBool = retBool and isinstance(dictionary[field], fieldParams['type'])
    else:
      if (field in dictionary):
        retBool = retBool and isinstance(dictionary[field], fieldParams['type'])
      else:
        dictionary[field] = fieldParams['defaultValue']

    return retBool




  def _validateDataTypeImports (self):
    dataTypeImports = self.__dict__['dataTypeImports']
    assert(isinstance(dataTypeImports, list))

    for dataTypeImport in dataTypeImports:
      assert(isinstance(dataTypeImport, list) and (len(dataTypeImport) == 2))
      dataType = dataTypeImport[0]
      dataTypeConfig = dataTypeImport[1]
      assert(isinstance(dataType, str))
      assert(isinstance(dataTypeConfig, dict))

      fieldsToCheck = {
        'removeData':                { 'type': bool, 'required': True,  'defaultValue': None  },
        'uploadData':                { 'type': bool, 'required': True,  'defaultValue': None  },
        'refreshCalcFields':         { 'type': bool, 'required': True,  'defaultValue': None  },
        'useSQLOnRemove':            { 'type': bool, 'required': False, 'defaultValue': False },
        'disableDownstreamOnRemove': { 'type': bool, 'required': False, 'defaultValue': False },
      }
      for fieldToCheck, fieldParams in fieldsToCheck.items():
        assert(self._validateAndAssignFieldInDict(dataTypeConfig, fieldToCheck, fieldParams))
      assert(len(set(dataTypeConfig.keys()) - set(fieldsToCheck.keys())) == 0)

      dataTypeConfig['gzipFiles'] = []
      dataTypeConfig['remoteFileUrls'] = []




  def _validateDataTypeExports (self):
    dataTypeExports = self.__dict__['dataTypeExports']
    assert(isinstance(dataTypeExports, list))

    for dataTypeExport in dataTypeExports:
      assert(isinstance(dataTypeExport, list) and (len(dataTypeExport) == 2))
      dataType = dataTypeExport[0]
      dataTypeConfig = dataTypeExport[1]
      assert(isinstance(dataType, str))
      assert(isinstance(dataTypeConfig, dict))

      fieldsToCheck = {
        'downloadData':      { 'type': bool, 'required': True,  'defaultValue': None     },
        'refreshCalcFields': { 'type': bool, 'required': True,  'defaultValue': None     },
        'numRecordsPerFile': { 'type': int,  'required': False, 'defaultValue': 2000     },
        'filter':            { 'type': str,  'required': False, 'defaultValue': ''       },
        'include':           { 'type': str,  'required': False, 'defaultValue': 'this'   },
      }
      for fieldToCheck, fieldParams in fieldsToCheck.items():
        assert(self._validateAndAssignFieldInDict(dataTypeConfig, fieldToCheck, fieldParams))
      assert(len(set(dataTypeConfig.keys()) - set(fieldsToCheck.keys())) == 0)
      dataTypeExport[1]['filter'] = '' if (dataTypeExport[1]['filter'] == '1 == 1') else dataTypeExport[1]['filter']





  def __post_init__ (self):
    d = self.__dict__

    d['priority'] = max(d['priority'], 0)

    if (d['errorOutputFolder'] == None):
      d['errorOutputFolder'] = (d['dataDownloadFolder'] + '_Errors')

    if (d['maxColumnPrintLength'] == None):
      if (d['outerAPICall'] == 'uploadAPI'):
        d['maxColumnPrintLength'] = min(max([len(x[0]) for x in d['dataTypeImports']]) + 80, 150)
      elif (d['outerAPICall'] == 'downloadAPI'):
        d['maxColumnPrintLength'] = min(max([len(x[0]) for x in d['dataTypeExports']]) + 80, 150)

    self._validateDataTypeImports()
    self._validateDataTypeExports()

    d['serverVersion'] = c3UtilityMethods.getC3ServerVersionOnEnv(d['environmentArguments'], d['errorSleepTimeSeconds'])
    d['cassandraTypes'] = c3UtilityMethods.retrieveCassandraTypes(d['environmentArguments'], d['errorSleepTimeSeconds'])
    d['environmentArguments'] = None
