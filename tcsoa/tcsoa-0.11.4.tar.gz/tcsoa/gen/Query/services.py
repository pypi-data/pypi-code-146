from tcsoa.gen.Query._2013_05.services import SavedQueryService as imp0
from tcsoa.gen.Query._2007_01.services import SavedQueryService as imp1
from tcsoa.gen.Query._2006_03.services import SavedQueryService as imp2
from tcsoa.gen.Query._2018_11.services import SavedQueryService as imp3
from tcsoa.gen.Query._2019_06.services import SavedQueryService as imp4
from tcsoa.gen.Query._2020_04.services import SavedQueryService as imp5
from tcsoa.gen.Query._2010_09.services import SavedQueryService as imp6
from tcsoa.gen.Query._2007_06.services import SavedQueryService as imp7
from tcsoa.gen.Query._2007_09.services import SavedQueryService as imp8
from tcsoa.gen.Query._2008_06.services import SavedQueryService as imp9
from tcsoa.gen.Query._2010_04.services import SavedQueryService as imp10
from tcsoa.gen.Query._2007_06.services import FinderService as imp11
from tcsoa.gen.Query._2014_11.services import FinderService as imp12
from tcsoa.gen.Query._2012_10.services import FinderService as imp13
from tcsoa.base import TcService


class SavedQueryService(TcService):
    createSavedQueries = imp0.createSavedQueries
    deleteQueryCriterias = imp1.deleteQueryCriterias
    describeSavedQueries = imp2.describeSavedQueries
    executeBOQueriesWithContext = imp3.executeBOQueriesWithContext
    executeBOQueriesWithSort = imp4.executeBOQueriesWithSort
    executeBOQueriesWithSortAndContext = imp5.executeBOQueriesWithSortAndContext
    executeBusinessObjectQueries = imp6.executeBusinessObjectQueries
    executeSavedQueries = imp7.executeSavedQueries
    executeSavedQueries2 = imp8.executeSavedQueries
    executeSavedQueries3 = imp9.executeSavedQueries
    executeSavedQuery = imp2.executeSavedQuery
    findSavedQueries = imp10.findSavedQueries
    getSavedQueries = imp2.getSavedQueries
    reorderSavedQueryCriterias = imp1.reorderSavedQueryCriterias
    retrieveQueryCriterias = imp1.retrieveQueryCriterias
    retrieveSearchCriteria = imp7.retrieveSearchCriteria
    saveQueryCriterias = imp1.saveQueryCriterias
    saveSearchCriteria = imp7.saveSearchCriteria


class FinderService(TcService):
    findWorkspaceObjects = imp11.findWorkspaceObjects
    groupObjectsByProperties = imp12.groupObjectsByProperties
    performSearch = imp13.performSearch
    performSearch2 = imp12.performSearch
