from postr.model.event import TextNote
from postr.model.filter import Filter
from postr.model.messages import parse_message, SubscriptionResponse, RequestMessage
from postr.user import User

user = User()
note = user.sign(TextNote(content="Hello World"))
assert note.verify()


msg = RequestMessage(subscription_id="ABC", filters=[Filter()])
payload = msg.payload()

from websocket import create_connection

# ws = create_connection("wss://nostr.openchain.fr")
ws = create_connection("wss://relay.damus.io")
# ws = create_connection("wss://nostr-verified.wellorder.net")
# payload = note.get_message().json()
# payload = json.dumps(["REQ", "ABCDEFG", Filter().dict(exclude_unset=True)])
print(payload)
ws.send(payload)
print("Sent")
print("Receiving...")

for i in range(100):
    match result := parse_message(ws.recv()):
        case SubscriptionResponse(event=TextNote()):
            event = result.event
            if event.verify():
                print("TextNote", event.content)
        case SubscriptionResponse():
            event = result.event
            if event.verify():
                print("unknown kind", event.kind)
        case _:
            print("Received something else")

# print(f"Received '{result}'")
ws.close()

private_key = cc.PrivateKey()
public_key = private_key.public_key

message = b"Hello world"
signature = private_key.sign(message)

assert cc.verify_signature(signature, message, public_key.format(compressed=True))
assert cc.verify_signature(signature, message, public_key.format(compressed=False))
