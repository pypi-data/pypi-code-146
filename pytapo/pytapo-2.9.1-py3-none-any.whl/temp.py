
    def scan(self):
        requests = self.performRequest(
            {
                "method": "multipleRequest",
                "params": {
                    "requests": [
                        {
                            "method": "getDeviceInfo",
                            "params": {"device_info": {"name": ["basic_info"]}},
                        },  # correct request, OK
                        {
                            "method": "getDeviceInfo",
                            "params": {"device_infoBAD": {"name": ["basic_info"]}},
                        },  # incorrect param key: -40106
                        {
                            "method": "getDeviceInfo",
                            "params": {"device_info": {"name": ["basic_infoBAD"]}},
                        },  # incorrect value in array: -40106
                        {
                            "method": "getDeviceInfo",
                            "params": {"device_info": {"name": []}},
                        },  # empty array: OK
                        {
                            "method": "getDeviceInfo",
                            "params": {"device_info": {"name": "null"}},
                        },  # incorrect value type: -40106
                        {
                            "method": "getDeviceInfoBAD",
                            "params": {"device_info": {"name": []}},
                        },  # incorrect function name: -40210
                        {
                            "method": "getDeviceInfo",
                            "paramssssss": {"device_info": {"name": []}},
                        },  # incorrect params key name, OK
                        {"method": "getDeviceInfo"},  # only method, OK
                        {"method": "getDeviceInfoBAD"},  # method does not exist: -40210
                        {
                            "method": "getConnectStatus"
                        },  # -40210 this means the function does not exist
                        {
                            "method": "scanApList"
                        },  # -40210 this means the function does not exist
                        {
                            "method": "connectAp"
                        },  # -40210 this means the function does not exist
                        {
                            "method": "getConnectionType",
                            "params": {"network": {"get_connection_type": []}},
                        },  # todo: create wifi function
                    ]
                },
            }
        )
        for request in requests["result"]["responses"]:
            print(request)

        return True
