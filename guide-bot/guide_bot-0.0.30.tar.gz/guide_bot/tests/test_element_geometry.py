import unittest

import numpy as np
from scipy.spatial.transform import Rotation as R

from guide_bot.elements.Element_straight import Straight
from guide_bot.elements.Element_gap import Gap
from guide_bot.elements.Element_kink import Kink

from guide_bot.parameters.instrument_parameters import FixedInstrumentParameter
from guide_bot.parameters.instrument_parameters import RelativeFreeInstrumentParameter

from guide_bot.base_elements.base_element_geometry import BaseElementGeometry
from guide_bot.base_elements.base_element_geometry import PositionAndRotation
from guide_bot.base_elements.base_element_geometry import line_intersect_plane
from guide_bot.base_elements.base_element_geometry import inside_polygon


class Test_element_geometry(unittest.TestCase):
    def test_float_setup(self):
        """
        Ensure BaseElementGeometry transfers given float input to attributes
        """
        element_geometry = BaseElementGeometry(start_point=2.2, next_start_point=8.4,
                                               start_width=0.08, start_height=0.09,
                                               end_width=0.05, end_height=0.06)

        self.assertEqual(element_geometry.start_point, 2.2)
        self.assertEqual(element_geometry.next_start_point, 8.4)
        self.assertEqual(element_geometry.start_width, 0.08)
        self.assertEqual(element_geometry.start_height, 0.09)
        self.assertEqual(element_geometry.end_width, 0.05)
        self.assertEqual(element_geometry.end_height, 0.06)

    def test_float_int_setup(self):
        """
        Ensure attributes can be set with mix of floats and ints
        """
        element_geometry = BaseElementGeometry(start_point=2.2, next_start_point=9,
                                               start_width=0.08, start_height=0.09,
                                               end_width=0.05, end_height=0.06)

        self.assertEqual(element_geometry.start_point, 2.2)
        self.assertEqual(element_geometry.next_start_point, 9)
        self.assertEqual(element_geometry.start_width, 0.08)
        self.assertEqual(element_geometry.start_height, 0.09)
        self.assertEqual(element_geometry.end_width, 0.05)
        self.assertEqual(element_geometry.end_height, 0.06)

    def test_FixedInstrumentParameter_setup(self):
        """
        Ensure attributes can be set with FixedInstrumentParmaeter
        """
        width = FixedInstrumentParameter("test_width", 0.0823)

        element_geometry = BaseElementGeometry(start_point=2.2, next_start_point=9,
                                               start_width=width, start_height=0.09,
                                               end_width=0.05, end_height=0.06)

        self.assertEqual(element_geometry.start_point, 2.2)
        self.assertEqual(element_geometry.next_start_point, 9)
        self.assertEqual(element_geometry.start_width, 0.0823)
        self.assertEqual(element_geometry.start_height, 0.09)
        self.assertEqual(element_geometry.end_width, 0.05)
        self.assertEqual(element_geometry.end_height, 0.06)

        self.assertIs(element_geometry.instrument_parameters["start_width"], width)

    def test_RelativeFreeInstrumentParameter_setup(self):
        """
        Ensure attributes can be set with RelativeFreeInstrumentParameter
        """
        height = RelativeFreeInstrumentParameter("test_height", 0.05, 0.1)
        height.set_value(0.5)  # Will set height to halfway between 0.05 and 0.1, 0.075
        self.assertAlmostEqual(height.get_value(), 0.075)

        element_geometry = BaseElementGeometry(start_point=2.2, next_start_point=9,
                                               start_width=0.08, start_height=height,
                                               end_width=0.05, end_height=0.06)

        self.assertEqual(element_geometry.start_point, 2.2)
        self.assertEqual(element_geometry.next_start_point, 9)
        self.assertEqual(element_geometry.start_width, 0.08)
        self.assertAlmostEqual(element_geometry.start_height, 0.075)
        self.assertEqual(element_geometry.end_width, 0.05)
        self.assertEqual(element_geometry.end_height, 0.06)

        self.assertIs(element_geometry.instrument_parameters["start_height"], height)

        height.set_value(0.0)
        # Should not yet update
        self.assertAlmostEqual(element_geometry.start_height, 0.075)

        # Update and check new state is transferred
        element_geometry.load_new_state()
        self.assertAlmostEqual(element_geometry.start_height, 0.05)

    def test_corners(self):

        element_geometry = BaseElementGeometry(start_point=2.0, next_start_point=5.0,
                                               start_width=0.02, start_height=0.04,
                                               end_width=0.08, end_height=0.04)

        pr = PositionAndRotation(np.array([0, 0, 0]), R.from_euler("z", 0))

        # Corner points at start
        a, b, c, d = element_geometry.get_corners(pr, 0)

        self.assertEqual(a[0], -0.02*0.5)
        self.assertEqual(a[1], -0.04*0.5)
        self.assertEqual(a[2], 0)

        self.assertEqual(b[0], -0.02*0.5)
        self.assertEqual(b[1], 0.04*0.5)
        self.assertEqual(b[2], 0)

        self.assertEqual(c[0], 0.02*0.5)
        self.assertEqual(c[1], 0.04*0.5)
        self.assertEqual(c[2], 0)

        self.assertEqual(d[0], 0.02*0.5)
        self.assertEqual(d[1], -0.04*0.5)
        self.assertEqual(d[2], 0)

        # Corner points at middle (3 m long, will be at 1.5 m)
        a, b, c, d = element_geometry.get_corners(pr, 0.5)

        self.assertEqual(a[0], -(0.02 + 0.08) * 0.25)
        self.assertEqual(a[1], -(0.04 + 0.04) * 0.25)
        self.assertEqual(a[2], 1.5)

        self.assertEqual(b[0], -(0.02 + 0.08) * 0.25)
        self.assertEqual(b[1], (0.04 + 0.04) * 0.25)
        self.assertEqual(b[2], 1.5)

        self.assertEqual(c[0], (0.02 + 0.08) * 0.25)
        self.assertEqual(c[1], (0.04 + 0.04) * 0.25)
        self.assertEqual(c[2], 1.5)

        self.assertEqual(d[0], (0.02 + 0.08) * 0.25)
        self.assertEqual(d[1], -(0.04 + 0.04) * 0.25)
        self.assertEqual(d[2], 1.5)

    def test_line_intersect_trvial(self):
        """
        trivial intersection check along z
        """

        pr = PositionAndRotation(np.array([0, 0, 0]), R.from_euler("z", 0))

        p0 = np.array([0, 0, -1])
        p1 = np.array([0, 0, 1])

        intersect = line_intersect_plane(point0=p0, point1=p1, pr=pr)

        self.assertAlmostEqual(intersect[0], 0)
        self.assertAlmostEqual(intersect[1], 0)
        self.assertAlmostEqual(intersect[2], 0)

    def test_line_intersect_translated(self):
        """
        trivial intersection check along z, but translated in x and y
        """

        pr = PositionAndRotation(np.array([0, 0, 0]), R.from_euler("z", 0))

        x_off = 0.273
        y_off = 3.283

        p0 = np.array([x_off, y_off, -1])
        p1 = np.array([x_off, y_off, 1])

        intersect = line_intersect_plane(point0=p0, point1=p1, pr=pr)

        self.assertAlmostEqual(intersect[0], x_off)
        self.assertAlmostEqual(intersect[1], y_off)
        self.assertAlmostEqual(intersect[2], 0)

    def test_inside_polygon_trivial_triangle(self):
        """
        Trivial point on triangle with inside_polygon
        """

        point = np.array([0, 0, 0])

        corner1 = np.array([0, 1, 0])
        corner2 = np.array([-0.5, -1, 0])
        corner3 = np.array([0.5, -1, 0])

        self.assertTrue(inside_polygon(point, [corner1, corner2, corner3]))

        point = np.array([0, 0, 0.1])
        self.assertFalse(inside_polygon(point, [corner1, corner2, corner3]))

    def test_inside_polygon_trivial_rectangle(self):
        """
        Trivial point on triangle with inside_polygon
        """

        point = np.array([0, 0, 0])

        corner1 = np.array([-1, -1, 0])
        corner2 = np.array([-1, 1, 0])
        corner3 = np.array([1, 1, 0])
        corner4 = np.array([1, -1, 0])

        self.assertTrue(inside_polygon(point, [corner1, corner2, corner3, corner4]))

        point = np.array([0, 0, 0.1])
        self.assertFalse(inside_polygon(point, [corner1, corner2, corner3, corner4]))

    def test_intersection_point_on_element_simple(self):
        """
        Ensure element_geometry returns good corners and that intersection points
        are determined to be inside / outside the relevant polygon
        """
        element_geometry = BaseElementGeometry(start_point=2.0, next_start_point=5.0,
                                               start_width=0.02, start_height=0.04,
                                               end_width=0.08, end_height=0.04)

        pr = PositionAndRotation(np.array([0, 0, 0]), R.from_euler("z", 0))

        # Corner points at start
        corners = element_geometry.get_corners(start_pr=pr, distance_unit_less=0)

        x_off_list = [0.009, 0.03, -0.03, 0.008, 0.008]
        y_off_list = [0.015, 0.015, 0.015, 0.041, -0.041]
        result_list = [True, False, False, False, False]

        for x_off, y_off, result in zip(x_off_list, y_off_list, result_list):
            p0 = np.array([x_off, y_off, -1])
            p1 = np.array([x_off, y_off, 1])

            intersect = line_intersect_plane(point0=p0, point1=p1, pr=pr)
            if result:
                self.assertTrue(inside_polygon(intersect, corners))
            else:
                self.assertFalse(inside_polygon(intersect, corners))

    def test_intersection_point_on_element_rotated(self):
        """
        Ensure element_geometry returns good corners and that intersection points
        are determined to be inside / outside the relevant polygon, here with a
        rotated element geometry.
        """
        element_geometry = BaseElementGeometry(start_point=2.0, next_start_point=5.0,
                                               start_width=0.02, start_height=0.04,
                                               end_width=0.08, end_height=0.04)

        z_point = 50
        pr = PositionAndRotation(np.array([0, 0, z_point]), R.from_euler("y", 12, degrees=True))

        # Corner points at start
        corners = element_geometry.get_corners(start_pr=pr, distance_unit_less=0)

        x_off_list = [0.006, 0.0099, 0.03, -0.03, 0.008, 0.008]
        y_off_list = [0.015, 0.015, 0.015, 0.015, 0.041, -0.041]
        result_list = [True, False, False, False, False, False]

        for x_off, y_off, result in zip(x_off_list, y_off_list, result_list):
            p0 = np.array([x_off, y_off, -1000])
            p1 = np.array([x_off, y_off, 1000])

            intersect = line_intersect_plane(point0=p0, point1=p1, pr=pr)
            if result:
                self.assertTrue(inside_polygon(intersect, corners))
            else:
                self.assertFalse(inside_polygon(intersect, corners))

            # since rotated around y, should be closer on one side.
            if x_off > 0:
                self.assertTrue(intersect[2] < z_point)
            else:
                self.assertTrue(intersect[2] > z_point)
