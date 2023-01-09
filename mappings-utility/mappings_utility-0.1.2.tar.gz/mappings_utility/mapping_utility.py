import pandas as pd
import collections as coll


class MappingUtility():
  '''An object to do operations on a key-to-key mapping table
  initialise with the mapping table, a list of source column headers and a list of target column headers
  '''

  def __init__(self, mappingDataFrame: pd.DataFrame, sourceList: list, targetList: list):
      self.mappingDafaFrame = mappingDataFrame
      self.sourceList = sourceList
      self.targetList = targetList
  
  @classmethod
  def from_csv(class_object, path: str, sourceList: list, targetList: list):
      return class_object(pd.read_csv(path), sourceList, targetList)


  @classmethod
  def from_dict(class_object, mappingDict: dict , sourceList: list, targetList: list):  
      return class_object(pd.DataFrame(mappingDict), sourceList, targetList)


  def generateGroupDimension(self, fromList: list):
      if not all(e in (self.sourceList + self.targetList) for e in fromList):
        raise ValueError('at least one of the names do not exist in the mapping dataframe')

      return self.mappingDafaFrame[fromList].apply(lambda x: pd.Series('.'.join(x), index=['.'.join(fromList)]), axis=1).iloc[:,0]


  def maxTargetVariation(self, sourceCodes, targetCodes):
      if not (isinstance(sourceCodes, list) and isinstance(targetCodes, list)):
        raise TypeError('inputs should be lists')
      
      #print(sourceCodes, targetCodes)
      uniquecombinations = { '.'.join((x,y)) : x for x, y in zip(sourceCodes, targetCodes)}
      countedsources = coll.Counter(uniquecombinations.values())
      return max(countedsources.values())

  def analyseOneToOneCompatibility(self):
      otoc = pd.DataFrame(index= self.sourceList, columns= self.targetList)
      for k in self.sourceList:
        for l in self.targetList:
          otoc.at[k,l] = self.maxTargetVariation( self.mappingDafaFrame[k].values.tolist(), self.mappingDafaFrame[l].values.tolist())    
     
      return otoc
  

  def getMinimumCompatibilitySet(self, targetDimension):
      sourceDims = self.generateGroupDimension(self.sourceList).values.tolist()
      targetDim = self.mappingDafaFrame[targetDimension].values.tolist()

      if self.maxTargetVariation(sourceDims, targetDim) != 1:
         raise Exception('Sources do not have enough variation for target. No solution found.') 

      lsCore = self.sourceList.copy()
      #'iterate through source and drop unnecessary ones one by one

      for i, v in reversed(list(enumerate(lsCore))):
        lsCoreTemp = lsCore.copy()
        if len(lsCoreTemp)> 1:
          lsCoreTemp.pop(i)
          if self.maxTargetVariation(self.generateGroupDimension(lsCoreTemp).values.tolist(), targetDim) == 1: 
            lsCore.pop(i)
    
      return lsCore

if __name__ == "__main__":      

    # ---------------The code from here is used for illustration of the class and could be translated into test cases----------------
    dictMapping = {'Indicator':['MP','MS','EP','ES','MP','MP'], 'Activity':['C','C','D','D','C','C'],'Measure':['P','S','P','S','P','P']}
    testdf = pd.DataFrame(dictMapping)

    print('\n Mapping tables')
    testMU = MappingUtility(testdf, ['Activity','Measure'], ['Indicator'])
    print(testMU.mappingDafaFrame)

    file_loc = "https://raw.githubusercontent.com/OECDSTD/SampleFilesForColab/main/test-mapping.csv"
    test2MU = MappingUtility.from_csv(file_loc,['DOMAIN', 'SUBJECT_S', 'COICOP', 'ACTIVITY', 'ADJUSTMENT_S','UNIT_MEASURE', 'BASE_PERIOD'], ['SUBJECT_T', 'ADJUSTMENT_T', 'UNIT', 'MEASURE'])
    print(test2MU.mappingDafaFrame)

    print('\n Dimension group example')
    gd = testMU.generateGroupDimension(['Activity','Measure'])
    print(gd)

    print('\n Single compatibility check between Activity and Indicator')
    print(testMU.maxTargetVariation(testMU.mappingDafaFrame['Activity'].values.tolist(), testMU.mappingDafaFrame['Indicator'].values.tolist()))

    print('\n Full compatibility check')
    print(testMU.analyseOneToOneCompatibility())
    print(test2MU.analyseOneToOneCompatibility())

    print('\n Generate the minimum set of source variables needed to describe a given target dimension')
    print('Indicator:', testMU.getMinimumCompatibilitySet('Indicator'))
    print('SUBJECT_T:', test2MU.getMinimumCompatibilitySet('SUBJECT_T'))
