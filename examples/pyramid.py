#!/usr/bin/env python
import sys
sys.path.append('.')
from SimpleSolidPy.primitives import *


c = None
for i in range(10, 1, -1):
    c_new = Cube(i, i, 1)
    if c:
        c = c.attachment('top') + c_new.attachment('bottom')
    else:
        c = c_new

SimpleSolidPy.root_window.exportSTL('pyramid.stl')

SimpleSolidPy.root_window.start()
