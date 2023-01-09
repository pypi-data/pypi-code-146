class Parser:
    def createContext(self):
        self.context = {
            'totalQueries' : 0,
            'timeZero':0,
            'ident':0,
            'DEF:SOQL queries' : 0,
            'DEF:CPU time' : 0,
            'CMT:SOQL queries' : 0,
            'CMT:CPU time' : 0,
            "exception":False,
            'totalQueries':0,
            'timeZero':0,
            'ident':0,
            'DEF:SOQL queries':0,
            'DEF:CPU time':0,
            'CMT:SOQL queries':0,
            'CMT:CPU time':0,
            'exception':False,
            'previousElapsedTime':0,
            'previousCPUTime':0,
            'previousIsLimit':0,
            'prevTimes':{
                0:[0,0]
            },
            'prevLevel':0,
            'firstLineIn':True,
            'firstLineOut':True
        }

    def parse(self,logId,logData,printLimits=True,userDebug=True,level=None,writeTofile=False):
        self.createContext()
        context = self.context
        context['printLimits'] = printLimits
        context['userDebug'] = userDebug
        context['logLevel'] = level

        context['lines'] = logData.splitlines()
        debugList = []

        print()

        context['debugList'] = debugList
        context['openItemsList'] = []

        for num,line in enumerate(context['lines']):
    #     print(num)

            chunks = line.split('|')
            context['chunks'] = chunks
            context['line'] = line
            context['num'] = num

            if context['firstLineIn'] == True:
                if 'APEX_CODE' in line:
                    context['firstLineIn'] = False
                    levels = line.strip().split(' ')[1].replace(',','=').replace(';','  ')
                    obj = {
                        'type':'LOGDATA',
                        'output':levels
                    }
                    continue      
                else:
                    obj = {
                        'type':'LOGDATA',
                        'output':line
                    }
                    debugList.append(obj)
                    continue


            if len(chunks)>1 and chunks[1] in ['HEAP_ALLOCATE','STATEMENT_EXECUTE','VARIABLE_SCOPE_BEGIN']:
                continue

            if '|SYSTEM_MODE_EXIT|' in line:
                nop=1

            parseUserInfo(context)

        # if '|' in line:   #This is a new line always. 
        #     multiLine = None
            
            parseExceptionThrown(context)
            parseVariableAssigment(context)
            parseLimits(context) 
            parseUserDebug(context)
            parseNamedCredentials(context)
            parseCallOutResponse(context)
            parseWfRule(context)
            parseConstructor(context)
            parseFlow(context)
            parseCodeUnit(context) 
            parseDML(context)
            parseSOQL(context)
            parseMethod(context)

        appendEnd(context)
        
        context['debugList'] = processRepetition(debugList)
        printDebugList(context,logId,writeTofile)

        print()

        return context

