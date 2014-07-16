#!/usr/bin/env python2.7

import sys
sys.path.append('.')
from PyQt4 import QtCore, QtGui
import SimpleSolidPy
import SimpleSolidPy.container
from SimpleSolidPy.primitives import *


SimpleSolidPy.root_window = SimpleSolidPy.container.EmbeddedContainer()
#SimpleSolidPy.root_window = SimpleSolidPy.container.FreeCADContainer()

c = Cube(10)
s = Sphere(7)

c = c.attachment('center') + s.attachment('center')

c.show()

#FreeCADGui.activeDocument().activeView().setAnimationEnabled(False)
#FreeCADGui.activeDocument().activeView().viewAxometric()
#FreeCADGui.activeDocument().activeView().fitAll()

SimpleSolidPy.root_window.app.exec_()
