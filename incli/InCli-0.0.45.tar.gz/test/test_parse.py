import unittest
from InCli.SFAPI import restClient,CPQ,account,Sobjects,utils,query,jsonFile,debugLogs
import traceback


class Test_Parse(unittest.TestCase):

    def isRep(self,repss,x,parsedLine):
      if parsedLine['type'] != 'METHOD':
        return False,None

      for reps in repss:
        delta = reps[1]-reps[0]
        if x>= reps[0] and x <= reps[0] + len(reps) * delta - 1:
          if x>= reps[0] and x <= reps[0] + delta-1:
            parsedLine['output'] = f"{parsedLine['output']}  *** {len(reps)}"
            return True,parsedLine
          else:
            return True,None

      return False,None


    def test_findRepeating(self):

      #  objs = jsonFile.read('/Users/uormaechea/Documents/Dev/python/VirtualEnvs/prj1/.incli/logs/07L3O00000Dg1OSUAZ')

      try:
        logId = '07L3O00000Dg1OSUAZ'
        parseContext = {
          'filepath':f'/Users/uormaechea/Documents/Dev/python/VirtualEnvs/prj1/.incli/logs/{logId}.log'
        }
        parsed = debugLogs.parseFile(parseContext) #.parseLog(filepath=f'/Users/uormaechea/Documents/Dev/python/VirtualEnvs/prj1/.incli/logs/{logId}.log')

        repss = utils.repeatingSequence(parsed,"output")

        parsedX = []
        for x,parsedLine in enumerate(parsed):
          isrepe, obj = self.isRep(repss,x,parsedLine)
          if isrepe == True and obj == None:
            continue
          parsedX.append(parsedLine)
        debugLogs.printDebugList(parsedX,logId)    
      

      except Exception as e:
        print(e)
        print(traceback.format_exc())

    def test_parseStorage(self):
      try:
        restClient.init('ConnectionLess')
        debugLogs.parseStorage()
      except Exception as e:
        print(e)
        traceback.format_exc()

      print()
        



