import requests

class ConnectionManagementRPAOCI:
    def get_connection(connection_id):
        url = "https://downstream-dev.test-37.splat.us-ashburn-1.oci.oracleiaas.com/20230401/connections/{connection_id}/content".format(connection_id = connection_id)
        response = requests.get(url, verify=False)
        if int(response.status_code) // 100 == 2:
            content = response.json()["content"]
            return content
        else:
            return None
