"""
This is a test class for manipulating HBs. It manips the world 1 HB to move
left after 1-1 depending on when the player enters the level.
"""
from smb3_eh_manip.app.hbs import hb
from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.models import World


ONE_ONE_DURATION_FRAMES = 1449  # stop and jump under the end card


class W1HBTest:
    def __init__(self):
        self.world = World.load(number=1)
        self.hb = self.world.hbs[0]

    def calculate_facing(self, seed_lsfr: LSFR):
        lsfr = seed_lsfr.clone()
        lsfr.next_n(ONE_ONE_DURATION_FRAMES + hb.LEVEL_TO_FACE_FRAMES)
        return hb.calculate_facing_direction(
            lsfr, self.world, self.hb, hb.LEVEL_FACE_TO_MOVE_FRAMES
        )
