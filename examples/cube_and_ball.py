#!/usr/bin/env python
import SimpleSolidPy
from SimpleSolidPy.primitives import Cube, Sphere


# Get a cube and a sphere
c = Cube(25.4)
s = Sphere(25.4*.7)

# Connect their centers and fuse into a single object
c.connect('center', s.attachment('center'))
s.color('red')

# Show a view window
SimpleSolidPy.preview()