import asyncio

from plugp100 import TapoApiClient, TapoApiClientConfig, LightEffect


async def main():
    # create generic tapo api
    config = TapoApiClientConfig("<ip>", "<email>", "<passwd>")
    sw = TapoApiClient.from_config(config)
    await sw.login()
    await sw.on()
    await sw.set_brightness(100)
    state = await sw.get_state()
    print(state.firmware_version)
    print(state.is_hardware_v2)

    # light effect example
    await sw.set_light_effect(LightEffect.rainbow())
    state = await sw.get_state()
    print(state.get_unmapped_state())
    print(state.get_energy_unmapped_state())
    print(state.get_semantic_firmware_version())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.run_until_complete(asyncio.sleep(0.1))
    loop.close()
