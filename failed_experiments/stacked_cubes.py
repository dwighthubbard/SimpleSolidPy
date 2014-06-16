#!/usr/bin/python2.7
"""
Build a pyramid
"""
import sys
sys.path.append('.')
from SimpleSolidPy.container import FreeCADContainer
from SimpleSolidPy.primitives import Cube

container = FreeCADContainer()
c = None
for i in range(10, 1, -1):
    c_new = Cube(i, i, 1)
    if c:
        c = c.attachment('top') + c_new.attachment('bottom')
    else:
        c = c_new
container.start()
