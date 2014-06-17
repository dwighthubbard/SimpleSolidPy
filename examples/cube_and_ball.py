#!/usr/bin/env python
#import SimpleSolidPy
import sys
sys.path.append('.')
from SimpleSolidPy.primitives import *


c = Cube(10)
s = Sphere(7)

c = c.attachment('center') + s.attachment('center')

c.show()
c.exportStl('testfile.stl')
SimpleSolidPy.root_window.start()
