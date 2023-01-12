import unittest
from univer_db.models import AbiturientRegAts

from . import Session


class AbiturientRegAtsTestCase(unittest.TestCase):
    def test_get_obj(self):
        session = Session()
        ats = session.query(AbiturientRegAts).first()
        print(f"ats: {ats}")
    
    def test_get_parent(self):
        session = Session()
        ats = session.query(AbiturientRegAts).filter(
            AbiturientRegAts.parent_id != 1).first()
        print(f"ats: {ats}")
        print(f"ats.parent_id: {ats.parent_id}")
        print(f"ats.parent: {ats.parent}")
