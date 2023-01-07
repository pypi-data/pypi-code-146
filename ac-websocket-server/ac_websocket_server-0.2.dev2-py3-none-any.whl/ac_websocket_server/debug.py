'''Asyncio Debug Utilities.'''

import asyncio

DELAY = 10


async def monitor_tasks():
    '''
    Monitor tasks and print out every DELAY seconds.

    Call with:
    loop.create_task(monitor_tasks())
    '''
    # pylint: disable=expression-not-assigned

    while True:
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        tasks = [
            t for t in asyncio.all_tasks()
            if t is not asyncio.current_task()
        ]
        [t.print_stack(limit=5) for t in tasks]
        await asyncio.sleep(DELAY)
