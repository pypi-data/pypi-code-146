su_apis = {
    "analytics": {
        "tileData": "/api/v2/searchOverview/getTileData",
        "searchSummaryChart": "/api/v2/searchOverview/getSearchSummaryChart",
        "searchQueryAll": "/api/v2/searchQuery/all",
        "searchQueryWithResults": "/api/v2/searchQuery/withResults",
        "searchQueryWithNoClicks": "/api/v2/searchQuery/withNoClicks",
        "searchQueryWithoutResult": "/api/v2/searchQuery/withoutResults",
        "searchQueryHistogram": "/api/v2/searchQuery/histogram",
        "missedQueryHistogram": "/api/v2/searchQuery/missedQueryHistogram",
        "searchSessionByCaseUidAuth": "/api/v2/searchSession/byCaseUidAuth",
        "allSearchConversion": "/api/v2/searchConversion/all",
        "searchConversionNotOnFirstPage": "/api/v2/searchConversion/notOnFirstPage",
        "searchConversionWithFilters": "/api/v2/searchConversion/withFilters",
        "searchConversionBySessionId": "/api/v2/searchConversion/bySessionsId/<searchSessionId>",
        "discussionsReadyToBecomeArticles": "/api/v2/searchConversion/DiscussionsReadyToBecomeArticles",
        "searchSessionBySearchSessionId": "/api/v2/searchSession/bySearchSessionId/<searchSessionId>",
        "searchSessionAllsearchQuery": "/api/v2/searchSession/all/searchQuery",
        "kcsSupport": "/api/v2/searchQuery/kcsSupport",
        "searchSessionByCaseUid": "/api/v2/searchSession/byCaseUid",
        "articlesCreatedCases": "/api/v2/conversion/articlesCreatedCases",
        "articlesDeflectedCase": "/api/v2/conversion/articlesDeflectedCase",
        "attachedArticles": "/api/v2/conversion/attachedArticles",
        "attachedOnCase": "/api/v2/conversion/attachedOnCase"
    },
    "search": {
        "searchResults": "/api/v2_search/searchResults"
    },
    "content": {
        "contentSources": "/api/v2_cs/contentSource/all",
        "contentSourceByID": "/api/v2_cs/contentSource",
        "objectAndFields": "/api/v2_cs/contentSource/<contentSourceId>/objectAndFields",
        "objectData": "/api/v2_cs/apiData/contentSource/<contentSourceId>/object/<objectId>/get",
        "objectDataWithId": "/api/v2_cs/apiData/contentSource/<contentSourceId>/object/<objectId>/document/<documentId>/get",
        "updateDoucmentById": "/api/v2_cs/apiData/contentSource/<contentSourceId>/object/<objectId>/document/<documentId>/update",
        "bulkUpload": "/api/v2_cs/apiData/contentSource/<contentSourceId>/object/<objectId>/bulkUpload"
    },
    "oauth": {
        "accessToken": "/oauth/token"
    }
}

class Apis:
    def get_apis(type):
        if (type):
            return su_apis[type]
        else:
            return 'Unknown api type.'
