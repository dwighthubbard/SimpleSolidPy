#!/usr/bin/env python
#import SimpleSolidPy
from SimpleSolidPy.primitives import *


c = None
for i in range(10, 1, -1):
    #c_new = SimpleSolidPy.primitives.Cube(i, i, 1)
    c_new = Cube(i, i, 1)
    if c:
        c = c.attachment('top') + c_new.attachment('bottom')
    else:
        c = c_new
c.show()


SimpleSolidPy.root_window.start()
