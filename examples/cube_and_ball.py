#!/usr/bin/env python
#import SimpleSolidPy
from SimpleSolidPy.primitives import *


c = Cube(10)
s = Sphere(7)

c = c.attachment('center') + s.attachment('center')

c.show()
SimpleSolidPy.root_window.start()
