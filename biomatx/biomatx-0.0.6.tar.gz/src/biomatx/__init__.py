"""
    pybiomatx

    Python API for managing the Biomatx home automation system
    :author: Damien Merenne <dam@cosinux.org>
    :license: MIT
"""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from struct import pack
from typing import Awaitable, Callable, List

__all__: List[str] = [
    "Bus",
    "Module",
    "Relay",
    "Switch",
]  # noqa: WPS410 (the only __variable__ we use)

_LOGGER = logging.getLogger(__name__)

SCENARIO_MODULE_ADDRESS = 7


@dataclass(frozen=True)
class Packet:
    """A Biomatx bus packet.

    Biomatx bus uses 2 bytes packet where
    [0-4] = 01010
    [5-7] = module address
    [8]: 0 pushed / 1 released
    [9-11] = module address
    [12-15] = switch address
    """

    module: int
    switch: int
    released: bool

    @classmethod
    def from_bytes(cls, data: bytes) -> Packet:
        p1, p2 = data
        module = (p2 & 0b01110000) >> 4
        switch = 0b00001111 & p2
        released = p2 >> 7
        return Packet(module, switch, bool(released))

    @property
    def pressed(self):
        return not self.released

    def __bytes__(self) -> bytes:
        p1 = 0b01010000 | self.module
        p2 = int(self.released) << 7 | self.module << 4 | self.switch
        return pack(
            "cc", p1.to_bytes(1, byteorder="little"), p2.to_bytes(1, byteorder="little")
        )


class Switch:
    """Biomatx switches.

    Switches are buttons that can be pressed or released."""

    def __init__(self, module: Module, address: int):
        self.address = address
        self.module = module
        self.released = True

    @property
    def bus(self):
        return self.module.bus

    @property
    def pressed(self):
        return not self.released

    def _packet(self):
        return self.module._packet(self.address, self.released)

    def _process(self, packet: Packet):
        assert packet.module == self.module.address
        assert packet.switch == self.address
        self.released = packet.released
        _LOGGER.debug("switch %s %s", self, "released" if self.released else "pressed")
        return True

    async def press(self):
        _LOGGER.debug("pressing switch %s", self)
        self.released = False
        await self.bus.send_packet(self._packet())

    async def release(self):
        _LOGGER.debug("releasing switch %s", self)
        self.released = True
        await self.bus.send_packet(self._packet())

    async def activate(self):
        await self.press()
        await self.release()

    def __repr__(self):
        return "<{}.{} module={} address={} pressed={}>".format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.module.address,
            self.address,
            self.pressed,
        )

    def __str__(self):
        return f"{self.module.address}/{self.address}"


class Relay:
    """Biomatx relay.

    Relays are controlled by a switch, they can be on or off."""

    def __init__(self, switch: Switch):
        self.switch = switch
        self.address = switch.address
        self.module = switch.module
        self.on = False

    @property
    def off(self):
        return not self.on

    def _process(self, packet: Packet):
        assert packet.module == self.module.address
        assert packet.switch == self.address

        # Update state on release
        if packet.released:
            self.on = not self.on
            _LOGGER.debug("relay %s turned %s", self, "on" if self.on else "off")
            return True
        return False

    async def toggle(self):
        _LOGGER.debug(
            "toggling relay %s from %s to %s",
            self,
            "on" if self.on else "off",
            "off" if self.on else "on",
        )
        await self.switch.activate()
        self.on = not self.on

    def force_toggle(self):
        """Toggle the state is memory without changing physical state."""
        self.on = not self.on

    def __repr__(self):
        return "<{}.{} module={} address={} on={}>".format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.module.address,
            self.address,
            self.on,
        )

    def __str__(self):
        return str(self.switch)


class Module:
    """A Biomatx module

    Modules contains 10 switches."""

    def __init__(self, bus: Bus, address: int):
        self.address = address
        self.bus = bus
        self.switches = [Switch(self, i) for i in range(0, 10)]
        if self.address != SCENARIO_MODULE_ADDRESS:
            self.relays = [Relay(i) for i in self.switches]

    def _packet(self, switch: int, released: bool):
        return Packet(self.address, switch, released)

    def __repr__(self):
        return "<{}.{} address={}>".format(
            self.__class__.__module__,
            self.__class__.__name,
            self.address,
        )


class Bus:
    """Biomatx Bus.

    The bus is a group of maximum 7 modules connected together. It uses an UTP cable
    with RJ45 connectors to convey a RS485 serial signal. Each time a switch is
    pressed/released, a packet is emitted on the bus. Sending a packet on the bus will
    trigger the matching relay.

    """

    def __init__(self, module_count: int, sleep: float = 0.5):
        self.running = False
        self._modules = {}
        self._stopped = None

        for i in range(0, 8):
            if i < module_count or i == SCENARIO_MODULE_ADDRESS:
                _LOGGER.debug(f"initializing module {i}")
                self._modules[i] = Module(self, i)

    @property
    def modules(self):
        return [
            module
            for module in self._modules.values()
            if module.address != SCENARIO_MODULE_ADDRESS
        ]

    @property
    def scenarios(self):
        return self._modules[SCENARIO_MODULE_ADDRESS]

    def switch(self, module: int, address: int):
        return self._modules[module].switches[address]

    def relay(self, module: int, address: int):
        return self._modules[module].relays[address]

    @property
    def relays(self):
        """Return all available relays."""
        all_relays = [module.relays for module in self.modules]
        return [relay for relays in all_relays for relay in relays]

    @property
    def switches(self):
        """Return all available switches."""
        all_switches = [module.switches for module in self._modules.values()]
        return [switch for switches in all_switches for switch in switches]

    async def connect(
        self,
        port: str,
        callback: Callable[[Switch | Relay], Awaitable[None]],
        loop: asyncio.Loop = None,
    ):
        """Open the serial device to which the physical bus is connected."""
        import serial
        import serial_asyncio

        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        self._callback = callback

        _LOGGER.debug("connecting to %s", port)
        self._reader, self._writer = await serial_asyncio.open_serial_connection(
            loop=loop,
            url=port,
            baudrate=19200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            xonxoff=False,
            rtscts=False,
        )
        _LOGGER.info("connected to %s", port)

    async def loop(self):
        """Process packets in a loop, keeping the device models state up to date."""
        self._stopped = self._loop.create_future()
        self.running = True
        _LOGGER.info("bus monitoring started")
        while self.running:
            _LOGGER.debug("waiting for next packet")
            try:
                await self.process_packet()
            except Exception as e:
                _LOGGER.exception("error while processing packet")
        _LOGGER.info("bus monitoring stopped")
        self._stopped.set_result(None)

    async def send_packet(self, packet: Packet):
        self._writer.write(bytes(packet))
        await self._writer.drain()
        # Leave time for the system to process
        await asyncio.sleep(0.2)

    async def read_packet(self) -> Packet:
        while True:
            data = await self._reader.readexactly(1)
            if (data[0] & 0b11111000) == 0b01010000:
                break
            _LOGGER.warning(f"dropping invalid start byte {data}")
        data +=  await self._reader.readexactly(1)
        _LOGGER.debug(f"received packet {data}")
        return Packet.from_bytes(data)

    def _trigger_callback(self, device: [Switch | Relay]):
        return asyncio.create_task(self._callback(device))

    async def process_packet(self):
        try:
            packet = await self.read_packet()
        except asyncio.IncompleteReadError:
            return []

        _LOGGER.debug(f"received {packet}")

        if not packet.module in self._modules:
            _LOGGER.error(f"unregistered module for {packet}")
            return []

        if packet.switch >= 10:
            _LOGGER.error(f"invalid relay for {packet}")
            return []

        tasks = []
        if packet.module != SCENARIO_MODULE_ADDRESS:
            relay = self.relay(packet.module, packet.switch)
            if relay._process(packet):
                tasks.append(self._trigger_callback(relay))
        switch = self.switch(packet.module, packet.switch)
        if switch._process(packet):
            tasks.append(self._trigger_callback(switch))
        return asyncio.gather(*tasks)

    async def stop(self):
        if not self.running:
            _LOGGER.warning("trying to stop non running bus")
            return

        _LOGGER.info("stopping bus monitoring")
        self.running = False
        self._writer.close()
        await self._stopped
        self._stopped = None
        self._loop = None
