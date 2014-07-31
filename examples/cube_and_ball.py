#!/usr/bin/env python
#import SimpleSolidPy
import sys
sys.path.append('.')
from SimpleSolidPy.primitives import *


# Get a cube and a sphere
c = Cube(10)
s = Sphere(7)

# Connect their centers and fuse into a single object
c = c.attachment('center') + s.attachment('center')

# Draw our window
SimpleSolidPy.root_window.start()
