#!/usr/bin/env python
import SimpleSolidPy
from SimpleSolidPy.primitives import Cube


base_width = 25
# Create a pyramid by drawing smaller and smaller cubes and stacking them on top of each other
c = None
for i in range(base_width, 1, -2):
    c_new = Cube(i, i, 2)
    if c:
        c = c.attachment('top') + c_new.attachment('bottom')
    else:
        c = c_new

# Show a view window
SimpleSolidPy.preview()
