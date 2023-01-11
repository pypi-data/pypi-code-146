from semantha_sdk.rest.RestClient import RestClient


class Instances:
    def __init__(self, session: RestClient, api_endpoint: str):
        self.__session = session
        self.__api_endpoint = api_endpoint

    def get_instances(self):
        return self.__session.get(self.__api_endpoint).execute()

    def post_domain_classes(self, body: dict):
        return self.__session.post(self.__api_endpoint, body).execute()

