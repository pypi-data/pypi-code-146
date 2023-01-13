from FCM.MCCore import MCCore

""" Master Class to work with Any Collection """
class CommonCollection(MCCore):

    def __init__(self, collectionName, **kwargs):
        super().__init__(**kwargs)
        self.connect(collectionName)

if __name__ == '__main__':
    c = CommonCollection("virtual_worlds")
    print(c.base_query({"symbol": "ADS"}))