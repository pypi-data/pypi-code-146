"""Streaming websocket sample printing EURUSD and GBPAUD prices to the terminal."""

import asyncio
from pprint import pprint

from saxo_apy import SaxoOpenAPIClient
from saxo_apy.utils import decode_streaming_message

client = SaxoOpenAPIClient()
client.login()  # ensure app_config.json is available in this directory


async def create_subscription() -> None:
    """Create subscription for EURUSD (uic 21) and GBPAUD (uic 22) prices."""
    sub = client.post(
        "/trade/v1/infoprices/subscriptions",
        data={
            "Arguments": {
                "Uics": "21,22",
                "AssetType": "FxSpot",
            },
            # this value is set when the streaming connection is initialized
            "ContextId": client.streaming_context_id,
            "ReferenceId": "my-fx-stream",
        },
    )
    pprint(sub)


async def message_handler() -> None:
    """Handle each received message by printing it to the terminal."""
    async with client.streaming_connection as stream:
        async for message in stream:
            decoded = decode_streaming_message(message)
            pprint(decoded.data)


async def main() -> None:
    """Execute main application logic."""
    client.setup_streaming_connection()

    # ensure refresh() is called so the websocket connection is re-authorized automatically
    # this keeps the streaming connection alive - else it is closed when token expires
    asyncio.ensure_future(client.async_refresh())
    await create_subscription()

    # this call will run forever, receiving messages until interrupted by user
    await message_handler()


# run the app
asyncio.run(main())
