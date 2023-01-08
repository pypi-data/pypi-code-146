from browser import window, websocket


async_url = 'ws://' + window.DJANGO_LIVESYNC.HOST + ':' + str(window.DJANGO_LIVESYNC.PORT)


def on_message(evt):
    print(evt.data)
    print(dir(evt))


ws = websocket.WebSocket(async_url)
ws.bind('message', on_message)
