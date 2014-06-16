#!/usr/bin/env python
import sys
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD
import FreeCADGui

from SimpleSolidPy.primitives import Cube

from pivy.sogui import *
from pivy.coin import *
import sys


def myViewer(iv):
    # Initialize Coin. This returns a main window to use.
    # If unsuccessful, exit.
    myWindow = SoGui.init([])
    if myWindow == None:
        print("No window")
        sys.exit(1)

    # Make an empty scene and add our node to it
    scene = SoSeparator()
    scene.addChild(iv)

    # Create a viewer in which to see our scene graph.
    viewer = SoGuiExaminerViewer(myWindow)

    # Put our scene into viewer, change the title
    viewer.setSceneGraph(scene)
    viewer.setTitle("FreeCAD Object Viewer")
    viewer.show()

    SoGui.show(myWindow) # Display main window
    SoGui.mainLoop()     # Main Coin event loop


doc = FreeCAD.newDocument()
c = None
for i in range(10, 1, -1):
    c_new = Cube(i, i, 1)
    if c:
        c = c.attachment('top') + c_new.attachment('bottom')
    else:
        c = c_new

from pivy import coin
inp = coin.SoInput()
inp.setBuffer(c)
myNode=coin.SoDB.readAll(inp)
myViewer(FreeCADGui.activeDocument().getObject().toString())
