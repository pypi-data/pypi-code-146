class DeviceMetadata:

    def __init__(self, device_metadata: dict):
        self.device_key: str = device_metadata.get('DeviceKey')
        self.device_group_key: str = device_metadata.get('DeviceGroupKey')