"""
Test class. Manip for bro moving left after 1-1.
"""
from smb3_eh_manip.app.hbs import hb
from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.models import Direction, World


class W1BroLeft:
    def __init__(self):
        self.world = World.load(number=1)
        self.hb = self.world.hbs[0]

    def calculate_window(self, seed_lsfr: LSFR):
        return hb.calculate_window(
            seed_lsfr,
            965,
            385,
            Direction.LEFT,
            self.world,
            self.hb,
        )
