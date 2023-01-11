import unittest
import tempfile

from smb3_eh_manip.app import models


class TestModels(unittest.TestCase):
    def test_serialize(self):
        world = models.World(
            number=2,
            positions=[
                models.Position(x=5, y=2),
                models.Position(x=5, y=3, level=models.Level(name="2-3")),
                models.Position(x=5, y=4),
                models.Position(
                    x=6,
                    y=3,
                ),
                models.Position(x=7, y=3, level=models.Level(name="2-quicksand")),
                models.Position(x=7, y=4),
                models.Position(x=8, y=4, level=models.Level(name="2-4")),
                models.Position(x=9, y=4),
                models.Position(x=9, y=3),
                models.Position(
                    x=9,
                    y=2,
                ),
            ],
            hbs=[
                models.HammerBro(index=2, item="box", x=6, y=3),
                models.HammerBro(index=3, item="hammer", x=9, y=2),
            ],
        )
        world.dump(path_prefix=tempfile.tempdir)
        world_load = models.World.load(
            number=world.number, path_prefix=tempfile.tempdir
        )
        self.assertEqual(world, world_load)

    def test_window_create_centered_window(self):
        self.assertEqual(10, models.Window.create_centered_window(10, 1).action_frame)
        self.assertEqual(10, models.Window.create_centered_window(11, 2).action_frame)
        self.assertEqual(11, models.Window.create_centered_window(12, 3).action_frame)
        self.assertEqual(11, models.Window.create_centered_window(13, 4).action_frame)
        self.assertEqual(12, models.Window.create_centered_window(14, 5).action_frame)
