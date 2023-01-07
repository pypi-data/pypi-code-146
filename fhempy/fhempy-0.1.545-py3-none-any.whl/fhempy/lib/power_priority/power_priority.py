import asyncio

from .. import fhem, generic


class power_priority(generic.FhemModule):
    def __init__(self, logger):
        super().__init__(logger)

        attr_config = {
            "devices": {
                "default": "",
                "format": "json",
                "help": (
                    "Set the devices you would like to turn on or off.<br>"
                    "E.g. prio 1 wallbox, prio 2 aircondition<br>"
                    '{ "wallbox": { "avg_power": 2000 }, '
                    '"aircondition": { "avg_power": 1500 }}'
                ),
            }
        }
        self.set_attr_config(attr_config)

        set_config = {}
        self.set_set_config(set_config)

    # FHEM FUNCTION
    async def Define(self, hash, args, argsh):
        await super().Define(hash, args, argsh)
        if len(args) != 5:
            return (
                "Usage: define my_solarpriority fhempy solarpriority "
                "SOLARPLANTDEVICE AVAILABLE_ENERGY_READING"
            )

        self._solardevice = args[3]
        self._solarreading = args[4]

    async def available_energy(self):
        return await fhem.ReadingsVal(self._solardevice, self._solarreading, 0)

    async def prioritize_devices(self):
        energy = await self.available_energy()
        for devname in self._attr_devices:
            devconfig = self._attr_devices[devname]
            devpower = devconfig["avg_power"]

    # Set functions in format: set_NAMEOFSETFUNCTION(self, hash, params)
    async def set_on(self, hash, params):
        # params contains the keyword which was defined in set_list_conf for "on"
        # if not provided by the user it will be "" as defined in set_list_conf (default = "" and optional = True)
        seconds = params["seconds"]
        if seconds != 0:
            await fhem.readingsSingleUpdate(hash, "state", "on " + str(seconds), 1)
        else:
            await fhem.readingsSingleUpdate(hash, "state", "on", 1)

    async def set_off(self, hash, params):
        # no params argument here, as set_off doesn't have arguments defined in set_list_conf
        await fhem.readingsSingleUpdate(hash, "state", "off", 1)
        self.create_async_task(self.long_running_task())
        return ""

    async def long_running_task(self):
        await asyncio.sleep(30)
        await fhem.readingsSingleUpdate(self.hash, "state", "long running off", 1)

    async def set_mode(self, hash, params):
        # user can specify mode as mode=eco or just eco as argument
        # params['mode'] contains the mode provided by user
        mode = params["mode"]
        await fhem.readingsSingleUpdate(hash, "mode", mode, 1)

    async def set_desiredTemp(self, hash, params):
        temp = params["temperature"]
        await fhem.readingsSingleUpdate(hash, "mode", temp, 1)

    async def set_holidayMode(self, hash, params):
        start = params["start"]
        end = params["end"]
        temp = params["temperature"]
        await fhem.readingsSingleUpdate(hash, "start", start, 1)
        await fhem.readingsSingleUpdate(hash, "end", end, 1)
        await fhem.readingsSingleUpdate(hash, "temp", temp, 1)
