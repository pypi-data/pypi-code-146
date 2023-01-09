from peeringdb.models.facility import CreateFacilityModel, FacilityModel
from peeringdb.peeringdb import PeeringdbConnection


class Facility(object):
    def __init__(self, connection: PeeringdbConnection) -> None:
        self.connection = connection

    def create(self, **kwargs):
        """create a facility"""
        pass

    def read(self, id: int):
        """get a facility by id"""
        url = f"/fac/{id}"
        fac = FacilityModel.parse_obj(self.connection.get(url=url)[0])
        return fac

    def update(self, id: int, **kwargs):
        """update a facility"""

        pass

    def delete(self, id: int):
        """delete a facility"""
        pass

    def list(self):
        """get a list of matches for query"""
        pass
