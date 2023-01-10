import requests

# Sets up the API-Connector
class Connect:
    def __init__(self, ip_address="localhost", port=5001):

        # Check if port has the right format
        if str(port).isnumeric() == False:
            raise TypeError("The given port is not numeric")
        elif int(port) <= 0 or int(port) >= 65536:
            raise ValueError("Port number has to be between 1 and 65535")
        
        # Saves API Endpoint if port checks are passed
        self.endpoint = str(ip_address) + ":" + str(port)

        # Checks if the API is responding
        response = requests.post('http://{endpoint}/api/v0/bitswap/stat'.format(endpoint=self.endpoint))
        if response.status_code != 200:
            raise Exception("The given endpoint isn't working as intended")