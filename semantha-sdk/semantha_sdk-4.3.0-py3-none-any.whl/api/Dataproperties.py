from semantha_sdk.api import SemanthaAPIEndpoint


class DataProperties(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/dataproperties"

    def get_data_properties(self, domain: str):
        return self._session.get(f"/api/domains/{domain.lower()}/dataproperties").execute()

    def post_data_properties(self, domain: str, body: dict):
        return self._session.post(f"/api/domains/{domain.lower()}/dataproperties", body).execute()
