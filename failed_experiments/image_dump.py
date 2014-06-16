#!/usr/bin/env python
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD,FreeCADGui
FreeCADGui.showMainWindow()
import Part,PartGui

OutDir = 'c:/temp/'
doc = FreeCAD.newDocument()
box = doc.addObject("Part::Box","myBox")
box.Height=4
box.Width=2
doc.recompute()
Gui.activeDocument().activeView().viewAxometric()
Gui.activeDocument().activeView().setAnimationEnabled(False)
Gui.SendMsgToActiveView("ViewFit")
