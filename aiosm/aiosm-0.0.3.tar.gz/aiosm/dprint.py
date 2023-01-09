
import asyncio
import datetime


def dprint(message_type: str, *args) -> None:
	if message_type in [
		"Sending",
		"Received",
	]:
		print(str(datetime.datetime.now()) + ": (" + asyncio.current_task().get_name() + ") " + message_type + "")
	else:
		print(str(datetime.datetime.now()) + ": (" + asyncio.current_task().get_name() + ") " + message_type + ": \n\t", *args)
