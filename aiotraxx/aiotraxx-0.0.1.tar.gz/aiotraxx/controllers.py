from uplink import Consumer, Query, get, headers



@headers({"Accept": "text/csv"})
class Sensors(Consumer):
    @get("/assets/{asset_id}/asset_sensor_profiles/{sensor_id}/measurements/query.csv")
    def sensor_data(
        self,
        asset_id: int,
        sensor_id: str,
        begin: Query,
        end: Query,
        tz: Query
    ):
        """Get sensor data for an asset as a CSV."""