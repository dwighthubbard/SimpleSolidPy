#!/usr/bin/env python
import PyQt4
from PyQt4 import QtGui
import sys

sys.path.append('.')
sys.path.append('/usr/lib/freecad/lib')

import FreeCAD, FreeCADGui, Part
import SimpleSolidPy.primitives


def getMainWindow():
     toplevel = QtGui.qApp.topLevelWidgets()
     for i in toplevel:
         print i.metaObject().className()
         if i.metaObject().className() == "Gui::MainWindow":
             return i
     raise Exception("No main window found")


#FreeCADGui.showMainWindow()
#FreeCADGui.setupWithoutGUI()

app = QtGui.qApp
FreeCADWindow = app.activeWindow()

mw=getMainWindow()
mw.showMinimized()

doc=FreeCAD.newDocument()

#box=Part.makeCone(10,8,10)
#Part.show(box)

c = None
for i in range(10, 1, -1):
    c_new = SimpleSolidPy.primitives.Cube(i, i, 1)
    if c:
        c = c.attachment('top') + c_new.attachment('bottom')
    else:
        c = c_new
c.show()

# switch off animation so that the camera is moved to the final position immediately
FreeCADGui.activeDocument().activeView().setAnimationEnabled(False)
FreeCADGui.activeDocument().activeView().viewAxometric()
FreeCADGui.activeDocument().activeView().fitAll()
#FreeCADGui.activeDocument().activeView().saveImage('crystal.png',800,600,'Current')

#FreeCAD.closeDocument(doc.Name)

# causes a crash because after processing this script the event is restarted!!!
#mw.deleteLater()
FreeCADGui.exec_loop()

