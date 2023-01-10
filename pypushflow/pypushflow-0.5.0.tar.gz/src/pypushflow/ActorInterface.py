class ActorInterface:
    """The interface that makes a class a pypushflow actor"""

    def trigger(self, inData):
        raise NotImplementedError

    @property
    def pool_resources(self):
        return 0
