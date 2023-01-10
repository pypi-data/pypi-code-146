import asyncio

import aiohttp

from .. import fhem, generic


class volvo(generic.FhemModule):

    VEHICLELIST = "/vehicles"
    VEHICLE_DETAILS = "/vehicles/"  # + VIN
    ACCEPT_HEADER = {
        VEHICLELIST: "application/vnd.volvocars.api.connected-vehicle.vehiclelist.v1+json",
        VEHICLE_DETAILS: "application/vnd.volvocars.api.connected-vehicle.vehicle.v1+json",
    }

    def __init__(self, logger):
        super().__init__(logger)

        self.attr_config = {
            "car": {
                "default": "",
                "help": "Select the car you would like to control.",
            },
            "update_interval": {
                "default": 30,
                "format": "int",
                "help": "Readings update intervall in seconds (default 30s).",
            },
            "update_readings": {
                "default": "always",
                "options": "always,onchange",
                "help": "Update readings only on value change or always (default onchange).",
            },
        }
        self.set_attr_config(self.attr_config)

        self.base_url = "https://api.volvocars.com/connected-vehicle/v1"

    # FHEM FUNCTION
    async def Define(self, hash, args, argsh):
        await super().Define(hash, args, argsh)
        if len(args) != 5:
            return "Usage: define my_volvo fhempy volvo api_key access_token"
        self.api_key = args[3]
        self.access_token = args[4]
        self.create_async_task(self.get_cars())
        await fhem.readingsSingleUpdate(self.hash, "state", "connecting", 1)

    async def get_cars(self):
        cars = await self.volvo_get(
            volvo.VEHICLELIST, volvo.ACCEPT_HEADER[volvo.VEHICLELIST]
        )
        if len(cars) == 0:
            self.logger.error("No cars found")
            return

        self.vin = cars[0]["vin"]
        await self.get_car_details()

    async def get_car_details(self):
        details = await self.volvo_get(
            volvo.VEHICLE_DETAILS + self.vin, volvo.ACCEPT_HEADER[volvo.VEHICLE_DETAILS]
        )

    async def volvo_get(self, path, accept_header):
        url = self.base_url + path
        headers = {
            "accept": accept_header,
            "vcc-api-key": self.api_key,
            "authorization": f"Bearer {self.access_token}",
        }
        try:
            response = {}
            async with aiohttp.ClientSession(
                trust_env=True, headers=headers
            ) as session:
                async with session.get(url) as resp:
                    response = await resp.json()

            if response["status"] == 200:
                return response["data"]
            else:
                self.logger.error(
                    f"Failed to get data from {path}: {response['error']}"
                )
        except Exception:
            self.logger.exception(f"Failed to get data from {path}")
            return {}
