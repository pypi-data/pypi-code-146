from . import restClient,query,digitalCommerceUtil,file,utils,objectUtil,Sobjects
import simplejson,logging

import colorama
import sys,time,os
import ansi2html,re
import threading,traceback
from queue import Queue

def _queryLogRecords(logUserId=None,limit=50,whereClause=None):
    where = f" where {whereClause} " if whereClause != None else ''
    where = f" where logUserId='{logUserId}' " if logUserId is not None else where

    call = query.query(f"Select Id,LogUserId,LogLength,LastModifiedDate,Request,Operation,Application,Status,DurationMilliseconds,StartTime,Location,RequestIdentifier FROM ApexLog  {where} order by LastModifiedDate desc limit {limit}")
    return call

userCache = {}
def _queryUsername(Id):
    usernameq = f"select Username from User where Id='{Id}'"

    if usernameq in userCache:
        username = userCache[usernameq]
    else:
        username = query.queryField(usernameq)
        userCache[usernameq] = username   
    return username

def _logRecord_toString(logRecord):
    log = logRecord
    username = _queryUsername(log['LogUserId'])

    logLine = f"""LOGDATA:    Id: {log['Id']}   LogUserId: {log['LogUserId']} ({username})   Request: {log['Request']}  Operation: {utils.CGREEN}{log['Operation']}{utils.CEND}    lenght: {log['LogLength']}    duration: {log['DurationMilliseconds']} 
LOGDATA:      startTime: {log['StartTime']}    app: {log['Application']}      status: {log['Status']}     location: {log['Location']}     requestIdentifier: {log['RequestIdentifier']}
    """     
    return logLine

def _queryLogData(logId):
    logRecords = query.queryRecords(f"Select fields(all) FROM ApexLog where Id ='{logId}' limit 1")

    if logRecords == None or len(logRecords)==0:
        utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{logId}> cannot be found in the Server.',other=f"No record in ApexLogwith Id {logId}")    
    logRecord = logRecords[0]

    action = f"/services/data/v56.0/sobjects/ApexLog/{logId}/Body/"
    logbody = restClient.callAPI(action)
    return logRecord,logbody

def parseStorage(pc):
    
    search_dir = restClient.logFolder()

    os.chdir(search_dir)
    files = filter(os.path.isfile, os.listdir(search_dir))
    files = [os.path.join(search_dir, f) for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    fileNames = [os.path.basename(f) for f in files]
    fileNames = [f for f in fileNames if '.log' in f]

    ids = [f.split('.')[0] for f in fileNames]
    print(f"Parsing {len(ids)} files in {search_dir}")

    try:
        _parseIds(ids,pc,printProgress=True,printNum=False)

    except KeyboardInterrupt:
        print('Interrupted')
    
    _printParsingResults(pc)

def parseTail(pc):
    deleteList = []
    def deleteRecords(q):
      while True:
        Id = q.get()
        res = Sobjects.delete('ApexLog',Id)
        restClient.glog().debug(f"deleted records {Id}")
        q.task_done()


    timefield = "StartTime"

    logRecords = query.queryRecords(f"Select fields(all) FROM ApexLog order by {timefield} desc limit 1")
    if len(logRecords) > 0:
        _time = logRecords[0][timefield]
        _timez = _time.split('.')[0] + "Z"
    else:
        _timez = '2000-12-12T17:19:35Z'

    waitingPrinted = False
    q= None
    restClient.glog().debug(f"deleteLogs-->{pc['deleteLogs']}")
    if pc['deleteLogs']==True:
        if loguser==None:
            username = restClient.getCurrentThreadConnection()['username']
            loguser = f"Username:{username}"
        
        restClient.glog().debug("Starting queue")
        q = Queue(maxsize=0)
        threading.Thread(target=deleteRecords,args=(q,), daemon=True).start()
        threading.Thread(target=deleteRecords,args=(q,), daemon=True).start()
    
    logUserId = _getLogUserId(loguser=pc['loguser']) if pc['loguser'] != None else None

    try:
        while (True):
            where = f" {timefield} > {_timez} "
            where = f" {pc['whereClause']} and {where}" if pc['whereClause'] is not None else where
            where = f" logUserId='{logUserId}'and {where} " if logUserId is not None else where

            fields = "Id,LogUserId,LogLength,LastModifiedDate,Request,Operation,Application,Status,DurationMilliseconds,StartTime,Location,RequestIdentifier"
            logRecords = query.queryRecords(f"Select {fields} FROM ApexLog where {where} order by StartTime desc")
            if len(logRecords) > 0:
                waitingPrinted = False

                logIds = [record['Id'] for record in logRecords]
                _parseIds(logIds=logIds,pc=pc,raiseKeyBoardInterrupt=True)

                _time = logRecords[-1][timefield]
                _timez = _time.split('.')[0] + "Z"

                if q!=None:
                    for logId in logIds:
                        q.put(logId)
                        restClient.glog().debug(f"{logId} into queue...")

            else:
                if waitingPrinted == False:
                    print()
                    if pc['loguser'] != None:
                        print(f"waiting for debug logs for user {pc['loguser']}")
                    else:
                        print(f"waiting for debug logs ")

                    waitingPrinted = True

            time.sleep(2)
    except KeyboardInterrupt as e:
        print()
        _printParsingResults(pc)
        print("Terminating -tail..., cleaning up")
        if q != None:
            while q.empty()==False:
                time.sleep(1)
        print('Terminated')
        return

def _parseIds(logIds,pc,raiseKeyBoardInterrupt=False,printProgress=False,threads=10,printNum=True):
    def readBody(q):
      while True:
        Id = q.get()
        _readBodyId(Id)
        restClient.glog().debug(f"Read body for Id {Id}")
        q.task_done()

    if 'total' not in pc:
        pc['total'] = 0
    if 'parsed' not in pc:
        pc['parsed'] = []
    if 'errors' not in pc:
        pc['errors'] = []
    parsed = pc['parsed']
    errors = pc['errors']

    if threads >0 and ('queue' not in pc or pc['queue'] == False):
        q = Queue(maxsize=0)
        for x in range(0,threads):
            threading.Thread(target=readBody,args=(q,), daemon=True).start()
    if threads>0:
        for logid in logIds:
            q.put(logid)
            
    for num,logId in enumerate(logIds):
        if printProgress:
            sys.stdout.write("\r%d%%" % int(100*num/len(logIds)))
        try:
            _parsed={
                'logId':logId,
                'status':'ok'
            }
            parsed.append(_parsed)
            pc['logId'] = logId
            _readBody(pc)
            _parseLog_print(pc)
            _printParsedLog(pc)
            if printNum:
                print( pc['total']+num+1)
            if pc['context']['exception'] == True:
                _parsed['status'] = pc['context']['exception_msg'][0:200]

        except KeyboardInterrupt:
            if raiseKeyBoardInterrupt:
                raise
            break
        except utils.InCliError as e:
             _parsed['status'] = f"Parse error: {e.args[0]['errorCode']}  "
             utils.printException(e)
             errors.append(e)
        except Exception as e:
            _parsed['status'] = f"Unknown: {e}"
            errors.append(e)
            print(traceback.format_exc())


    pc['total'] = pc['total'] + num + 1
    
def _printParsingResults(pc):
    print()

    if 'parsed' not in pc:
        print("No files parsed.")
        return 
    parsed = pc['parsed']
    errors = pc['errors']

    print(f"{pc['total']} logs parsed")
    parsed = [par for par in parsed if par['status']!='ok']

    if len(parsed) == 0:
        print("No errors.")
    if len(parsed)>0:
        utils.printFormated(parsed)

        errors = list({error.args[0]['errorCode']:error for error in errors}.values())
        for error in errors:
            utils.printException(error)  

def parseLogs_LastN(pc):
    whereClause = pc['whereClause']
    loguser = pc['loguser']
    lastN = pc['lastN']

    where = f" where {whereClause} " if whereClause is not None else ''
    where = f" where logUserId='{_getLogUserId(loguser)}' " if loguser is not None else where

    q = f"Select Id FROM ApexLog {where} order by LastModifiedDate desc limit {lastN}"
    if lastN == None:
        lastN = 1
    logIds = query.queryFieldList(f"Select Id FROM ApexLog {where} order by LastModifiedDate desc limit {lastN}")
    if logIds == None or len(logIds)==0:
        utils.raiseException(errorCode='NO_LOG',error=f'No logs can be found. ',other=q)

    _parseIds(logIds,pc)
    _printParsingResults(pc)

def _getLogUserId(loguser):
    chunks = loguser.split(":")
    key = chunks[0] if len(chunks)>1 else 'Id'
    value = chunks[1] if len(chunks)>1 else chunks[0]
    if key.lower() == 'id':
        return value
    id = query.queryField(f"Select Id from User where {key}='{value}'") if key.lower()!='id' else value
    if id == None:
        utils.raiseException('QUERY',f"User with field {key} = {value} does not exist in the User Object.")    
    return id

def _readBodyId(logId):
    filename = f"{restClient.logFolder()}{logId}.log"

    if file.exists(filename) == True:
        body = file.read(filename)

        if len(body)==0:
            print("The file seems corrupted. Getting log from server.")
            file.delete(filename)
            return _readBodyId(logId)
        return None,body,filename
    else:
        logRecord,body = _queryLogData(logId) 
        body = _logRecord_toString(logRecord=logRecord) + body  
        _saveToStore(logId,body)
        return logRecord,body,filename

def _readBody(pc):
    logId = pc['logId']
    pc['logRecord'],pc['body'],pc['filepath'] = _readBodyId(logId)

def parseFile(parseContext):
    parseContext['body'] = file.read(parseContext['filepath'])
    parseContext['operation'] = 'parsefile'
    name = os.path.basename(parseContext['filepath']).split('.')[0]
    parseContext['logId']=name
    context =  _parseLog_print(parseContext)
    _printParsedLog(parseContext)
    return context

def parseLogId(logId,parseContext):
    _readBody(parseContext)
    if parseContext['body'] == None :
        utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{logId}> cannot be found. ')

    if len(parseContext['body'])==0:
        utils.raiseException(errorCode='NO_LOG',error=f'The body for the requested log <{logId}> is empty. ')
    context =  _parseLog_print(parseContext)
    _printParsedLog(parseContext)

    return context

def parseLog(logId=None,filepath=None,printLimits=False,lastN=1,loguser=None,level=None,whereClause=None,writeToFile=False,tail=False,deleteLogs=False,store=False,error=False):
    parseContext = {
        'logId' :logId,
        'filepath':filepath,
        'printLimits':printLimits,
        'lastN':lastN,
        'loguser':loguser,
        'level':level,
        'whereClause':whereClause,
        'writeToFile':writeToFile,
        'tail':tail,
        'deleteLogs':deleteLogs,
        'parseStore':store,
        'logToStore':True,
        'onlyErrors':error,
        'operation':None
    }

    if tail == True:
        return parseTail(parseContext)

    elif store == True:
        return parseStorage(parseContext)

    elif filepath != None:
        return parseFile(parseContext)

    elif logId != None:  #check if already downloaded
        return parseLogId(logId,parseContext)
    else:
        return parseLogs_LastN(parseContext)


def _saveToStore(logId,body):
    filename = f"{restClient.logFolder()}{logId}.log"
    file.write(filename,body) 

def _parseLog_print(pc):
    body = pc['body']
    logId = pc['logId']

    if body == None :
        utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{logId}> cannot be found. ')

    if len(body)==0:
        utils.raiseException(errorCode='NO_LOG',error=f'The body for the requested log <{logId}> is empty. ')

    return parse(pc)    

def printLogRecords(loguser=None,limit=50,whereClause=None):
    logUserId = _getLogUserId(loguser) if loguser != None else None
    if loguser != None:
        print(f'Logs for user {loguser}:')
    logs = _queryLogRecords(logUserId,limit=limit,whereClause=whereClause)
    logs = utils.deleteNulls(logs,systemFields=False)
    logs1 = []
    for log in logs:
        log['LastModifiedDate'] = log['LastModifiedDate'].split('.')[0]
        log['StartTime'] = log['StartTime'].split('.')[0]
        log['LogUserId'] =  f"{log['LogUserId']} ({_queryUsername(log['LogUserId'])})"

        logs1.append(log)

    utils.printFormated(logs1,rename="LogLength%Len:DurationMilliseconds%ms:Application%App")
    return logs

def delta(obj,field):
    return obj[field][1] - obj[field][0] if len(obj[field]) > 1 else 0

def setTimes(context,line,obj=None,field=None,value=None,chunkNum=None,type=None):
    def addList(obj,field,val):
        if field in obj:
            obj[field].append(val)
        else:
            obj[field] = [val]

    chunks = line.split('|')

    if obj == None:
        obj = {
            'type' : type,
            'ident' : context['ident'],
            'exception' :False
        }
       
        if len(chunks)>3:
            obj['Id'] = chunks[3]

    addList(obj,'lines',line)
    addList(obj,'CPUTime',context['DEF:CPU time'])
    addList(obj,'SOQLQueries',context['DEF:SOQL queries'])
    addList(obj,'cmtCPUTime',context['CMT:CPU time'])
    addList(obj,'cmtSOQLQueries',context['CMT:SOQL queries'])
    addList(obj,'totalQueries',context['totalQueries'])
    addList(obj,'time',chunks[0].split(' ')[0])
    if len(chunks)>1:
        addList(obj,'timeStamp',int ((chunks[0].split('(')[1]).split(')')[0]))
    else:
        addList(obj,'timeStamp',0)


    if obj['type'] is None:
        print()

    if field is not None:
        obj[field] = chunks[chunkNum] if value is None else value

    if context['timeZero'] == 0:
        context['timeZero'] = obj['timeStamp'][0]

    obj['elapsedTime'] = obj[f'timeStamp'][0] #- _context['timeZero']

    return obj

def createContext():
    context = {
        'totalQueries' : 0,
        'timeZero':0,
        'ident':0,
        'DEF:SOQL queries' : 0,
        'DEF:CPU time' : 0,
        'CMT:SOQL queries' : 0,
        'CMT:CPU time' : 0,
        "exception":False
    }
    context['totalQueries'] = 0
    context['timeZero'] = 0
    context['ident'] = 0
    context['DEF:SOQL queries'] = 0
    context['DEF:CPU time']=0
    context['CMT:SOQL queries'] = 0
    context['CMT:CPU time']=0
    context['exception'] = False
    context['file_exception'] = False
    context['previousElapsedTime'] = 0
    context['previousCPUTime'] = 0
    context['previousIsLimit'] = False
    context['prevTimes'] = {
        0:[0,0]
    }
    context['prevLevel'] = 0
    context['firstLineIn'] = True
    context['firstLineOut'] = True
    return context

def parse(pc):
   # logId,logData,printLimits=True,userDebug=True,level=None,writeTofile=False,error=False,limits=False
    logId = pc['logId']

    try:
       return  _parse(pc)
    except KeyboardInterrupt as e:
        print(f"Parsing for logI {logId} interrupted.")
        raise
    except Exception as e:
        print(f"Exception while parsing for logI {logId} ")
        raise 

def _printParsedLog(pc):
    context = pc['context']
    context['debugList'] = processRepetition(context['debugList'])
    printDebugList(pc)

def _parse(pc):
    context = createContext()
    pc['context'] = context

    logData = pc['body']
    context['lines'] = logData.splitlines()
    debugList = []

    context['debugList'] = debugList
    context['openItemsList'] = []

    for num,line in enumerate(context['lines']):
        chunks = line.split('|')
        context['chunks'] = chunks
        context['lenChunks'] = len(chunks)

        context['line'] = line
        context['num'] = num

        if '16994953586' in chunks[0]:
            a=1

        if context['firstLineIn'] == True:
            if 'APEX_CODE' in line:
                context['firstLineIn'] = False
                levels = line.strip().split(' ')[1].replace(',','=').replace(';','  ')
                obj = {
                    'type':'LOGDATA',
                    'output':levels
                }
                debugList.append(obj)

                continue      
            else:
                obj = {
                    'type':'LOGDATA',
                    'output':line
                }
                debugList.append(obj)
                continue

        if context['lenChunks'] == 1:
            continue

        if len(chunks)>1 and chunks[1] in ['HEAP_ALLOCATE','STATEMENT_EXECUTE','VARIABLE_SCOPE_BEGIN','HEAP_ALLOCATE','SYSTEM_METHOD_ENTRY','SYSTEM_METHOD_EXIT','SOQL_EXECUTE_EXPLAIN','ENTERING_MANAGED_PKG','SYSTEM_CONSTRUCTOR_ENTRY','SYSTEM_CONSTRUCTOR_EXIT']:
            continue

        if '|SYSTEM_MODE_EXIT|' in line:
            nop=1

        if parseVariableAssigment(context):
            continue

        if parseLimits(context):
            continue
        if parseUserDebug(context):
            continue
        if parseUserInfo(context):
            continue
      #  parseUserDebug(context)
        if parseExceptionThrown(context):
            continue

        if parseSOQL(context)==True:
            continue

        if parseMethod(context):
            continue

        if parseDML(context):
            continue

        if parseConstructor(context):
            continue
        if parseCodeUnit(context):
            continue
        if parseConstructor(context):
            continue

        parseNamedCredentials(context)
        parseCallOutResponse(context)
        parseWfRule(context)
        parseFlow(context)
        

    if len(context['openItemsList']) > 0:
        a=1
    appendEnd(context)
 #   context['debugList'] = processRepetition(debugList)
 #   printDebugList(context)

    return context

def append_and_increaseIdent(context,obj,increase=True):
    context['openItemsList'].append(obj)
    if increase == True:
        increaseIdent(context)
    context['debugList'].append(obj)

def decreaseIdent_pop_setFields(context,type,value,key='key',endsWith=None,decrease=True):
    obj = popFromList(context,type=type,key=key,value=value,endsWith=endsWith)
    if obj == None:
        a=1
    else:
        if decrease == True:
            decreaseIdent(context)
        setTimes(context,context['line'],obj)
    return obj

def parseUserInfo(context):
    if '|USER_INFO|' in context['line']:
        obj = setTimes(context,context['line'],field='output',value=context['chunks'][4],type='USER_INFO')
        context['debugList'].append(obj)
        return True
    return False
#312780516
def appendEnd(context):

    for line in reversed(context['lines']):
        if '|' in line:
            break
    lastline = line
    obj = setTimes(context,lastline,type="END")
    obj['output'] = 'Final Limits'
    context['debugList'].append(obj)

def parseSOQL(context):
    line = context['line']
    chunks = context['chunks']
    if _isInOp(context,'SOQL_EXECUTE_BEGIN'):
  #  if context['lenChunks']>1 and chunks[1] == 'SOQL_EXECUTE_BEGIN':
   # if '|SOQL_EXECUTE_BEGIN|' in line:
        obj = setTimes(context,line,type="SOQL")
        obj['query'] = chunks[4]
        obj['object'] = chunks[4].lower().split(' from ')[1].strip().split(' ')[0]
        obj['apexline'] = chunks[2][1:-1]

        soql = obj['query'].lower()
        _from = soql.split(' from ')[-1].strip()
        _from = _from.split(' ')[0]

        obj['from'] = _from
        obj['output'] = f"Select: {obj['from']} --> No SOQL_EXECUTE_END found"

        append_and_increaseIdent(context,obj,increase=False)
        return True

    if context['lenChunks']>1 and chunks[1] == 'SOQL_EXECUTE_END':
 #   if '|SOQL_EXECUTE_END|' in line:
        context['totalQueries'] = context['totalQueries'] + 1
        obj = decreaseIdent_pop_setFields(context,type="SOQL",key='type',value='SOQL',decrease=False)
   #     if obj == None:
   #         return True
   #     print(chunks[0])
    #    if '30536880065' in chunks[0]:
    #        a=1
        obj['rows'] = chunks[3].split(':')[1]
        obj['output'] = f"Select: {obj['from']} --> {obj['rows']} rows"
        return True

    return False
def parseLimits(context):
    line = context['line']
    chunks = context['chunks'] 

    if '|LIMIT_USAGE|' in line:
        if '|SOQL|' in line:
            context[f'DEF:SOQL queries'] = chunks[4]

    if '|LIMIT_USAGE_FOR_NS|' in line:
        obj = setTimes(context,line,type='LIMIT')
        obj['output'] = f"{chunks[1].lower()}  {chunks[2]}"
        context['debugList'].append(obj)

        limits = chunks[2]
        if limits == '(default)':
            limitsNS = 'DEF:'
        elif limits == 'vlocity_cmt':
            limitsNS ='CMT:'
        else:
            limitsNS = f"{limits}:"

        next = 1
        nextline = context['lines'][context['num']+next]
        while '|' not in nextline:
            if 'SOQL queries' in nextline:
                nlchunks = nextline.split(' ')
                if int(context[f'{limitsNS}SOQL queries']) < int(nlchunks[6]):
                    context[f'{limitsNS}SOQL queries'] = nlchunks[6]
            if 'CPU time' in nextline:
                nlchunks = nextline.split(' ')

                if int(context[f'{limitsNS}CPU time']) < int(nlchunks[5]):
                    context[f'{limitsNS}CPU time'] = nlchunks[5]
            next = next + 1
            nextline = context['lines'][context['num']+next]

def parseLimitsX(context):
    line = context['line']
    chunks = context['chunks'] 

    if '*** getCpuTime() ***' in line:
        chs = chunks[4].split(' ')
        context[f'DEF:CPU time'] = chs[4]
    if 'CPU Time:' in line:
        chs = chunks[4].split(' ')
        context[f'DEF:CPU time'] = chs[2]    
    if '*** getQueries() ***' in line:
        chs = chunks[4].split(' ')
        context[f'DEF:SOQL queries'] = chs[4]

    if '|LIMIT_USAGE|' in line:
        if '|SOQL|' in line:
            context[f'DEF:SOQL queries'] = chunks[4]

    if '|LIMIT_USAGE_FOR_NS|' in line:
        limits = chunks[2]
        if limits == '(default)':
            context['limits_NS'] = 'DEF:'
        elif limits == 'vlocity_cmt':
            context['limits_NS'] = 'CMT:'
        else:
            context['limits_NS'] = f"{limits}:"


        limitsDict = setTimes(context,line,type='LIMITS')
        limitsDict['limitType'] = limits
        limitsDict['output'] = limitsDict['limitType']

    if 'limits_NS' in context and context['limits_NS']!=None and line == '':
        context['limits_NS'] = None
    
    if 'limits_NS' in context and  context['limits_NS'] != None:
        chunks = line.split(' ')
        limits = context['limits_NS']
        if 'SOQL queries' in line:
            if int(context[f'{limits}SOQL queries']) < int(chunks[6]):
                context[f'{limits}SOQL queries'] = chunks[6]
        if 'CPU time' in line:
            if int(context[f'{limits}CPU time']) < int(chunks[5]):
                context[f'{limits}CPU time'] = chunks[5]

    #dont know why this is here. Never reaches here.
    if 'limits_NS' in context and  context['limits_NS'] is not None and line =='':
        setTimes(context,limitsDict['lines'][0],limitsDict)
        s = f"limits-{limits.lower()} {limitsDict['time'][0]}"
        if context['printLimits'] == True:
            context['debugList'].append(limitsDict)
        context['limits'] = None   

def parseUserDebug(context):
    line = context['line']
    chunks = context['chunks']

    if '|USER_DEBUG|' in line:
        obj = setTimes(context,line,type='DEBUG')
        obj['type'] = 'DEBUG'
        obj['subType'] = chunks[3]
        obj['string'] = chunks[4]
        obj['output'] = obj['string'] 
        if obj['subType'] == 'ERROR':
            context['exception'] = True
            context['exception_msg'] = obj['output']
        obj['apexline'] = chunks[2][1:-1]
        context['debugList'].append(obj)
        if context['num']<(len(context['lines'])-1):
            next = 1
            nextline = context['lines'][context['num']+next]
            while '|' not in nextline:
                obj = context['debugList'][-1].copy()
                context['debugList'].append(obj)
                obj['string'] = nextline
                obj['output'] = nextline
                next = next + 1
                nextline = context['lines'][context['num']+next]

        if '*** getCpuTime() ***' in line:
            chs = chunks[4].split(' ')
            context[f'DEF:CPU time'] = chs[4]
        if 'CPU Time:' in line:
            chs = chunks[4].split(' ')
            context[f'DEF:CPU time'] = chs[2]    
        if '*** getQueries() ***' in line:
            chs = chunks[4].split(' ')
            context[f'DEF:SOQL queries'] = chs[4]

        return True

    return False
def parseUserDebugX(context):
    line = context['line']
    chunks = context['chunks']

    if '|' in line:   #This is a new line always. 
        if 'debug_multiLine' in context and context['debug_multiLine'] == True:
            a=1
        context['debug_multiLine'] = False

    if '|USER_DEBUG|' in line:
        context['debug_multiLine'] = True

    if 'debug_multiLine' in context and context['debug_multiLine'] == True:
        if '|' in line:
            obj = setTimes(context,line,type='DEBUG')
            obj['type'] = 'DEBUG'
            obj['subType'] = chunks[3]
            obj['string'] = chunks[4]
            obj['apexline'] = chunks[2][1:-1]
            if obj['subType'] == 'ERROR':
                context['file_exception']=True

        else:
            obj = context['debugList'][-1].copy()
            obj['string'] = line
        context['debugList'].append(obj)
        obj['output'] = obj['string'] 

def parseExceptionThrown(context):

    line = context['line']
    chunks = context['chunks']

    if context['lenChunks']>1 and chunks[1] == 'EXCEPTION_THROWN':
        obj = setTimes(context,line,type='EXCEPTION',field='output',value=chunks[3])
        context['exception'] = True
        context['exception_msg'] = obj['output']

        context['debugList'].append(obj)
        context['file_exception'] = True
        next = 1
        nextline = context['lines'][context['num']+next]
        while '|' not in nextline:
            if nextline != '':
                obj = context['debugList'][-1].copy()
                context['debugList'].append(obj)
                obj['output'] = nextline
            next = next + 1
            nextline = context['lines'][context['num']+next]
        return True

    if context['lenChunks']>1 and chunks[1] == 'FATAL_ERROR':
        obj = setTimes(context,line,type='EXCEPTION',field='output',value=chunks[2])
        context['exception'] = True
        context['exception_msg'] = obj['output']

        context['debugList'].append(obj)
        context['file_exception'] = True
        next = 1
        nextline = context['lines'][context['num']+next]
        while '|' not in nextline:
            if nextline != '':
                obj = context['debugList'][-1].copy()
                context['debugList'].append(obj)
                obj['output'] = nextline
            next = next + 1
            nextline = context['lines'][context['num']+next]
        return True
    return False
def _isInOp(context,text,contains=False):
    if context['lenChunks']<2:
        return False
    if contains:
        if text in context['chunks'][1]:
            return True
    elif context['chunks'][1] == text:
        return True
    return False
def parseWfRule(context):
    line = context['line']
    chunks = context['chunks'] 

    if _isInOp(context,'WF_RULE_EVAL',contains=True):
  #  if '|WF_RULE_EVAL' in line:
        if 'BEGIN' in chunks[1]:
            obj = setTimes(context,line,field='output',value='Workflow',type='RULE_EVAL')
            append_and_increaseIdent(context,obj)

        if 'END' in chunks[1]:
            decreaseIdent_pop_setFields(context,type='RULE_EVAL',key='output',value='Workflow')
        #    obj = getFromList(context['openItemsList'],'output','Workflow')
        #    setTimes(line,obj)

    if _isInOp(context,'WF_CRITERIA',contains=True):
  #  if '|WF_CRITERIA_' in line:
        if 'BEGIN' in chunks[1]:
            obj = setTimes(context,line,type='WF_CRITERIA')
            obj['nameId'] = chunks[2]
            obj['rulename'] = chunks[3]
            obj['rulenameId'] = chunks[4]
            obj['output'] = obj['rulename']

            append_and_increaseIdent(context,obj)

        if 'END' in chunks[1]:
            obj =decreaseIdent_pop_setFields(context,type='WF_CRITERIA',key='type',value='WF_CRITERIA')   
            obj['result'] = chunks[2]
            obj['output'] = f"{obj['rulename']} --> {obj['result']}"
  
    if _isInOp(context,'WF_RULE_NOT_EVALUATED'):
  #  if 'WF_RULE_NOT_EVALUATED' in line:
        obj =decreaseIdent_pop_setFields(context,type='WF_CRITERIA',key='type',value='WF_CRITERIA')   
        obj['output'] = f"{obj['rulename']} --> Rule Not Evaluated"

    if _isInOp(context,'WF_ACTION'):
 #   if '|WF_ACTION|' in line:
        obj = getFromList(context['openItemsList'],'output','Workflow',delete=False)
        obj['action'] = chunks[2]

def parseMethod(context):
    line = context['line']
    chunks = context['chunks'] 
    if context['lenChunks']>1 and 'METHOD_' in  chunks[1]:
        if len(chunks)<4:
            print(line)
            return

        operation = chunks[1]
        method = getMethod(line)

        if 'ENTRY' in operation:
            obj = setTimes(context,line,type='METHOD')
            obj['method'] = method
            obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'
            obj['output'] = obj['method']
            context['debugList'].append(obj)

            if '.getInstance' in method:
                pass
            else:
                context['openItemsList'].append(obj)
                increaseIdent(context)
            return True
        else:
            obj = getFromList(context['openItemsList'],'method',method)
            if obj == None:
                obj = getFromList(context['openItemsList'],'method',f"{method}",endsWith=True)

            if obj is not None:
                decreaseIdent(context)
                setTimes(context,line,obj)

            else:
                obj = setTimes(context,line,type='NO_ENTRY')
                obj['method'] = chunks[4]
                obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'
                context['debugList'].append(obj)

            if 'method' in obj:
                obj['output']=obj['method']
            else:
                obj['output']=obj['Id']
            return True
        return False
def parseVariableAssigment(context):
    line = context['line']
    chunks = context['chunks'] 

    if 'EXP_VAR' in context and context['EXP_VAR'] == True:
        if chunks[1] == 'VARIABLE_ASSIGNMENT' and chunks[2] == '[EXTERNAL]':
            obj = setTimes(context,line,type='VAR_ASSIGN')
            obj['type'] = 'VAR_ASSIGN'
            obj['subType'] = 'EXCEPTION'
            obj['string'] = chunks[4]
            obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'

            context['debugList'].append(obj)         
            obj['output'] = obj['string'] 

        else:
            context['EXP_VAR'] = False
        return False

    if _isInOp(context,'VARIABLE_ASSIGNMENT'):
        if len(chunks) >= 5:
            if 'ExecutionException' in chunks[4] or 'ExecutionException' in chunks[4]:
                obj = setTimes(context,line,type='VAR_ASSIGN')
                obj['type'] = 'VAR_ASSIGN'
                obj['subType'] = 'EXCEPTION'
                obj['string'] = chunks[4]
                obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'

                context['debugList'].append(obj)
                obj['output'] = obj['string'] 

                context['EXP_VAR'] = True
        return True
    return False
def parseDML(context):
    line = context['line']
    chunks = context['chunks']

    if _isInOp(context,'DML_BEGIN'):
 #   if '|DML_BEGIN|' in line:
        obj = setTimes(context,line,type="DML")
        obj['OP'] = chunks[3]
        obj['Type'] = chunks[4]
        obj['Id'] = chunks[2]
        obj['apexline'] = chunks[2][1:-1]
        obj['output'] = f"{obj['OP']} {obj['Type']}" 
        append_and_increaseIdent(context,obj)
        return True

    if _isInOp(context,'DML_END'):
  #  if '|DML_END|' in line:
        decreaseIdent_pop_setFields(context,'DML',key='Id',value=chunks[2])
        return True
    return False
def parseCallOutResponse(context):
    line = context['line']
    chunks = context['chunks']

    if _isInOp(context,'CALLOUT_RESPONSE'):
 #   if 'CALLOUT_RESPONSE' in line:
        obj = setTimes(context,line,type='CALLOUT')
        #  obj['type'] = 'DEBUG'
        #  obj['subType'] = chunks[3]
        obj['string'] = chunks[3]
        obj['apexline'] = chunks[2][1:-1]

        context['debugList'].append(obj)  
        obj['output'] = obj['string'] 

def parseConstructor(context):
    line = context['line']
    chunks = context['chunks']

    if _isInOp(context,'CONSTRUCTOR_ENTRY'):
  #  if '|CONSTRUCTOR_ENTRY|' in line:
        obj = setTimes(context,line,field='output',value=chunks[5],type='CONSTRUCTOR')
        obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'

        append_and_increaseIdent(context,obj)
        return True

    if _isInOp(context,'CONSTRUCTOR_EXIT'):
  #  if '|CONSTRUCTOR_EXIT|' in line:
        decreaseIdent_pop_setFields(context,type='CONSTRUCTOR',key='output',value=chunks[5])
        return True
    return False
def parseCodeUnit(context):
    line = context['line']
    chunks = context['chunks']

    if _isInOp(context,'CODE_UNIT_STARTED'):
  #  if '|CODE_UNIT_STARTED|' in line:
        obj = setTimes(context,line,type='CODE_UNIT')
        obj['output'] = chunks[4] if len(chunks)>4 else chunks[3]
        append_and_increaseIdent(context,obj)
        return True

    if _isInOp(context,'CODE_UNIT_FINISHED'):
  #  if '|CODE_UNIT_FINISHED|' in line:
        decreaseIdent_pop_setFields(context,'CODE_UNIT',key='output',value=chunks[2])
        return True
    return False
def parseNamedCredentials(context):
    line = context['line']
    chunks = context['chunks']

    if _isInOp(context,'NAMED_CREDENTIAL_REQUEST'):
 #   if '|NAMED_CREDENTIAL_REQUEST|' in line:
        obj = setTimes(context,line,field='output',value=chunks[2],type='NAMED_CRD')
        append_and_increaseIdent(context,obj)
        return True

    if _isInOp(context,'NAMED_CREDENTIAL_RESPONSE'):
 #   if "|NAMED_CREDENTIAL_RESPONSE|" in line:
        obj = decreaseIdent_pop_setFields(context,type='NAMED_CRD',key='type',value='NAMED_CRD')
        return True
    return False
def parseFlow(context):
    line = context['line']
    chunks = context['chunks']
    debugList = context['debugList']

    if 1==2:
        if '|FLOW_START_INTERVIEWS_BEGINxx|' in line:
            obj = setTimes(context,line,type='FLOW_START_INTERVIEWS',field='output',value='FLOW_START_INTERVIEWS')
            append_and_increaseIdent(context,obj)

        if '|FLOW_START_INTERVIEWS_ENDxx|' in line:
            decreaseIdent_pop_setFields(context,'FLOW_START_INTERVIEWS',key='output',value='FLOW_START_INTERVIEWS')

    if _isInOp(context,'FLOW_START_INTERVIEW_BEGIN'):
  #  if '|FLOW_START_INTERVIEW_BEGIN|' in line:
        obj = setTimes(context,line,type='FLOW_START_INTERVIEW')
        obj['Id'] = chunks[2]
        obj['Name'] = chunks[3]
        obj['output'] = obj['Name']
        obj['key'] = obj['Id']
        append_and_increaseIdent(context,obj)

    if _isInOp(context,'FLOW_START_INTERVIEW_END'):
 #   if '|FLOW_START_INTERVIEW_END|' in line:
        decreaseIdent_pop_setFields(context,'FLOW_START_INTERVIEW',value=chunks[2])

    if _isInOp(context,'FLOW_ELEMENT_ERROR'):
  #  if '|FLOW_ELEMENT_ERROR|' in line:
        obj = setTimes(context,line,type='FLOW_ELEMENT_ERROR')
        obj['message'] = chunks[2]
        obj['elementType'] = chunks[3]
        obj['elementName'] = chunks[4]
        obj['output'] = utils.CRED+ f"{obj['message']} in {obj['elementType']}:{obj['elementName']}" + utils.CEND
        debugList.append(obj)
        context['exception'] = True
        context['exception_msg'] = obj['output']

def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

def printDebugList(pc):
    logId = pc['logId']
    toFile= pc['writeToFile'] if 'writeToFile' in pc else False

    if toFile == True:
        filename = f"{restClient.logFolder()}{logId}_ansi.txt"

        original_stdout = sys.stdout
        with open(filename, 'w') as f:
            sys.stdout = f 
            _printDebugList(pc)
            sys.stdout = original_stdout 
        data = file.read(filename)
        html = ansi2html.Ansi2HTMLConverter().convert(data)
        filename = f"{restClient.logFolder()}{logId}.html"
        file.write(filename,html)
        print(f"Html file: {filename}")
        clean = escape_ansi(data)
        filename = f"{restClient.logFolder()}{logId}.txt"
        file.write(filename,clean)  
        print(f"Txt file: {filename}")
 
    else:
        colorama.just_fix_windows_console()
        _printDebugList(pc)

def _printDebugList(pc):
    logId = pc['logId'] if 'logId' in pc else None
    context = pc['context']
    onlyErrors = pc['onlyErrors'] if 'onlyErrors' in pc else False
    if context['exception'] == False and onlyErrors == True:
        return 
    print('___________________________________________________________________________________________________________________________________________________________________')
    if logId != None:
        print(logId)
    print()
    if logId != None:
        print(f"Parsing log Id {logId}    file: {restClient.logFolder()}{logId}.log")

    firstLines = True
    for num,d in enumerate(context['debugList']):
        if d['type'] == 'LOGDATA':
            print(d['output'])
            continue
        else:
            if firstLines == True:
                firstLines = False
                print()
                print()
        printLimits = pc['printLimits'] if 'printLimits' in pc else False
        if printLimits == False:
            if '*** getCpuTime() ***' in d['output']:
                continue
            if '*** getQueries() ***' in d['output']:
                continue
            if d['type'] == 'LIMIT':
                continue
        printParsedLog(pc,d)    
    print()
def processRepetition(debugList):
    def isRep(repss,x,parsedLine):
      if parsedLine['type'] not in ['METHOD','WF_CRITERIA']:
        return False,None

      for reps in repss:
        delta = reps[1]-reps[0]
        if x>= reps[0] and x <= reps[0] + len(reps) * delta - 1:
          if x>= reps[0] and x <= reps[0] + delta-1:
            if 'output' not in parsedLine:
                print()
            parsedLine['output'] = f"{parsedLine['output']}  *** {len(reps)},  {x-reps[0]+1}"
            if len(parsedLine['timeStamp'])>1:
                parsedLine['timeStamp'][1] = debugList[x+(len(reps)-1)*delta]['timeStamp'][1]
            return True,parsedLine
          else:
            return True,None

      return False,None

    for deb in debugList:
        if 'output' not in deb:
            print()
    repss = utils.repeatingSequence(debugList,"output")

    parsedX = []
    for x,parsedLine in enumerate(debugList):
        isrepe, obj = isRep(repss,x,parsedLine)
        if isrepe == True and obj == None:
            continue
        parsedX.append(parsedLine)

    return parsedX   

def getMethod(line):
    chunks = line.split('|')
    if len(chunks) == 4:
        method = chunks[3]
    else:
        method = chunks[4]
    if '(' in method:
        method = method.split('(')[0]
    return method

def getTime(line):
    chunks = line.split('|')
    return chunks[0].split(' ')[0]

def getTimeStamp(line):
    chunks = line.split('|')
    return int ((chunks[0].split('(')[1]).split(')')[0])

def increaseIdent(context):
    if context == None:
        context['ident'] = context['ident'] + 1
    else:
        context['ident'] = context['ident'] + 1

def decreaseIdent(context):
    if context == None:
        context['ident'] = context['ident'] - 1
    else:
        context['ident'] = context['ident'] - 1

def emptyString(context,size,char=' ',ident=None):
    str = ''
    if ident is None:
        ident = context['ident']
    length = ident * size
    for x in range(length):
        str = str + char  
    return str     

def rootString(context):
    str = ''
    length = context['ident'] 
    if length == 0:
        return ''
    for x in range(length-1):
        str = str + '⎮'
    str = str + '⌈' 

    return str     

def printParsedLog(pc,d):
    context = pc['context']
    Cinit = utils.CEND

    _plimit=' '
 

    if d['type'] == 'LIMITS':
        context['previousIsLimit'] = True
        return
    if context['previousIsLimit'] == True:
        _plimit = '*' 
        _context['previousIsLimit'] = False

    #levels
    if 'ident' not in d:
        print()
    level = d['ident']
    pcLevel = pc['level'] if 'level' in pc else None
    if pcLevel != None:
        if level > int(context['parseContext']['level']):
            return

    #colors
    _type = d['type']
    if _type == 'DEBUG':
        _type = f"{d['type']}-{d['subType']}"
        Cinit = utils.CRED if d['subType'] == 'ERROR' else utils.CGREEN
    elif d['type'] == 'EXCEPTION':
        Cinit = utils.CRED
    elif _type == 'VAR_ASSIGN':
        if d['subType'] == 'EXCEPTION':
            Cinit = utils.CRED
        else:
            return
    elif d['type'] == 'SOQL':
        Cinit = utils.CCYAN
    elif d['type'] == 'DML':
        Cinit =  utils.CYELLOW
    elif d['type'] == 'CODE_UNIT':
        Cinit =  utils.CPURPLE

    #i = f"{emptyString(1,' ',level)}."
    #i= level
    identation = f"{emptyString(context,3,' ',level)}"

    if 'output' not in d:
        print()
    val = d['output']

    if val == '':
        print()
    
    val = Cinit +f"{identation}{val}"

    _apexline = d['apexline'] if 'apexline' in d else ''

    _totalQueriesTrace = delta(d,'totalQueries') 
    spacer = '_' if d['type'] == 'SOQL' else '.'
    _totalQueriesTrace = f"{level:2}:{emptyString(context,1,spacer,level)}{_totalQueriesTrace}" if _totalQueriesTrace >0 else ' '

    _cpuTime0 = int(d['CPUTime'][0])
    _cpuTime1 = int(d['CPUTime'][1]) if len(d['CPUTime']) >1 else ''
    _timeStamp1 = d['timeStamp'][1] if len(d['timeStamp'])>1 else d['timeStamp'][0]

    _totalQueries0 = d['totalQueries'][0]
    _totalQueries1 = d['totalQueries'][1] if len(d['SOQLQueries']) >1 else _totalQueries0
    _totalQueriesD = _totalQueries1-_totalQueries0

    _cpuPrevD = _cpuTime0 - int(context['previousCPUTime'])

    if level == context['prevLevel']:
        _elapsedPrevD = d['timeStamp'][0] - context['prevTimes'][level][1]

    if level > context['prevLevel']:
        _elapsedPrevD = d['timeStamp'][0] - context['prevTimes'][context['prevLevel']][0]

    if level<context['prevLevel']:
        if level<0:
            a=1
        _elapsedPrevD = d['timeStamp'][0] - context['prevTimes'][level][1]

    if _elapsedPrevD <0:
        if '***' in d['output']:
            _elapsedPrevD = d['timeStamp'][0] - context['prevTimes'][level][0]

    context['prevTimes'][level] = [d['timeStamp'][0],_timeStamp1]

    _elapsedPrevD = ms(_elapsedPrevD)

    context['prevLevel'] = level

    _exp = "!" if d['exception'] == True else ''

    _sql2 = d['SOQLQueries'][1] if len(d['SOQLQueries'])>1 else ''
    _sqlcmt2 = d['cmtSOQLQueries'][1] if len(d['cmtSOQLQueries'])>1 else d['cmtSOQLQueries'][0]
  #  _sqlcmt2 = d['cmtSOQLQueries'][1] if len(d['cmtSOQLQueries'])>1 else ''

    context['previousCPUTime'] = _cpuTime0
    context['previousElapsedTime']  = d['elapsedTime']

    if d['type'] in ['SOQL','DML','VAR_ASSIGN'] and level == 0:
        _typeColor =utils. CYELLOW 
    else:
         _typeColor = ''

    if _cpuPrevD == 0 and _type != 'END':
        _cpuPrevD = ''
        _cpuTime0 = ''

    if _totalQueriesD==0:
        _totalQueriesD = ''
    if _totalQueries1 ==0:
        _totalQueries1 = ''
    if _sql2 ==0:
        _sql2=''
    if _sqlcmt2==0:
        _sqlcmt2=''
    _delta = f"{delta(d,'timeStamp')/1000000:.2f}"
    if _delta == "0.00":
        _delta =''

    if _type == 'END':
        _sql2 = d['SOQLQueries'][0]
        _cpuTime0 = d['CPUTime'][0]
        _sqlcmt2 = d['cmtSOQLQueries'][0]

    if context['firstLineOut'] == True:
        print(f"{'time(ms)':10}|{'elapsed':10}|{'time1(ns)':12}|{'time2(ns)':12}|{'t2-t1':10}|{'Qd':4}|{'Qt':4}|{'cpuD':6}|{'CPUin':6}|{'Q':3}|{'Qcm':3}|{'type':21}|{'al':4}{'':50}")
        context['firstLineOut'] = False

    if _type not in ['EXCEPTION','DEBUG-ERROR']:
        val = val[:150]
    if _type == 'DEBUG-ERROR':
        a=1
    print(f"{ms(d['elapsedTime']):10}|{_elapsedPrevD:8}|{d['timeStamp'][0]:12}|{_timeStamp1:12}|{_delta:>10}|{_totalQueriesD:4}|{_totalQueries1:4}|{_cpuPrevD:6}|{_cpuTime0:>6}|{_sql2:>3}|{_sqlcmt2:>3}|{_typeColor}{_type:21}{utils.CEND}|{_apexline:>4}| {val:50}"+utils.CEND)

def ms(val):
    return f"{val/1000000:10.2f}"

def popFromList(context,type,value,key='key',endsWith=False):
    openItemsList = context['openItemsList']
    try:
        for i,obj in enumerate(openItemsList):
            if obj['type'] == type:
                if endsWith == True:
                    if key not in obj:
                        continue
                    if obj[key].endswith(value) or obj[key].startswith(value):
                        openItemsList.pop(i)
                        return obj    
                else:
                    if key not in obj:
                        continue
                    if obj[key] == value:
                        openItemsList.pop(i)
                        return obj
    except Exception as e:
        print(e) 
    return None

def getFromList(theList,field,value,endsWith=False,delete=True):
    try:
        for i,obj in enumerate(theList):
            if field in obj:
                if endsWith == True:
                    if obj[field].endswith(value) or obj[field].startswith(value):
                        if delete == True:
                            theList.pop(i)
                        return obj    
                else:
                    if obj[field] == value:
                        if delete==True:
                            theList.pop(i)
                        return obj
    except Exception as e:
        print(e) 
    return None



