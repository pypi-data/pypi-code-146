from nwgraph import Message
import torch as tr

def test_message_1():
    message = Message(tr.zeros(5))
    assert tr.allclose(message.content, tr.zeros(5))

def test_message_2():
    x = tr.randn(5, 10)
    message = Message(x)
    assert tr.allclose(message.content, x)
