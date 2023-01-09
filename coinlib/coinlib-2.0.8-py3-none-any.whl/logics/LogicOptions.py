
class LogicOptions:

    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])

    makerFee: float
    takerFee: float