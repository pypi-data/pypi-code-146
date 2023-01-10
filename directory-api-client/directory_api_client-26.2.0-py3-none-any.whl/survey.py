from directory_api_client.base import AbstractAPIClient

url_get_survey_details = 'survey/{pk}'


class SurveyAPIClient(AbstractAPIClient):
    def get_survey_details(self, id):
        return self.get(url=url_get_survey_details.format(pk=id), use_fallback_cache=True)
