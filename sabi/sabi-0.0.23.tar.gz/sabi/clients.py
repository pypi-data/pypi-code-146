from sabi.api_client import ApiClient


class Clients(ApiClient):
    headers = None

    def __init__(self, api_key, host=None):
        version = "v1"
        base = f"{version}/clients"
        super().__init__(api_key, base, host)

    def company_integration(self, company_integration_hash_id):
        response = self.get("company_integrations", company_integration_hash_id)
        return response

    def integrations(self, type):
        response = self.get("integrations", type)
        return response

    def individuals(self):
        response = self.get("individuals")
        return response

    def save_individuals_status(self, individuals):
        """
        Example for valid payload:
        {
            "accounts": [
                {"accountId": "5be24ba3f91c106033269289", "status": "closed"}
            ]
        }

        """
        response = self.put("update_individuals_status", json=individuals)

    def mark_integration_unhealthy(self, company_integration_id):
        response = self.put("mark_integration_unhealthy", company_integration_id)
        return response
