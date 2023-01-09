from searchunify.utils.validation.analytics import AnalyticsValidator
from searchunify.utils.validation.content import ContentValidator
from searchunify.utils.validation.search import SearchValidator
from searchunify.core.search.search import Search
from searchunify.core.content.contents import Content
from searchunify.core.analytics.analytics import Analytics
from searchunify.core.auth.oauth2 import Oauth2
from searchunify.utils.constants.constants import Constants, AuthVariables
from searchunify.client.client import Client

CONSTANTS = Constants()
AUTH_VARS = AuthVariables()

class Searchunify:
    """
    Used to initialize SearchUnify client. 
    Provide SearchUnify instance url, username, password, client_id and client_secret.
    """
    def __init__(self, **props):
        try:
            Client.authentication_type_validation(props)
            if (CONSTANTS.OAUTH2_DEL == AUTH_VARS.AUTH_TYPE):
               Oauth2.generate_access_token(props)
        except Exception as error:
            raise Exception(error)

    def refresh_token(self):
        """
        Get accessToken from refresh token.
        """
        try:
            response = Oauth2.access_token_from_refresh_token()
            return response
        except Exception as error:
            raise Exception(error)

    def get_tiles_data(self, **props):
        """
        Used to get information about visitors, search users, clicks, results, cases, and other essential search behavior.
        """
        try:
            AnalyticsValidator.get_tiles_data(**props)
            response = Analytics.get_tiles_data(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def get_search_summary_chart(self, **props):
        """
        Return Searches with Results, and All Searches with Clicks (conversions) have changed over the period between startDate and endDate.
        """
        try:
            AnalyticsValidator.get_search_summary_chart(**props)
            response = Analytics.get_search_summary_chart(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def get_all_search_query(self, **props):
        """
        Returns the most popular search queries over the period from startDate to endDate.
        """
        try:
            AnalyticsValidator.analytics_data_validation(**props)
            response = Analytics.get_all_search_query(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def get_search_queries_with_result(self, **props):
        """
        Returns the most popular search queries for which results were found.
        """
        try:
            AnalyticsValidator.analytics_data_validation(**props)
            response = Analytics.get_search_queries_with_result(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def search_queries_with_no_clicks(self, **props):
        """
        Returns the most popular search queries for which results were found but users didn't click on any of them.
        """
        try:
            AnalyticsValidator.analytics_data_validation(**props)
            response = Analytics.search_queries_with_no_clicks(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def search_queries_without_result(self, **props):
        """
        Returns the most popular search queries for which no results were found.
        """
        try:
            AnalyticsValidator.analytics_data_validation(**props)
            response = Analytics.search_queries_without_result(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def search_query_histogram(self, **props):
        """
        Returns search and conversion data over the period between startDate and endDate.
        """
        try:
            AnalyticsValidator.analytics_data_validation(**props)
            response = Analytics.search_query_histogram(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def missed_query_histogram(self, **props):
        """
        Returns the total number of queries that didn't produce even one result. The data is for the period between startDate and endDate.
        """
        try:
            AnalyticsValidator.analytics_data_validation(**props)
            response = Analytics.missed_query_histogram(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def search_session_by_case_uid_auth(self, **props):
        """
        Return the activity on a case.
        """
        try:
            AnalyticsValidator.search_session_by_case_uid_auth(**props)
            response = Analytics.search_session_by_case_uid_auth(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def get_all_search_conversion(self, **props):
        """
        Return a list of the count most popular documents. The data is from between startDate and endDate on a search client whose ID is searchClientID.
        If the searchClientID is not specified, then the call fetches data from all the search clients.
        """
        try:
            AnalyticsValidator.analytics_data_validation(**props)
            response = Analytics.get_all_search_conversion(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def search_conversion_not_On_first_page(self, **props):
        """
        Return a list of the count documents that are not on the first page. These documents can be boosted to enhance search experience.
        The data is from between startDate and endDate on a search client whose ID is searchClientID. If the searchClientID is not specified, then the call fetches data from all the search clients.
        """
        try:
            AnalyticsValidator.analytics_data_validation(**props)
            response = Analytics.search_conversion_not_On_first_page(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def search_conversion_with_filters(self, **props):
        """
        Return a chart of the popularity of all your content sources.
        The data is presented in an alphabetical order and includes:
        objectName, objectData, filterName, filterData, facetName, and facetName.
        An objectName is a content type and a filter is a high-level facet.
        The data is from between startDate and endDate.
        """
        try:
            AnalyticsValidator.search_conversion_with_filters(**props)
            response = Analytics.search_conversion_with_filters(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def search_conversion_by_sessionid(self, **props):
        """
        Return a list of the count most popular searches in a session.
        The data is from between startDate and endDate on a search client whose ID is searchClientID.
        If the searchClientID is not specified, then the call fetches data from all the search clients.
        """
        try:
            AnalyticsValidator.search_conversion_by_sessionid(**props)
            response = Analytics.search_conversion_by_sessionid(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def get_search_session_by_search_sessionid(self, **props):
        """
        Return a list of the count queries in a search session and the documents accessed during that session.
        The data is from between startDate and endDate on a search client whose ID is searchClientID.
        If the searchClientID is not specified, then the call fetches data from all the search clients.
        """
        try:
            AnalyticsValidator.get_search_session_by_search_sessionid(**props)
            response = Analytics.get_search_session_by_search_sessionid(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def get_discussions_ready_to_become_article(self, **props):
        """
        Return count discussions that have been accessed the most and can be converted into articles.
        The data is from between startDate and endDate.
        """
        try:
            AnalyticsValidator.get_discussions_ready_to_become_article(**props)
            response = Analytics.discussions_ready_to_become_article(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def search_queries_in_sessions(self, **props):
        """
        Return a list of the count search sessions and the searches conducted in each session.
        The data is from between startDate and endDate on a search client whose ID is searchClientID.
        If the searchClientID is not specified, then the call fetches data from all the search clients.
        """
        try:
            AnalyticsValidator.analytics_data_validation(**props)
            response = Analytics.search_queries_in_sessions(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def get_kcs_support_search_query(self, **props):
        """
        Return the number of articles generated on your cases between startDate and endDate on a search client whose ID is searchClientID.
        If the searchClientID is not specified, then the call fetches data from all the search clients.
        """
        try:
            AnalyticsValidator.analytics_data_validation(**props)
            response = Analytics.get_kcs_support_search_query(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def get_search_session_by_case_uid(self, **props):
        """
        Return search, conversion, page views, case deflection, and case creation data for the argument caseUid.
        """
        try:
            AnalyticsValidator.search_session_by_case_uid_auth(**props)
            response = Analytics.get_search_session_by_case_uid(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def get_case_created_articles(self, **props):
        """
        Return the list of articles that were consulted before a user created a case.
        """
        try:
            AnalyticsValidator.case_created_validation(**props)
            response = Analytics.get_case_created_articles(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def get_case_deflected_articles(self, **props):
        """
        Returns the articles that were consulted by users who didn't create a case.
        """
        try:
            AnalyticsValidator.case_created_validation(**props)
            response = Analytics.get_case_deflected_articles(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def get_attached_articles(self, **props):
        """
        Return how many articles have been attached to cases.
        """
        try:
            AnalyticsValidator.get_attached_articles(**props)
            response = Analytics.get_attached_articles(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def get_attached_on_case(self, **props):
        """
        From the article URL, find out which cases it has been attached to.
        """
        try:
            AnalyticsValidator.get_attached_on_case(**props)
            response = Analytics.get_attached_on_case(**props)
            return response
        except Exception as error:
            raise Exception(error)

    # content source methods.
    def get_content_sources(self):
        """
        Used to list all added content sources in SearchUnify instance.
        """
        try:
            response = Content.get_content_sources()
            return response
        except Exception as error:
            raise Exception(error)

    def get_content_source_by_id(self, **props):
        """
        Used to get particular content source.
        You need pass contentSourceId as a parameter particular content source.
        """
        try:
            ContentValidator.content_source_id_validation(**props)
            response = Content.get_content_source_by_id(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def get_object_and_fields(self, **props):
        """
        Used to get content source objects and fileds.
        """
        try:
            ContentValidator.content_source_id_validation(**props)
            response = Content.get_object_and_fields(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def get_object_specific_data(self, **props):
        """
        If you have multiple objects type. You can get data from particular object by this method.
        """
        try:
            ContentValidator.get_object_specific_data(**props)
            response = Content.get_object_specific_data(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def get_object_specific_data_with_id(self, **props):
        """
        Used to get data from a specific object type and specific document id.
        """
        try:
            ContentValidator.get_object_specific_data_with_id(**props)
            response = Content.get_object_specific_data_with_id(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def update_doucment_by_id(self, **props):
        """
        Used to update particular document in SearchUnify index.
        """
        try:
            ContentValidator.update_doucment_by_id(**props)
            response = Content.update_doucment_by_id(**props)
            return response
        except Exception as error:
            raise Exception(error)

    def upload_data(self, **props):
        """
        Used to index multiple document at a time.
        """
        try:
            ContentValidator.upload_data(**props)
            response = Content.upload_data(**props)
            return response
        except Exception as error:
            raise Exception(error)

    # Search methods
    def get_search_results(self, **props):
        """
        Used to search content from a particular plateform.
        Pass uid, searchString and other optional parameters as per requirement.
        """
        try:
            SearchValidator.get_search_results(**props)
            response = Search.get_search_results(**props)
            return response
        except Exception as error:
            raise Exception(error)
