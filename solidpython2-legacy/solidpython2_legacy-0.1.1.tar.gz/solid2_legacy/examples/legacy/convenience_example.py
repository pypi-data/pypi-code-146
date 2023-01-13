#! /usr/bin/env python3

from solid2 import *

#scale
c = cube(10, 20, 10).scale(2).scale(2, 2, 2).scale([3, 3, 3]).scale(0.5, .5)
#rotate
c = c.rotate(10).rotate(45, 45, 45).rotate(45, 45).rotate(a=4, v=[1, 1, 0])
#translate
c = c.translate(10, 0, 0).translate([0, 10, 0]).translate((0, 0, 0))
#mirror
c = c.mirror(1, 0, 0).mirror([0, 1, 0])
#mirror regular syntax
c = mirror(0, 0, 1)(c)


#2d
s = square(10, 20).translate(10, 5).rotate(45).linear_extrude(3) + cylinder(10, _fn=6)

scad_render_to_file(c + ~s)
