from InCli.SFAPI import restClient ,utils,file,jsonFile,query,thread

import unittest,logging,os,shutil

class Test_Overrides(unittest.TestCase):
    def call_ServicesData(self):
        action = '/services/data'
        call = restClient.callAPI(action)
        self.assertTrue(len(call)>0)  

    def test_configFile(self):
        restClient.setLoggingLevel(logging.INFO)
        try:
            restClient.setConfigFile('sss')
        except Exception as e:
            utils.printException(e)
            self.assertTrue(e.args[0]['errorCode'] == 'NO_CONFIG')

        restClient.setConfigFile('/Users/uormaechea/Documents/Dev/python/Industries/config/ConnectionsParams.json')

        try:
            restClient.initWithConfig('XXXX')
        except Exception as e:
            utils.printException(e)
            self.assertTrue(e.args[0]['errorCode'] == 'NO_ORG')

        try:
            restClient.initWithConfig('NOSDEV')
            self.assertTrue(restClient._currentConnectionName=='NOSDEV')

            folder = restClient.debugFolder()

            st = '2222222'
            file.write(f"{folder}test.txt",st)
            st2 = file.read(f"{folder}test.txt")
            self.assertTrue(st==st2)

            
        except Exception as e:
            utils.printException(e)
            self.assertTrue(1==2)
        print()

    def test_debug_action(self):
     #   restClient.setConfigFile('/Users/uormaechea/Documents/Dev/python/Industries/config/ConnectionsParams.json')
        restClient.init("DEVNOSCAT2")   
        action = '/services/data'

        #Test  callAPI_debug 
        call = restClient.callAPI(action)
        self.assertTrue(len(call)>0)    
        restClient.callSave("testFile")
        lc = restClient.lastThreadCall()

        self.assertTrue('responseFilePath' in lc)
        fileContent = jsonFile.read(lc['responseFilePath'])

        self.assertEqual(call,fileContent)

        q = query.query(" select fields(all) from Account limit 1")
        print(q)

 
    def test_debug_guest(self):
        restClient.setConfigFile('/Users/uormaechea/Documents/Dev/python/Industries/config/ConnectionsParams.json')

        restClient.initWithConfig('DEVNOSCAT2_GUEST')
        action = '/services/data'
        call = restClient.callAPI(action)
        self.assertTrue(len(call)>0)    

        try:
            q = query.query(" select fields(all) from Account limit 1")
        except Exception as e:
            utils.printException(e)
            self.assertTrue(e.args[0]['errorCode'] ==  'HTTPs Error: 401')

    def test_debug_withToken(self):
        restClient.setLoggingLevel(logging.DEBUG)
        restClient.init('DEVNOSCAT2')
        
        action = '/services/data'

        call = restClient.callAPI(action)
        self.assertTrue(len(call)>0)  
        
        url = restClient._initializedConnections[0]['instance_url']
        token = restClient._initializedConnections[0]['access_token']
    
        restClient.initWithToken('test',url,token=token)
        self.assertTrue(restClient._currentConnectionName == 'test')
        call = restClient.callAPI(action)
        self.assertTrue(len(call)>0)  

        q = query.query(" select fields(all) from Order limit 1")
        print(q)

    def test_debug_threaded(self):
        restClient.init("DEVNOSCAT2") 

        a = [1]*100

        allTimes = []
        def doWork(a):
            action = '/services/data'
            call = restClient.callAPI(action)
            times= {
                "elapsed":restClient.getlastThreadCallTime()
            } 
            allTimes.append(times)

        thread.processList(doWork,a,10)

        utils.printFormated(allTimes)

    def test_login_sfdx(self):
        try:
            outputs = utils.executeCommandParse(["sfdxXXXX","auth:web:login","-r", "https://nos--devnoscat2.sandbox.my.salesforce.com"])
        except Exception as e:
            self.assertTrue(e.strerror ==  'No such file or directory')
            utils.printException(e)

        try:
            restClient.init("xxx.xxx@nos.pt")

        except Exception as e:
            self.assertTrue(e.args[0]['errorCode'] ==  'ConnectionError')
            utils.printException(e)

        try:            
            restClient.init("uormaechea.devnoscat2@nos.pt")
            q = query.query(" select fields(all) from Order limit 1")
            lc = restClient.lastThreadCall()
            self.assertEqual(lc['status_code'],200)
            print(q)

        except Exception as e:
            self.assertEqual('This','Should not happen')

    def test_congifData(self):        
        return
        dir = os.path.abspath("tmp")
        try:
            os.mkdir(dir)
        except Exception as e:
            self.assertTrue(e.strerror=='File exists')
        os.chdir(dir)
        current = os.getcwd()

        config = restClient.loadConfigData()

        self.assertTrue('orgs' in config)
        self.assertTrue(file.exists(restClient._configDataName))

        shutil.rmtree(current)


    def test_saveOrg(self):
        restClient.init("DEVNOSCAT2") 

        url = restClient._initializedConnections[0]['instance_url']
        token = restClient._initializedConnections[0]['access_token']

        restClient.saveOrg_inConfigFile('test1',url,token)
        restClient.initWithConfig('test1')
        self.assertTrue(restClient._currentConnectionName=='test1')
        self.call_ServicesData()

        restClient.saveOrg_inConfigFile('testGuest',url)
        restClient.initWithConfig('testGuest')
        self.assertTrue(restClient._currentConnectionName=='testGuest')
        self.call_ServicesData()
        try:
            q = query.query(" select fields(all) from Order limit 1")
        except Exception as e:
            self.assertEqual(e.args[0]['errorCode'],'HTTPs Error: 401')
            utils.printException(e)

    def test_saveDeleteOrg(self):
        restClient.saveOrg_inConfigFile('test1','xxx','yyyy')

        cd = restClient.loadConfigData()
        org = [i for i in cd['orgs'] if (i['name'] == 'test1')][0]
        self.assertTrue(org['name'] == 'test1')
        restClient.deleteOrg_inConfigFile('test1')
        cd = restClient.loadConfigData()
        org = [i for i in cd['orgs'] if (i['name'] == 'test1')]
        self.assertTrue(len(org)==0)
        print()

