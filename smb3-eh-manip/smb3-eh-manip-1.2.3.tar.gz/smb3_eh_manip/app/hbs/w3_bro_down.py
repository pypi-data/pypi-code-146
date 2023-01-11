"""
This is for manipulating world 3 hammer bro to go down after levels 1 and 2,
ensuring no runaway.

We intend on playing the first sections of 3-1 and 3-2 normally, but coming
out of the exit pipes, we calculate optimal windows in which we can end
the level to move the HB bro down.
"""
from smb3_eh_manip.app.hbs import hb
from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.models import Direction, World

# This includes stopping under the card and waiting for safety. If there are
# lots of frames, maybe its best to maintain pspeed? the y velocity is at least
# 4px different with pspeed vs without, so gotta pick either full speed or no
# speed IMO. This is safe.
THREE_ONE_BEFORE_JUMP_MIN_DURATION = 215
THREE_ONE_AFTER_JUMP_DURATION = 388
THREE_TWO_BEFORE_JUMP_MIN_DURATION = 234
THREE_TWO_AFTER_JUMP_DURATION = 478  # 1up fanfare


class W3BroDown:
    def __init__(self):
        self.world = World.load(number=3)
        self.hb = self.world.hbs[1]

    def calculate_3_1_window(self, seed_lsfr: LSFR):
        self.hb.y = 3  # let's assume we've reset in this scenario
        return hb.calculate_window(
            seed_lsfr,
            THREE_ONE_BEFORE_JUMP_MIN_DURATION,
            THREE_ONE_AFTER_JUMP_DURATION,
            Direction.DOWN,
            self.world,
            self.hb,
        )

    def calculate_3_2_window(self, seed_lsfr: LSFR):
        self.hb.y = 2  # let's assume above manip was successful in this scenario
        return hb.calculate_window(
            seed_lsfr,
            THREE_TWO_BEFORE_JUMP_MIN_DURATION,
            THREE_TWO_AFTER_JUMP_DURATION,
            Direction.DOWN,
            self.world,
            self.hb,
        )
