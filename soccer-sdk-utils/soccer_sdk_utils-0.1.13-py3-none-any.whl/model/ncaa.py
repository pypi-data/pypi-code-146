class School:
    def __init__(self, **kwargs):
        self.name = kwargs.get("nameOfficial")
        self.conference = kwargs.get("conferenceName")
        self.private = kwargs.get("privateFlag") == "Y"
        self.hbcu = kwargs.get("historicallyBlackFlag") == "Y"
        self.state = kwargs.get("memberOrgAddress")["state"]

    def __repr__(self):
        buffer = "<School("
        buffer += f"name='{self.name}', "
        buffer += f"conference='{self.conference}', "
        buffer += f"private={self.private}, "
        buffer += f"hbcu={self.hbcu}, "
        buffer += f"state='{self.state}')>"

        return buffer

    def __str__(self):
        return self.__repr__()
