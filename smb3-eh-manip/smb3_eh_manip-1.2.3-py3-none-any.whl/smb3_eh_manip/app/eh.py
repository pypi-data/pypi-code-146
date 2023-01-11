"""
Where the world dataclasses are agnostic of the underlying world and data,
this class has specific insight into world 2. Whatever we need to model that
is world 2 specific (direction hints, constraints, frame offsets) should live
here.
"""
from smb3_eh_manip.app.models import World


# we want to simulate the bros. after simulating we can figure out optimization.
# step1: identify which direction the bro should be facing coming out of 2-1
# step2: move the hammer bro in the correct direction
# step3: generalize to a loop so we can run many experiments
# step4: identify minimum level frame durations to optimize experiments
# step5: depth first search solutions and generate frame windows


BRO_MOVEMENT_FRAMES = 32  # it takes 32 frames for a HB to make 1 movement
LEVEL_FACE_TO_MOVE_FRAMES = 39
FORT_FACE_TO_MOVE_FRAMES = 102


class EH:
    def __init__(self):
        self.world = World.load(number=2)

    def tick(self):
        pass
