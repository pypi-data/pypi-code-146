import json
from .SFAPI import Sobjects, query,restClient,jsonFile,utils,objectUtil,debugLogs,digitalCommerceUtil
import logging
import simplejson,sys
from operator import itemgetter
from inspect import getmembers, isfunction
import traceback
import colorama

varsFile = 'confIcli.json'
vars = None


def readVars(field=None):
    global vars
    vars = jsonFile.read(varsFile)

    if field != None:
        return vars[field]
    return vars

def setVar(name,value):

    vars = jsonFile.read(varsFile)
    vars[name]=value
    jsonFile.write(varsFile,vars)
    print(simplejson.dumps(vars, indent=4))

def getParam(argv,key,i=1):
    if key not in argv:
        return None

    ind = argv.index(key)
    if (ind+i <= (len(argv)-1)):
        arg = argv[ind+i]
        if arg[0] == '-':
            return None
        return arg
    return None

def listEnvs():
    cons = restClient.getConfigOrgs()
    cons = sorted(cons,key=itemgetter('name'))
    utils.printFormated(cons,fieldsString='name:isSandBox:instance_url:login.username:login.password:login.bearer')
    env = readVars('environment')
    print(f"Current Environment is {env}")

def _queryAndPrint(q,fields=None,systemFields=True,nullFields=False):

    res = query.queryRecords(q)
    if fields != None:
        res = utils.deleteNulls(res,systemFields,nullFields)
        if fields=='all':
            utils.printFormated(res)
        else:
            utils.printFormated(res,fields)
    else:
        res = utils.deleteNulls(res,systemFields,nullFields)
        print(simplejson.dumps(res, indent=4))
    
    print()
    print(f"Null values printed-> {nullFields}  systemFields printed--> {systemFields}")

def option_q(args):
    if '-h' in args:
        help = f"""
        {utils.CYELLOW}-q "select..."{utils.CEND} query to execute. System Fields, such as LastModifiedDate, and null fields are not returned. 
            {utils.CYELLOW}-null{utils.CEND} - will print fields with null values
            {utils.CYELLOW}-system{utils.CEND} - will print the system fields
            {utils.CYELLOW}-all{utils.CEND} - will print both nulls and system fields
            {utils.CYELLOW}-fields "a:b:c:..."{utils.CEND} --> print in table format the specified fields.
            {utils.CYELLOW}-fields all{utils.CEND} --> print in table format"""
        return help

    #else:
    q = getParam(args,'-q')

    fields = getParam(args,'-fields') if '-fields' in args else None    
    nullFields = True if '-null' in args else False
    systemFields = True if '-system' in args else False
    all = True if '-all' in args else False
    if all == True:
        nullFields = True
        systemFields = True

    connectionInit(args)

    _queryAndPrint(q,fields=fields,systemFields=systemFields,nullFields=nullFields)

def option_cc(args):
    colorama.just_fix_windows_console()

    if '-h' in args:
        help = f"""
        {utils.CYELLOW}-cc{utils.CEND} 
            Checks the catalogs. Gets all catalogs, does a getOffers, getOfferDetails. Performs basketwithoutconfig and basket with config, if -basket is set. 
            {utils.CYELLOW}-code{utils.CEND} - Catalogue Code. does it for a single catalog. 
            {utils.CYELLOW}-list{utils.CEND} - List all the catalogues. 
            {utils.CYELLOW}-basket{utils.CEND} - Performs basket operations. """ 

        return help

    connectionInit(args)

   # path = getParam(args,'-checkCatalogs')
   # quantity = getParam(args,'-checkCatalogs',2)
    catcatalogueCode = getParam(args,'-code')
    list = True if '-list' in args else False
    basketOps = True if '-basket' in args else False

    account = getParam(args,'-account')

    if list == True:
        digitalCommerceUtil.printCatalogs()
        return

    digitalCommerceUtil.checkOffers(catcatalogueCode=catcatalogueCode,account=account,basketOps=basketOps)

    print()

def option_d(args):
    help = f"""
        {utils.CYELLOW}-d objectName{utils.CEND} --> Describe an object
            {utils.CYELLOW}-d objectName:fieldName{utils.CEND} --> describe a field in the object"""
    if '-h' in args:
        return help    

    connectionInit(args)

    objectField = getParam(args,'-d')
    if objectField == None:
        print(help)
        return

    ofs = objectField.split(':')

    sObjectName = ofs[0]
    fieldName = ofs[1] if len(ofs) > 1 else None

    res = Sobjects.describe(sObjectName)
    if fieldName == None:
        print(simplejson.dumps(res['fields'], indent=4))
    else:
        sibbling = objectUtil.getSiblingWhere(res['fields'],'name',fieldName)['object']

        print(simplejson.dumps(sibbling, indent=4))

def option_l(args):
    if '-h' in args:
        help = f"""
        {utils.CYELLOW}-l{utils.CEND} --> current org limits consuptions. """
        return help
    connectionInit(args)
    action = '/services/data/v51.0/limits'
    res = restClient.callAPI(action)
    records = []
    for key in res.keys():
        record = {
            'Limit':key,
            'Max':res[key]['Max'],
            'Remaining':res[key]['Remaining'],
        }
        record['Percent Remaining'] =  100 *(res[key]['Remaining']/res[key]['Max']) if res[key]['Max']>0 else 0
        record['__color__'] = ''

        if record['Max'] != 0:
            if record['Percent Remaining']<50:
                record['__color__'] = utils.CYELLOW
            if record['Percent Remaining']<25:
                record['__color__'] = utils.CYELLOW
        records.append(record)

    utils.printFormated(records)

def option_o(args):
    if '-h' in args:
        help = f"""
        {utils.CYELLOW}-o{utils.CEND} --> List all Objects
            {utils.CYELLOW}-name objectName{utils.CEND}  --> get one row from the object
            {utils.CYELLOW}-name objectName:Id{utils.CEND} --> get the row especified by the Id
            {utils.CYELLOW}-like name{utils.CEND} --> where the Name contains the substring name"""

        return help
        
    connectionInit(args)

    if '-name' in args:
        obj = getParam(args,'-name')
        chunks = obj.split(':')

        if len(chunks) == 1:
            q = f"select fields(all) from {chunks[0]} limit 1"
        else:
            q = f"select fields(all) from {chunks[0]} where Id='{chunks[1]}'"

        print('pre q:'+q)
        _queryAndPrint(q,systemFields=True,nullFields=True)
        return
        
    like = getParam(args,'-like') if '-like' in args else None    
    count = True if '-count' in args else False   

    objs = Sobjects.listObjects()
    if like is not None:
        if ':' not in like:
            like = f"name:{like}"        
        ls = like.split(':')
        outs = []
        for obj in objs:
      #      print(f"{str(ls[1])} . {str(obj[ls[0]])}")
            if str(ls[1]).lower() in str(obj[ls[0]]).lower():
                outs.append(obj) 
    else:
        outs = objs

    if count==True:
        for out in outs:
            if out['queryable'] == True:
                print("Quering objects row count.")
                print("", end=".")          
                try:
                    if out['name'] == 'AccountUserTerritory2View':
                        print()
                    c = query.query(f" select count(Id) from {out['name']}",raiseEx=True)
                    out['count'] = c['records'][0]['expr0']
                except Exception as e:
                    out['count'] = 'E'
            else:
                out['count'] = '-'
    
    #print(simplejson.dumps(objs, indent=4))
    utils.printFormated(outs,'name:label:associateParentEntity:associateParentEntity:queryable:count')

def option_default(args):
    help = f"""
        {utils.CYELLOW}-default:set key value{utils.CEND} --> defaults the specified key-value
        {utils.CYELLOW}-default:del key  {utils.CEND}  --> deletes the default
        {utils.CYELLOW}-default:get key  {utils.CEND}  --> displays the current value"""

    if '-h' in args:
        return help   

    if "-default:del" in args:
        key = getParam(args,'-default:del',1)
        if key == None:
            restClient.glog().info(f'Key not found in the provided arguments. {args}')
            return 
        restClient.delConfigVar(key)
        return

    if "-default:set" in args: 
        key = getParam(args,'-default:set',1)
        value = getParam(args,'-default:set',2)
        if key == None or value==None:
            print(help)
            return

        restClient.setConfigVar(key,value)
        print(f"Default value for {key} is {value}")

    if "-default:get" in args: 
        key = getParam(args,'-default:get',1)
        value =restClient.getConfigVar(key)
        print(f"Default value for {key} is {value}")

#def option_history(args):
#    return
#    if '-h' in args:
        help = """
        -history"""
        return help
#    print()
#    print('HISTORY:')
#    vars = jsonFile.read(varsFile)
#    for line in vars['history']:
        print(line)

def option_logs(args):
    help = f"""
        {utils.CYELLOW}-logs Id{utils.CEND} --> parse the log with the provided Id. No modifiers.
        {utils.CYELLOW}-logs inputfile {utils.CEND}--> parses the file provided in the inputfile. {utils.CGREEN}InCli -logs -inputfile "path to file/xxxx.log"{utils.CEND} No modifiers.
        {utils.CYELLOW}-logs store {utils.CEND}--> parses the files saved locally in order of creation(download) 
            {utils.CYELLOW}-error {utils.CEND}--> parses the files saved locally and displays only the ones with errors. {utils.CGREEN}InCli -logs -store -error "{utils.CEND} 
        {utils.CYELLOW}-logs -last X {utils.CEND}--> parses the last X logs. X as number.
        {utils.CYELLOW}-logs -tail {utils.CEND}--> activelly parsers new debug logs as they are created.
            {utils.CYELLOW}-deletelogs {utils.CEND}--> as log files are processed, they are deleted from the server. The local copy remains. 
            {utils.CGREEN}-logs -u OrgAlias -where "LogLength>3000"  -tail -deletelogs{utils.CEND} -> parses log files of size > 3000 as they are created. Deletes the retrieved logs. 
        {utils.CYELLOW}-logs{utils.CEND} --> lists log records in the org. 
            {utils.CYELLOW}-limit X{utils.CEND}, where X specifies the number of logs to list. Default 50 max 50K
                {utils.CGREEN}-logs -limit 1000{utils.CEND}, displays the last 1000 log records
            Modifiers:
            {utils.CYELLOW}-loguser field:value{utils.CEND}, filter the logs for the specified user. The user can be specified by any field in the User Object. 
                {utils.CGREEN}-loguser Id:0053O000000IHneQAG, -loguser "name:Onboarding Site Guest User", -loguser Alias:John.Doe, -loguser FirstName:Onboarding, -loguser ProfileId:00e3O000000IHneQAG{utils.CEND}
                {utils.CGREEN}Defaultable loguser{utils.CEND}: Can be set to default. {utils.CGREEN}-default:set loguser "Alias:John.Doe{utils.CEND}"
            {utils.CYELLOW}-where X {utils.CEND}--> the where clause for a query.  
                {utils.CGREEN}InCli -logs -loguser Alias:John.Doe -where="Status<>'Success" -last 10" {utils.CEND} --> parses the last 10 logs for user John.Doe where the status is not Success
            {utils.CYELLOW}-file {utils.CEND}--> creates 2 files for the parsed file, txt and html format. 
            {utils.CYELLOW}-limitinfo {utils.CEND}--> prints the times when the limits (CPU, SOQL) are parsed.  """


    if '-h' in args:
        return help

    logId = getParam(args,'-logs')    
    last = getParam(args,'-last')  
    limit = getParam(args,'-limit')    
    limitInfo = True if '-limitinfo' in args else False   

    level = getParam(args,'-level') 
    loguser = getParam(args,'-loguser') 
    whereClause = getParam(args,'-where') 
    toFile = True if '-file' in args else False
    inputfile = getParam(args,'-inputfile') 
    tail = True if '-tail' in args else False
    deletelogs = True if '-deletelogs' in args else False
    store = True if '-store' in args else False
    error = True if '-error' in args else False

    if loguser == None:
        loguser = restClient.getConfigVar('loguser')

    if logId == None and last== None and inputfile==None and tail == False and store==False:
        connectionInit(args)
        lim = 50 if limit == None else limit

        return debugLogs.printLogRecords(loguser=loguser,limit=lim,whereClause=whereClause)

    parseContext = {
        'logId' :logId,
        'filepath':inputfile,
        'printLimits':limitInfo,
        'lastN':last,
        'loguser':loguser,
        'level':level,
        'whereClause':whereClause,
        'writeToFile':toFile,
        'tail':tail,
        'deleteLogs':deletelogs,
        'parseStore':store,
        'logToStore':True,
        'onlyErrors':error,
        'operation':None
    }

    if tail:
        connectionInit(args)
        return debugLogs.parseTail(parseContext)

    elif store:
        return debugLogs.parseStorage(parseContext)

    elif inputfile != None:
        return debugLogs.parseFile(parseContext)

    elif logId != None:  #check if already downloaded        
        connectionInit(args)
        return debugLogs.parseLogId(logId,parseContext)
    else:
        connectionInit(args)
        return debugLogs.parseLogs_LastN(parseContext)

def option_h(args):

    module = __import__('InCli')

    funcs = getmembers(sys.modules[__name__], isfunction)
    functions = [func[0] for func in funcs if func[0].startswith('option_')]

    for f in functions:
        if f == 'option_h':
            continue

        print(eval(f'{f}(args)'))      
    print()

def connectionInit(argsIn):

    userName_or_ofgAlias = getParam(argsIn,'-u') 
    restClient.init(userName_or_ofgAlias)

def checkVersion():
    try:
        from importlib import metadata
    except ImportError:
        import importlib_metadata as metadata

    fileversion = metadata.version("InCli")

    try:
        restClient.init('ConnectionLess')
        restClient.glog().info("Checking version")
        res = restClient.requestRaw(url='https://pypi.org/pypi/InCli/json')
        version = res['urls'][1]['filename'].split('-')[1].split('.tar')[0]

        if version != fileversion:
            print()
            print(f"Version {fileversion}. {colorama.Fore.WHITE+colorama.Back.RED}Version {version} is available --> pip install InCli --upgrade{utils.CEND}")
        else:
            print()
            print(f"InCli version {fileversion} ")
    except Exception as e:
        print(e)

def _main(argsIn):

    if "-debug" in argsIn:
        restClient.setLoggingLevel(level=logging.DEBUG)
    else:
        restClient.setLoggingLevel(logging.INFO)

    restClient.glog().debug("In debug mode")
    checkVersion()

    if '-h' in argsIn:
        colorama.just_fix_windows_console()

        help = f"""
        {utils.CYELLOW}-u{utils.CEND} --> username or org alias to be used to log into the org. 
            {utils.CGREEN}Defaultable u{utils.CEND}: Can be set to a default value --> {utils.CGREEN}InCli -default:set u "xx@adas.com {utils.CEND}"""
        print(help)

    funcs = getmembers(sys.modules[__name__], isfunction)
    functions = [func[0] for func in funcs if func[0].startswith('option_')]

    args = []
    for argv in argsIn:
        if argv == '|':
            break
        args.append(argv)

    for arg in args:
        ar = arg.split(':')[0][1:]
        ar = f"option_{ar}"
        if ar in functions:
        #       module = __import__('InCli')
            res = None
            res = eval(f'{ar}(args)')
            if '-h' not in argsIn:
                return res
        #      func = getattr(module, ar)
        #      func(args)

    if '-h' in argsIn:
        print()
        print(utils.CBOLD+"SFDX Commands:"+utils.CEND)
        print(f" - {utils.CYELLOW}sfdx force:org:list --verbose --all {utils.CEND}--> to list all authorized Orgs and Connection Status")
        print(f" - {utils.CYELLOW}sfdx auth:web:login -r 'Instance Url' -a 'Alias' {utils.CEND}--> to re-authorize")
        print(f" - {utils.CYELLOW}sfdx auth:web:login -u 'userName'  -a 'alias' {utils.CEND}--> to authorize and Org")
        print()

def main():
    argsIn = sys.argv

    try:
        _main(argsIn)

    except KeyboardInterrupt as e:
        print()
        print("ate ja")
    except Exception as e:
        utils.printException(e)
        if "-debug" in sys.argv:
            print(traceback.format_exc())

if __name__ == '__main__':
    main()

